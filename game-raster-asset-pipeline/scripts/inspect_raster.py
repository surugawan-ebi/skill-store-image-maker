#!/usr/bin/env python3
"""Read-only validation for PNG outputs declared by raster-jobs.json."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import tempfile
import zlib
from pathlib import Path
from typing import Any


PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_FILE_BYTES = 256 * 1024 * 1024
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_PIXELS = 20_000_000
MAX_ASSETS = 256
MAX_COLLECTION_ITEMS = 4096
MAX_STRING_CHARS = 16_384
MAX_GRID_CELLS = 65_536
KINDS = {"sprite_sheet", "single_asset", "app_icon"}
TRANSPARENCY = {"required", "forbidden", "allowed"}


class ValidationError(ValueError):
    """Raised when an input contract or PNG structure is invalid."""


def require_int(value: Any, label: str, minimum: int = 0, maximum: int | None = None) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValidationError(f"{label} must be an integer")
    if value < minimum or (maximum is not None and value > maximum):
        upper = f" and <= {maximum}" if maximum is not None else ""
        raise ValidationError(f"{label} must be >= {minimum}{upper}")
    return value


def require_number(value: Any, label: str, minimum: float, maximum: float) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValidationError(f"{label} must be a number")
    number = float(value)
    if not minimum <= number <= maximum:
        raise ValidationError(f"{label} must be between {minimum} and {maximum}")
    return number


def resolve_relative(base: Path, raw: Any, label: str) -> Path:
    if not isinstance(raw, str) or not raw.strip():
        raise ValidationError(f"{label} must be a non-empty relative path")
    relative = Path(raw)
    if relative.is_absolute():
        raise ValidationError(f"{label} must not be absolute")
    resolved = (base / relative).resolve()
    try:
        resolved.relative_to(base.resolve())
    except ValueError as exc:
        raise ValidationError(f"{label} escapes the manifest directory") from exc
    return resolved


def validate_json_limits(value: Any, label: str = "manifest", depth: int = 0) -> None:
    if depth > 32:
        raise ValidationError(f"{label} nesting is too deep")
    if isinstance(value, str):
        if len(value) > MAX_STRING_CHARS:
            raise ValidationError(f"{label} exceeds {MAX_STRING_CHARS} characters")
        return
    if isinstance(value, list):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise ValidationError(f"{label} exceeds {MAX_COLLECTION_ITEMS} items")
        for index, item in enumerate(value):
            validate_json_limits(item, f"{label}[{index}]", depth + 1)
        return
    if isinstance(value, dict):
        if len(value) > MAX_COLLECTION_ITEMS:
            raise ValidationError(f"{label} exceeds {MAX_COLLECTION_ITEMS} keys")
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValidationError(f"{label} keys must be strings")
            validate_json_limits(key, f"{label} key", depth + 1)
            validate_json_limits(item, f"{label}.{key}", depth + 1)


def validate_manifest(data: Any, manifest_dir: Path) -> list[dict[str, Any]]:
    validate_json_limits(data)
    if not isinstance(data, dict):
        raise ValidationError("manifest root must be an object")
    if data.get("schema_version") != 1:
        raise ValidationError("schema_version must be 1")
    if not isinstance(data.get("project"), str) or not data["project"].strip():
        raise ValidationError("project must be a non-empty string")
    assets = data.get("assets")
    if not isinstance(assets, list) or not assets:
        raise ValidationError("assets must be a non-empty array")
    if len(assets) > MAX_ASSETS:
        raise ValidationError(f"assets must contain at most {MAX_ASSETS} entries")

    seen: set[str] = set()
    seen_outputs: set[Path] = set()
    protected_inputs: set[Path] = set()
    for index, asset in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(asset, dict):
            raise ValidationError(f"{label} must be an object")
        asset_id = asset.get("id")
        if not isinstance(asset_id, str) or not re.fullmatch(r"[a-z0-9-]+", asset_id):
            raise ValidationError(f"{label}.id must use lowercase letters, digits, and hyphens")
        if asset_id in seen:
            raise ValidationError(f"duplicate asset id: {asset_id}")
        seen.add(asset_id)
        if asset.get("kind") not in KINDS:
            raise ValidationError(f"{label}.kind must be one of {sorted(KINDS)}")
        references = asset.get("references")
        if not isinstance(references, list):
            raise ValidationError(f"{label}.references must be an array")
        reference_paths: list[Path] = []
        for ref_index, reference in enumerate(references):
            reference_path = resolve_relative(manifest_dir, reference, f"{label}.references[{ref_index}]")
            if not reference_path.is_file():
                raise ValidationError(f"{label}.references[{ref_index}] does not exist")
            reference_paths.append(reference_path)
            protected_inputs.add(reference_path)
        prompt_path = resolve_relative(manifest_dir, asset.get("prompt_file"), f"{label}.prompt_file")
        if not prompt_path.is_file():
            raise ValidationError(f"{label}.prompt_file does not exist")
        protected_inputs.add(prompt_path)

        output = asset.get("output")
        if not isinstance(output, dict):
            raise ValidationError(f"{label}.output must be an object")
        output_path = resolve_relative(manifest_dir, output.get("path"), f"{label}.output.path")
        if output_path in seen_outputs:
            raise ValidationError(f"duplicate output path: {output.get('path')}")
        seen_outputs.add(output_path)
        if output_path in reference_paths:
            raise ValidationError(f"{label}.output.path must not overwrite a reference")
        if output_path == prompt_path:
            raise ValidationError(f"{label}.output.path must not overwrite the saved prompt")
        if output.get("format") != "png":
            raise ValidationError(f"{label}.output.format must be png")
        if output_path.suffix.lower() != ".png":
            raise ValidationError(f"{label}.output.path must end in .png")
        width = require_int(output.get("width"), f"{label}.output.width", 1, MAX_PIXELS)
        height = require_int(output.get("height"), f"{label}.output.height", 1, MAX_PIXELS)
        if width * height > MAX_PIXELS:
            raise ValidationError(f"{label}.output dimensions exceed the {MAX_PIXELS}-pixel safety limit")
        if asset["kind"] == "app_icon" and output["width"] != output["height"]:
            raise ValidationError(f"{label} app_icon output must be square")
        if asset.get("transparency") not in TRANSPARENCY:
            raise ValidationError(f"{label}.transparency must be one of {sorted(TRANSPARENCY)}")
        validate_palette_contract(asset.get("palette"), label)
        validate_grid_contract(asset.get("grid"), asset, label)
    collisions = seen_outputs & protected_inputs
    if collisions:
        raise ValidationError("an output path must not overwrite any job's reference or saved prompt")
    return assets


def validate_palette_contract(palette: Any, label: str) -> None:
    if palette is None:
        return
    if not isinstance(palette, dict):
        raise ValidationError(f"{label}.palette must be an object")
    colors = palette.get("colors")
    if not isinstance(colors, list) or not colors:
        raise ValidationError(f"{label}.palette.colors must be a non-empty array")
    for color in colors:
        if not isinstance(color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", color):
            raise ValidationError(f"{label}.palette.colors values must be #RRGGBB")
    require_int(palette.get("tolerance", 0), f"{label}.palette.tolerance", 0, 255)
    require_int(palette.get("alpha_threshold", 0), f"{label}.palette.alpha_threshold", 0, 255)
    require_number(
        palette.get("max_out_of_palette_fraction", 0.0),
        f"{label}.palette.max_out_of_palette_fraction",
        0.0,
        1.0,
    )


def validate_grid_contract(grid: Any, asset: dict[str, Any], label: str) -> None:
    if grid is None:
        if asset["kind"] == "sprite_sheet":
            raise ValidationError(f"{label}.grid is required for sprite_sheet")
        return
    if asset["kind"] != "sprite_sheet":
        raise ValidationError(f"{label}.grid is allowed only for sprite_sheet")
    if not isinstance(grid, dict):
        raise ValidationError(f"{label}.grid must be an object")
    occupancy_mode = grid.get("occupancy_mode")
    if occupancy_mode not in {"alpha", "background_color"}:
        raise ValidationError(f"{label}.grid.occupancy_mode must be alpha or background_color")
    if occupancy_mode == "alpha":
        if asset["transparency"] != "required":
            raise ValidationError(f"{label}.transparency must be required for alpha occupancy")
        if "background_color" in grid or "background_tolerance" in grid:
            raise ValidationError(f"{label}.grid background fields are not allowed for alpha occupancy")
        require_int(grid.get("alpha_threshold", 0), f"{label}.grid.alpha_threshold", 0, 255)
    else:
        if asset["transparency"] not in {"forbidden", "allowed"}:
            raise ValidationError(
                f"{label}.transparency must be forbidden or allowed for background_color occupancy"
            )
        background_color = grid.get("background_color")
        if not isinstance(background_color, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}", background_color):
            raise ValidationError(f"{label}.grid.background_color must be #RRGGBB")
        if "alpha_threshold" in grid:
            raise ValidationError(f"{label}.grid.alpha_threshold is not allowed for background_color occupancy")
        require_int(grid.get("background_tolerance", 0), f"{label}.grid.background_tolerance", 0, 255)
    columns = require_int(grid.get("columns"), f"{label}.grid.columns", 1)
    rows = require_int(grid.get("rows"), f"{label}.grid.rows", 1)
    if columns * rows > MAX_GRID_CELLS:
        raise ValidationError(f"{label}.grid exceeds the {MAX_GRID_CELLS}-cell safety limit")
    cell_width = require_int(grid.get("cell_width"), f"{label}.grid.cell_width", 1)
    cell_height = require_int(grid.get("cell_height"), f"{label}.grid.cell_height", 1)
    origin_x = require_int(grid.get("origin_x", 0), f"{label}.grid.origin_x", 0)
    origin_y = require_int(grid.get("origin_y", 0), f"{label}.grid.origin_y", 0)
    stride_x = require_int(grid.get("stride_x", cell_width), f"{label}.grid.stride_x", cell_width)
    stride_y = require_int(grid.get("stride_y", cell_height), f"{label}.grid.stride_y", cell_height)
    require_int(grid.get("min_occupied_pixels", 1), f"{label}.grid.min_occupied_pixels", 1)
    require_int(
        grid.get("unexpected_cell_max_pixels", 0),
        f"{label}.grid.unexpected_cell_max_pixels",
        0,
    )
    gutter = require_int(grid.get("transparent_gutter", 0), f"{label}.grid.transparent_gutter", 0)
    if gutter * 2 >= min(cell_width, cell_height):
        raise ValidationError(f"{label}.grid.transparent_gutter leaves no cell interior")
    occupied = grid.get("occupied_cells")
    if not isinstance(occupied, list) or not occupied:
        raise ValidationError(f"{label}.grid.occupied_cells must be a non-empty array")
    normalized = [require_int(value, f"{label}.grid.occupied_cells[]", 0, columns * rows - 1) for value in occupied]
    if len(set(normalized)) != len(normalized):
        raise ValidationError(f"{label}.grid.occupied_cells must not contain duplicates")
    width = asset["output"]["width"]
    height = asset["output"]["height"]
    if origin_x + (columns - 1) * stride_x + cell_width > width:
        raise ValidationError(f"{label}.grid exceeds output width")
    if origin_y + (rows - 1) * stride_y + cell_height > height:
        raise ValidationError(f"{label}.grid exceeds output height")


def parse_png(path: Path) -> tuple[int, int, bytes]:
    size = path.stat().st_size
    if size > MAX_FILE_BYTES:
        raise ValidationError(f"PNG exceeds {MAX_FILE_BYTES} bytes")
    payload = path.read_bytes()
    if not payload.startswith(PNG_SIGNATURE):
        raise ValidationError("output is not a PNG file")

    position = len(PNG_SIGNATURE)
    ihdr: tuple[int, int, int, int, int, int, int] | None = None
    idat: list[bytes] = []
    palette: bytes | None = None
    transparency: bytes | None = None
    saw_iend = False
    saw_idat = False
    idat_ended = False
    while position + 12 <= len(payload):
        length = struct.unpack(">I", payload[position : position + 4])[0]
        chunk_type = payload[position + 4 : position + 8]
        end = position + 12 + length
        if end > len(payload):
            raise ValidationError("PNG chunk exceeds file length")
        chunk_data = payload[position + 8 : position + 8 + length]
        expected_crc = struct.unpack(">I", payload[position + 8 + length : end])[0]
        actual_crc = zlib.crc32(chunk_type)
        actual_crc = zlib.crc32(chunk_data, actual_crc) & 0xFFFFFFFF
        if actual_crc != expected_crc:
            raise ValidationError(f"PNG chunk {chunk_type.decode('latin1')} has an invalid CRC")
        if len(chunk_type) != 4 or not all(65 <= byte <= 90 or 97 <= byte <= 122 for byte in chunk_type):
            raise ValidationError("PNG chunk type must contain ASCII letters")
        if ihdr is None and chunk_type != b"IHDR":
            raise ValidationError("IHDR must be the first PNG chunk")
        if chunk_type == b"IHDR":
            if length != 13 or ihdr is not None:
                raise ValidationError("PNG must contain one valid IHDR")
            ihdr = struct.unpack(">IIBBBBB", chunk_data)
        elif chunk_type == b"PLTE":
            if saw_idat or palette is not None or not length or length > 768 or length % 3:
                raise ValidationError("PNG has an invalid PLTE chunk")
            palette = chunk_data
        elif chunk_type == b"tRNS":
            if saw_idat or transparency is not None:
                raise ValidationError("PNG has an invalid tRNS chunk")
            transparency = chunk_data
        elif chunk_type == b"IDAT":
            if idat_ended:
                raise ValidationError("PNG IDAT chunks must be consecutive")
            saw_idat = True
            idat.append(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0:
                raise ValidationError("PNG IEND chunk must be empty")
            saw_iend = True
            position = end
            break
        elif chunk_type[0] & 0x20 == 0:
            raise ValidationError(f"unsupported critical PNG chunk: {chunk_type.decode('ascii')}")
        if saw_idat and chunk_type != b"IDAT":
            idat_ended = True
        position = end

    if ihdr is None or not idat or not saw_iend:
        raise ValidationError("PNG is missing IHDR, IDAT, or IEND")
    if position != len(payload):
        raise ValidationError("PNG has trailing data after IEND")
    width, height, bit_depth, color_type, compression, filtering, interlace = ihdr
    if not width or not height or width * height > MAX_PIXELS:
        raise ValidationError(f"PNG dimensions exceed the {MAX_PIXELS}-pixel safety limit")
    if bit_depth != 8:
        raise ValidationError("only 8-bit PNG files are supported")
    if color_type not in {0, 2, 3, 4, 6}:
        raise ValidationError(f"unsupported PNG color type: {color_type}")
    if color_type == 3 and palette is None:
        raise ValidationError("indexed PNG requires PLTE")
    if color_type in {0, 4} and palette is not None:
        raise ValidationError("grayscale PNG must not contain PLTE")
    if color_type in {4, 6} and transparency is not None:
        raise ValidationError("PNG with an alpha channel must not contain tRNS")
    if transparency is not None:
        if color_type == 0 and len(transparency) != 2:
            raise ValidationError("grayscale PNG tRNS must contain one sample")
        if color_type == 2 and len(transparency) != 6:
            raise ValidationError("truecolor PNG tRNS must contain three samples")
        if color_type == 3 and (palette is None or not transparency or len(transparency) > len(palette) // 3):
            raise ValidationError("indexed PNG has an invalid tRNS chunk")
    if compression != 0 or filtering != 0 or interlace != 0:
        raise ValidationError("only standard, non-interlaced PNG files are supported")

    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color_type]
    row_bytes = width * channels
    expected_raw_size = height * (row_bytes + 1)
    try:
        decompressor = zlib.decompressobj()
        raw = decompressor.decompress(b"".join(idat), expected_raw_size + 1)
        if len(raw) > expected_raw_size or decompressor.unconsumed_tail:
            raise ValidationError("PNG decompressed data exceeds the IHDR size")
        raw += decompressor.flush(expected_raw_size + 1 - len(raw))
    except zlib.error as exc:
        raise ValidationError(f"PNG IDAT decompression failed: {exc}") from exc
    if len(raw) != expected_raw_size or not decompressor.eof or decompressor.unused_data:
        raise ValidationError("PNG decompressed data length does not match IHDR")

    reconstructed = bytearray()
    previous = bytearray(row_bytes)
    offset = 0
    for _ in range(height):
        filter_type = raw[offset]
        scanline = bytearray(raw[offset + 1 : offset + 1 + row_bytes])
        offset += row_bytes + 1
        if filter_type > 4:
            raise ValidationError(f"unsupported PNG filter type: {filter_type}")
        for index in range(row_bytes):
            left = scanline[index - channels] if index >= channels else 0
            above = previous[index]
            upper_left = previous[index - channels] if index >= channels else 0
            if filter_type == 1:
                scanline[index] = (scanline[index] + left) & 0xFF
            elif filter_type == 2:
                scanline[index] = (scanline[index] + above) & 0xFF
            elif filter_type == 3:
                scanline[index] = (scanline[index] + ((left + above) // 2)) & 0xFF
            elif filter_type == 4:
                scanline[index] = (scanline[index] + paeth(left, above, upper_left)) & 0xFF
        reconstructed.extend(scanline)
        previous = scanline

    rgba = expand_rgba(reconstructed, color_type, palette, transparency)
    return width, height, bytes(rgba)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def paeth(left: int, above: int, upper_left: int) -> int:
    prediction = left + above - upper_left
    left_distance = abs(prediction - left)
    above_distance = abs(prediction - above)
    upper_left_distance = abs(prediction - upper_left)
    if left_distance <= above_distance and left_distance <= upper_left_distance:
        return left
    if above_distance <= upper_left_distance:
        return above
    return upper_left


def expand_rgba(
    samples: bytearray,
    color_type: int,
    palette: bytes | None,
    transparency: bytes | None,
) -> bytearray:
    rgba = bytearray()
    if color_type == 6:
        return samples
    if color_type == 4:
        for index in range(0, len(samples), 2):
            gray, alpha = samples[index : index + 2]
            rgba.extend((gray, gray, gray, alpha))
        return rgba
    if color_type == 2:
        transparent_rgb = struct.unpack(">HHH", transparency) if transparency and len(transparency) == 6 else None
        for index in range(0, len(samples), 3):
            red, green, blue = samples[index : index + 3]
            alpha = 0 if transparent_rgb == (red, green, blue) else 255
            rgba.extend((red, green, blue, alpha))
        return rgba
    if color_type == 0:
        transparent_gray = struct.unpack(">H", transparency)[0] if transparency and len(transparency) == 2 else None
        for gray in samples:
            alpha = 0 if transparent_gray == gray else 255
            rgba.extend((gray, gray, gray, alpha))
        return rgba
    if palette is None or not palette or len(palette) % 3:
        raise ValidationError("indexed PNG has no valid PLTE")
    entries = [tuple(palette[index : index + 3]) for index in range(0, len(palette), 3)]
    alpha_values = transparency or b""
    for palette_index in samples:
        if palette_index >= len(entries):
            raise ValidationError("indexed PNG references a missing palette entry")
        red, green, blue = entries[palette_index]
        alpha = alpha_values[palette_index] if palette_index < len(alpha_values) else 255
        rgba.extend((red, green, blue, alpha))
    return rgba


def parse_colors(raw_colors: list[str]) -> list[tuple[int, int, int]]:
    return [tuple(int(color[index : index + 2], 16) for index in (1, 3, 5)) for color in raw_colors]


def palette_measurements(rgba: bytes, contract: dict[str, Any]) -> dict[str, Any]:
    allowed = parse_colors(contract["colors"])
    tolerance = contract.get("tolerance", 0)
    alpha_threshold = contract.get("alpha_threshold", 0)
    visible = 0
    outside = 0
    samples: list[str] = []
    for index in range(0, len(rgba), 4):
        red, green, blue, alpha = rgba[index : index + 4]
        if alpha <= alpha_threshold:
            continue
        visible += 1
        matches = any(max(abs(red - ar), abs(green - ag), abs(blue - ab)) <= tolerance for ar, ag, ab in allowed)
        if not matches:
            outside += 1
            color = f"#{red:02X}{green:02X}{blue:02X}"
            if color not in samples and len(samples) < 8:
                samples.append(color)
    return {
        "visible_pixels": visible,
        "out_of_palette_pixels": outside,
        "out_of_palette_fraction": outside / visible if visible else 0.0,
        "sample_out_of_palette_colors": samples,
    }


def grid_measurements(rgba: bytes, width: int, height: int, grid: dict[str, Any]) -> dict[str, Any]:
    columns = grid["columns"]
    rows = grid["rows"]
    cell_width = grid["cell_width"]
    cell_height = grid["cell_height"]
    origin_x = grid.get("origin_x", 0)
    origin_y = grid.get("origin_y", 0)
    stride_x = grid.get("stride_x", cell_width)
    stride_y = grid.get("stride_y", cell_height)
    gutter = grid.get("transparent_gutter", 0)
    occupancy_mode = grid["occupancy_mode"]
    alpha_threshold = grid.get("alpha_threshold", 0)
    background = parse_colors([grid["background_color"]])[0] if occupancy_mode == "background_color" else None
    background_tolerance = grid.get("background_tolerance", 0)
    occupancy = [0] * (columns * rows)
    gutter_pixels = [0] * (columns * rows)
    outside = 0

    for y in range(height):
        for x in range(width):
            pixel_offset = (y * width + x) * 4
            red, green, blue, alpha = rgba[pixel_offset : pixel_offset + 4]
            if occupancy_mode == "alpha":
                occupied = alpha > alpha_threshold
            else:
                assert background is not None
                background_red, background_green, background_blue = background
                occupied = alpha > 0 and max(
                    abs(red - background_red),
                    abs(green - background_green),
                    abs(blue - background_blue),
                ) > background_tolerance
            if not occupied:
                continue
            rel_x = x - origin_x
            rel_y = y - origin_y
            column = rel_x // stride_x if rel_x >= 0 else -1
            row = rel_y // stride_y if rel_y >= 0 else -1
            in_cell = (
                0 <= column < columns
                and 0 <= row < rows
                and rel_x - column * stride_x < cell_width
                and rel_y - row * stride_y < cell_height
            )
            if not in_cell:
                outside += 1
                continue
            cell = row * columns + column
            local_x = rel_x - column * stride_x
            local_y = rel_y - row * stride_y
            occupancy[cell] += 1
            if gutter and (
                local_x < gutter
                or local_x >= cell_width - gutter
                or local_y < gutter
                or local_y >= cell_height - gutter
            ):
                gutter_pixels[cell] += 1
    return {
        "cell_occupancy": occupancy,
        "cell_gutter_pixels": gutter_pixels,
        "occupied_pixels_outside_grid": outside,
    }


def validate_asset(asset: dict[str, Any], manifest_dir: Path) -> dict[str, Any]:
    output_path = resolve_relative(manifest_dir, asset["output"]["path"], "output.path")
    result: dict[str, Any] = {
        "asset_id": asset["id"],
        "image": asset["output"]["path"],
        "passed": False,
        "checks": [],
        "measurements": {},
    }

    def check(name: str, passed: bool, detail: str) -> None:
        result["checks"].append({"name": name, "status": "passed" if passed else "failed", "detail": detail})

    if not output_path.is_file():
        check("file", False, "declared output does not exist")
        return result

    try:
        width, height, rgba = parse_png(output_path)
    except (OSError, ValidationError) as exc:
        check("png", False, str(exc))
        return result

    check("png", True, "valid supported PNG")
    result["measurements"]["sha256"] = sha256_file(output_path)
    expected_width = asset["output"]["width"]
    expected_height = asset["output"]["height"]
    result["measurements"]["width"] = width
    result["measurements"]["height"] = height
    check(
        "dimensions",
        (width, height) == (expected_width, expected_height),
        f"measured {width}x{height}; expected {expected_width}x{expected_height}",
    )

    alpha_values = rgba[3::4]
    transparent_pixels = sum(alpha < 255 for alpha in alpha_values)
    fully_transparent_pixels = sum(alpha == 0 for alpha in alpha_values)
    result["measurements"]["transparent_pixels"] = transparent_pixels
    result["measurements"]["fully_transparent_pixels"] = fully_transparent_pixels
    policy = asset["transparency"]
    alpha_passed = policy == "allowed" or (policy == "required" and fully_transparent_pixels > 0) or (
        policy == "forbidden" and transparent_pixels == 0
    )
    check(
        "transparency",
        alpha_passed,
        f"policy {policy}; {transparent_pixels} pixels have alpha below 255 and "
        f"{fully_transparent_pixels} are fully transparent",
    )

    palette = asset.get("palette")
    if palette:
        measured_palette = palette_measurements(rgba, palette)
        result["measurements"]["palette"] = measured_palette
        maximum = palette.get("max_out_of_palette_fraction", 0.0)
        check(
            "palette",
            measured_palette["out_of_palette_fraction"] <= maximum,
            f"out-of-palette fraction {measured_palette['out_of_palette_fraction']:.8f}; maximum {maximum}",
        )

    grid = asset.get("grid")
    if grid and (width, height) == (expected_width, expected_height):
        measured_grid = grid_measurements(rgba, width, height, grid)
        result["measurements"]["grid"] = measured_grid
        occupied = set(grid["occupied_cells"])
        minimum = grid.get("min_occupied_pixels", 1)
        unexpected_maximum = grid.get("unexpected_cell_max_pixels", 0)
        occupancy_ok = all(
            count >= minimum if cell in occupied else count <= unexpected_maximum
            for cell, count in enumerate(measured_grid["cell_occupancy"])
        )
        check("grid_occupancy", occupancy_ok, f"cell pixel counts {measured_grid['cell_occupancy']}")
        check(
            "grid_bounds",
            measured_grid["occupied_pixels_outside_grid"] == 0,
            f"{measured_grid['occupied_pixels_outside_grid']} occupied pixels fall outside declared cells",
        )
        check(
            "transparent_gutter",
            not grid.get("transparent_gutter", 0) or not any(measured_grid["cell_gutter_pixels"]),
            f"occupied gutter pixels by cell {measured_grid['cell_gutter_pixels']}",
        )

    result["passed"] = all(item["status"] == "passed" for item in result["checks"])
    return result


def run_self_test() -> None:
    rgba = bytes((0x17, 0x20, 0x38, 255, 0, 0, 0, 0, 0x18, 0x20, 0x38, 255, 0, 0, 0, 0))
    palette = palette_measurements(
        rgba,
        {"colors": ["#172038"], "tolerance": 1, "alpha_threshold": 0},
    )
    assert palette["visible_pixels"] == 2
    assert palette["out_of_palette_pixels"] == 0
    outside_palette = palette_measurements(
        bytes((0x40, 0x40, 0x40, 255)),
        {"colors": ["#000000"], "tolerance": 1, "alpha_threshold": 0},
    )
    assert outside_palette["out_of_palette_pixels"] == 1
    grid = grid_measurements(
        rgba,
        2,
        2,
        {"occupancy_mode": "alpha", "columns": 1, "rows": 1, "cell_width": 2, "cell_height": 2},
    )
    assert grid["cell_occupancy"] == [2]
    assert grid["occupied_pixels_outside_grid"] == 0
    two_cell_rgba = bytearray(8 * 4 * 4)
    for x, y in ((1, 1), (5, 1)):
        offset = (y * 8 + x) * 4
        two_cell_rgba[offset : offset + 4] = bytes((255, 255, 255, 255))
    two_cells = grid_measurements(
        bytes(two_cell_rgba),
        8,
        4,
        {
            "occupancy_mode": "alpha",
            "columns": 2,
            "rows": 1,
            "cell_width": 4,
            "cell_height": 4,
            "transparent_gutter": 1,
        },
    )
    assert two_cells["cell_occupancy"] == [1, 1]
    assert two_cells["cell_gutter_pixels"] == [0, 0]
    opaque_white_sheet = bytearray(bytes((255, 255, 255, 255)) * (8 * 4))
    for x, y in ((1, 1), (5, 1)):
        offset = (y * 8 + x) * 4
        opaque_white_sheet[offset : offset + 4] = bytes((0, 0, 0, 255))
    background_cells = grid_measurements(
        bytes(opaque_white_sheet),
        8,
        4,
        {
            "occupancy_mode": "background_color",
            "background_color": "#FFFFFF",
            "background_tolerance": 0,
            "columns": 2,
            "rows": 1,
            "cell_width": 4,
            "cell_height": 4,
            "transparent_gutter": 1,
        },
    )
    assert background_cells["cell_occupancy"] == [1, 1]
    assert background_cells["cell_gutter_pixels"] == [0, 0]
    assert background_cells["occupied_pixels_outside_grid"] == 0
    background_contract_asset = {
        "kind": "sprite_sheet",
        "transparency": "forbidden",
        "output": {"width": 8, "height": 4},
    }
    validate_grid_contract(
        {
            "occupancy_mode": "background_color",
            "background_color": "#FFFFFF",
            "background_tolerance": 0,
            "columns": 2,
            "rows": 1,
            "cell_width": 4,
            "cell_height": 4,
            "occupied_cells": [0, 1],
        },
        background_contract_asset,
        "self_test",
    )
    try:
        validate_grid_contract(
            {
                "occupancy_mode": "alpha",
                "columns": 2,
                "rows": 1,
                "cell_width": 4,
                "cell_height": 4,
                "occupied_cells": [0, 1],
            },
            background_contract_asset,
            "self_test",
        )
    except ValidationError:
        pass
    else:
        raise AssertionError("alpha occupancy must reject forbidden transparency")
    assert paeth(10, 20, 15) == 15

    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        prompt = root / "prompt.md"
        prompt.write_text("test prompt", encoding="utf-8")
        valid_png = root / "valid.png"
        write_test_png(valid_png, 1, 1, bytes((0, 10, 20, 30, 0)))
        parsed_width, parsed_height, parsed_rgba = parse_png(valid_png)
        assert (parsed_width, parsed_height) == (1, 1)
        assert parsed_rgba == bytes((10, 20, 30, 0))

        almost_opaque = root / "almost-opaque.png"
        write_test_png(almost_opaque, 1, 1, bytes((0, 10, 20, 30, 254)))
        alpha_result = validate_asset(
            {
                "id": "alpha-test",
                "kind": "single_asset",
                "references": [],
                "prompt_file": "prompt.md",
                "output": {"path": "almost-opaque.png", "format": "png", "width": 1, "height": 1},
                "transparency": "required",
            },
            root,
        )
        assert not alpha_result["passed"]

        oversized_raw = root / "oversized-raw.png"
        write_test_png(oversized_raw, 1, 1, bytes((0, 10, 20, 30, 0, 99)))
        try:
            parse_png(oversized_raw)
        except ValidationError:
            pass
        else:
            raise AssertionError("PNG data beyond the IHDR dimensions must be rejected")

        trailing_png = root / "trailing.png"
        trailing_png.write_bytes(valid_png.read_bytes() + b"trailing")
        try:
            parse_png(trailing_png)
        except ValidationError:
            pass
        else:
            raise AssertionError("PNG trailing data must be rejected")

        nonempty_iend = root / "nonempty-iend.png"
        write_test_png(nonempty_iend, 1, 1, bytes((0, 10, 20, 30, 0)), iend_payload=b"x")
        try:
            parse_png(nonempty_iend)
        except ValidationError:
            pass
        else:
            raise AssertionError("non-empty IEND must be rejected")

        unknown_critical = root / "unknown-critical.png"
        write_test_png(unknown_critical, 1, 1, bytes((0, 10, 20, 30, 0)), before_idat=(b"ABCD", b"x"))
        try:
            parse_png(unknown_critical)
        except ValidationError:
            pass
        else:
            raise AssertionError("unknown critical PNG chunks must be rejected")

        for filename, kind, payload in (
            ("invalid-plte.png", b"PLTE", b"xx"),
            ("rgba-trns.png", b"tRNS", b"\x00\x00"),
        ):
            malformed = root / filename
            write_test_png(malformed, 1, 1, bytes((0, 10, 20, 30, 0)), before_idat=(kind, payload))
            try:
                parse_png(malformed)
            except ValidationError:
                pass
            else:
                raise AssertionError(f"malformed PNG structure must be rejected: {filename}")

        oversized_dimensions = {
            "schema_version": 1,
            "project": "self-test",
            "assets": [{
                "id": "oversized-dimensions",
                "kind": "single_asset",
                "references": [],
                "prompt_file": "prompt.md",
                "output": {
                    "path": "valid.png",
                    "format": "png",
                    "width": MAX_PIXELS,
                    "height": 2,
                },
                "transparency": "allowed",
            }],
        }
        try:
            validate_manifest(oversized_dimensions, root)
        except ValidationError:
            pass
        else:
            raise AssertionError("oversized declared dimensions must be rejected")

        huge_grid = {
            "schema_version": 1,
            "project": "self-test",
            "assets": [{
                "id": "huge-grid",
                "kind": "sprite_sheet",
                "references": [],
                "prompt_file": "prompt.md",
                "output": {"path": "valid.png", "format": "png", "width": 1, "height": 1},
                "transparency": "required",
                "grid": {
                    "occupancy_mode": "alpha",
                    "columns": MAX_GRID_CELLS + 1,
                    "rows": 1,
                    "cell_width": 1,
                    "cell_height": 1,
                    "occupied_cells": [0],
                },
            }],
        }
        try:
            validate_manifest(huge_grid, root)
        except ValidationError:
            pass
        else:
            raise AssertionError("oversized grids must be rejected before allocation")

        collision = {
            "schema_version": 1,
            "project": "self-test",
            "assets": [
                {
                    "id": "collision",
                    "kind": "single_asset",
                    "references": [],
                    "prompt_file": "valid.png",
                    "output": {"path": "valid.png", "format": "png", "width": 1, "height": 1},
                    "transparency": "allowed",
                }
            ],
        }
        try:
            validate_manifest(collision, root)
        except ValidationError:
            pass
        else:
            raise AssertionError("output path must not overwrite the saved prompt")

        second_prompt = root / "second-prompt.md"
        second_prompt.write_text("second prompt", encoding="utf-8")
        cross_job_collision = {
            "schema_version": 1,
            "project": "self-test",
            "assets": [
                {
                    "id": "first-output",
                    "kind": "single_asset",
                    "references": [],
                    "prompt_file": "prompt.md",
                    "output": {"path": "valid.png", "format": "png", "width": 1, "height": 1},
                    "transparency": "allowed",
                },
                {
                    "id": "second-input",
                    "kind": "single_asset",
                    "references": ["valid.png"],
                    "prompt_file": "second-prompt.md",
                    "output": {"path": "other.png", "format": "png", "width": 1, "height": 1},
                    "transparency": "allowed",
                },
            ],
        }
        try:
            validate_manifest(cross_job_collision, root)
        except ValidationError:
            pass
        else:
            raise AssertionError("an output must not overwrite another job's reference")


def write_test_png(
    path: Path,
    width: int,
    height: int,
    raw_scanlines: bytes,
    *,
    before_idat: tuple[bytes, bytes] | None = None,
    iend_payload: bytes = b"",
) -> None:
    def chunk(kind: bytes, payload: bytes) -> bytes:
        crc = zlib.crc32(kind)
        crc = zlib.crc32(payload, crc) & 0xFFFFFFFF
        return struct.pack(">I", len(payload)) + kind + payload + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 6, 0, 0, 0)
    middle = chunk(*before_idat) if before_idat else b""
    path.write_bytes(
        PNG_SIGNATURE
        + chunk(b"IHDR", ihdr)
        + middle
        + chunk(b"IDAT", zlib.compress(raw_scanlines))
        + chunk(b"IEND", iend_payload)
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, help="Path to raster-jobs.json")
    parser.add_argument("--asset", help="Validate only this asset id; otherwise validate all assets")
    parser.add_argument("--self-test", action="store_true", help="Run pure-function unit tests without reading images")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        print("inspect_raster self-test passed")
        return 0
    if args.manifest is None:
        parser.error("--manifest is required unless --self-test is used")

    try:
        manifest_path = args.manifest.resolve()
        if manifest_path.stat().st_size > MAX_MANIFEST_BYTES:
            raise ValidationError(f"manifest exceeds {MAX_MANIFEST_BYTES} bytes")
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
        assets = validate_manifest(data, manifest_path.parent)
        if args.asset:
            assets = [asset for asset in assets if asset["id"] == args.asset]
            if not assets:
                raise ValidationError(f"asset id not found: {args.asset}")
        results = [validate_asset(asset, manifest_path.parent) for asset in assets]
        report = {"manifest": str(args.manifest), "passed": all(item["passed"] for item in results), "assets": results}
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0 if report["passed"] else 1
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(json.dumps({"passed": False, "error": str(exc)}, indent=2, ensure_ascii=False))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
