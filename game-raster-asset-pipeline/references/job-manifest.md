# Raster Job Manifest

Use one `raster-jobs.json` per coherent batch. Paths are relative to the manifest directory. Do not commit absolute paths, credentials, signed URLs, or user-private locations.

## Top-level fields

```json
{
  "schema_version": 1,
  "project": "example-game",
  "assets": []
}
```

- `schema_version`: must be `1`.
- `project`: stable non-secret project label.
- `assets`: non-empty array of jobs with unique `id` values.

## Asset fields

Required fields:

- `id`: lowercase letters, digits, and hyphens.
- `kind`: `sprite_sheet`, `single_asset`, or `app_icon`.
- `references`: relative paths to supplied source images. Use `[]` for a genuinely text-only job; validate every path that is present and keep each source unchanged.
- `prompt_file`: relative path to the saved ImageGen prompt.
- `output.path`: unique relative candidate path for the untouched ImageGen PNG. It must not equal a reference path or another job output.
- `output.format`: `png`. The bundled inspector intentionally accepts only 8-bit, non-interlaced PNG; regenerate an unsupported output through ImageGen rather than converting it.
- `output.width`, `output.height`: exact positive pixel dimensions.
- `transparency`: `required`, `forbidden`, or `allowed`.

`required` means the output must contain at least one fully transparent pixel (`alpha = 0`), not merely antialiasing or a nearly opaque alpha value. Visual QA must still confirm that the intended background/margins are actually transparent.

Optional `palette` fields:

```json
"palette": {
  "colors": ["#172038", "#F2D27A", "#FFFFFF"],
  "tolerance": 0,
  "alpha_threshold": 0,
  "max_out_of_palette_fraction": 0.0
}
```

- `colors`: allowed visible RGB colors as six-digit hex values.
- `tolerance`: maximum per-channel distance from an allowed color, from `0` through `255`. Use `0` for strict pixel art.
- `alpha_threshold`: ignore pixels with alpha at or below this value when checking colors.
- `max_out_of_palette_fraction`: permitted fraction of visible pixels outside the palette, from `0.0` through `1.0`. Keep it at `0.0` unless antialiasing is explicitly approved.

Required `grid` fields for `sprite_sheet` jobs:

```json
"grid": {
  "occupancy_mode": "background_color",
  "background_color": "#FFFFFF",
  "background_tolerance": 0,
  "columns": 4,
  "rows": 2,
  "cell_width": 64,
  "cell_height": 64,
  "origin_x": 0,
  "origin_y": 0,
  "stride_x": 64,
  "stride_y": 64,
  "occupied_cells": [0, 1, 2, 3, 4, 5, 6, 7],
  "min_occupied_pixels": 24,
  "unexpected_cell_max_pixels": 0,
  "transparent_gutter": 1
}
```

- Number cells in row-major order from zero.
- Set `occupancy_mode` to `alpha` for transparent sheets. This mode treats pixels above `alpha_threshold` as occupied and requires `transparency: "required"`.
- Set `occupancy_mode` to `background_color` for opaque or mixed-alpha sheets with an intentional solid background. Supply `background_color` as `#RRGGBB` and `background_tolerance` from `0` through `255`. Fully transparent pixels and colors within the per-channel tolerance are unoccupied; other pixels are occupied. This mode allows `transparency: "forbidden"` or `"allowed"`.
- Do not mix mode-specific fields: alpha mode rejects background fields, and background-color mode rejects `alpha_threshold`.
- Prefer `background_color: "#FFFFFF"` with tolerance `0` when the contract requires a pure-white sheet. Increase tolerance only when the approved art specification explicitly permits near-background colors.
- Ensure every declared cell rectangle fits within the output canvas.
- `occupied_cells` lists cells that must contain at least `min_occupied_pixels` occupied pixels under the selected mode.
- Cells not listed may contain at most `unexpected_cell_max_pixels` occupied pixels.
- `transparent_gutter` is the existing field name for the required unoccupied pixel rows/columns along each cell edge. In background-color mode those rows/columns may contain the declared background rather than transparency. Use it to detect spill between frames.
- The grid check locates occupied cells; visual QA must still verify the pose assigned to each cell and its alignment against the reference.

## Path and output rules

- Resolve paths from the manifest directory and reject `..` escapes.
- Keep generated output below a dedicated `generated-assets/` directory when the target repository has no stronger convention.
- Save prompts below `prompts/` and preserve the exact prompt used.
- Do not overwrite an accepted asset during experimentation. Declare a new candidate path or version, validate it, then place it unchanged according to repository policy.
