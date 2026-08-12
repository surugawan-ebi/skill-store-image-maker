---
name: game-raster-asset-pipeline
description: Generate and quality-gate game raster assets with ImageGen, including faithful reference-to-sprite-sheet conversions, individual sprites or props, and app icons. Use when Codex must plan ImageGen jobs, preserve reference identity and cell order, place untouched outputs in a game project, verify PNG dimensions/transparency/palette/grid occupancy, visually inspect results, record provenance, or regenerate failed assets. Do not use for store/social promotional compositions, complete game-screen UI layouts, vector assets, or programmatic raster creation and editing.
---

# Game Raster Asset Pipeline

Generate final raster pixels only with ImageGen, then validate without changing them. Treat every generated file as immutable: a failed size, alpha, palette, grid, or visual check requires regeneration.

## Enforce the hard boundary

- Use ImageGen for every new or edited raster asset. Use the environment's ImageGen tool and its governing skill/instructions.
- Never use PIL, ImageMagick, SVG, canvas, HTML/CSS, Blender rendering, screenshots, procedural drawing, or another generator to create or edit the deliverable.
- Never resize, crop, pad, recolor, quantize, composite, sharpen, upscale, or remove a background after generation. Request the exact final pixel dimensions from ImageGen.
- Permit byte-for-byte copy or move operations only for placing an accepted output. Confirm the digest is unchanged.
- Stop at the manifest and prompt when ImageGen is unavailable or cannot receive every required reference. Do not create a placeholder raster.
- Do not use this skill for App Store, Google Play, or social marketing images; use `game-store-image-maker`. For a game screen, HUD, or menu contract, use Game Screen Foundry first and invoke this skill only for its individual raster jobs.

## Mandatory Creative Direction Gate

Before writing a raster job or calling ImageGen, require an approved creative direction for
the target game/asset family. Use `creative/creative-direction.md` or the project’s explicitly
named equivalent as the source of truth. A request that only says “make an asset” is not a
direction.

The brief must cover the asset purpose and audience, mood/style keywords, palette anchors and
avoid colors, shape/material/lighting language, camera/view and composition, references (or
explicit `none`), and must-have / must-not-have constraints. Keep unknown platform, pixel
size, or runtime details as `TBD`; do not infer them from the genre or filename.

- If the brief is absent, incomplete, or not marked approved, stop before job creation,
  ImageGen, PNG output, adoption, or regeneration. Inspecting inputs and drafting the brief is
  allowed, but visual production is not.
- If existing adopted assets or a supplied reference imply a direction, present that as a
  proposed summary and ask the user to confirm it; do not silently promote inference to an
  approved direction. After confirmation, record the brief and reference it in the job notes
  and registry entry.
- Every retry must preserve the approved direction unless the user explicitly approves a new
  direction. A failed QA result is not permission to improvise a new style.

## Run the workflow

1. Read repository instructions and inventory any supplied source images. Inspect every supplied local reference with `view_image` at original detail before writing the job. Allow `references: []` for a genuinely text-only job; if the user requires fidelity to a specific source, do not silently downgrade it to text-only when that source is missing.
2. Copy the text-only templates from `assets/project-template/` into the target project's chosen creative working directory. Keep all paths in committed manifests relative; never record secrets, credentials, or machine-local absolute paths.
3. Define each job in `raster-jobs.json`. Read [references/job-manifest.md](references/job-manifest.md) for the exact contract. Specify one final output path, exact dimensions, alpha policy, optional palette, and a required grid for sprite sheets.
4. Prepare the ImageGen request using [references/imagegen-and-visual-qa.md](references/imagegen-and-visual-qa.md). State the target dimensions, transparent/opaque requirement, reference invariants, cell order, and forbidden additions. Do not ask ImageGen to invent details that the brief marks as immutable.
5. Generate one asset per call unless ImageGen must preserve a single coherent sprite sheet. Include all required source images through the supported reference-image mechanism. Save the returned original directly at a new declared candidate output path without raster processing; never overwrite a previously accepted file.
6. Run the deterministic checks:

   ```bash
   python3 /path/to/game-raster-asset-pipeline/scripts/inspect_raster.py \
     --manifest path/to/raster-jobs.json --asset hero-idle-sheet
   ```

   The inspector reads PNG bytes but never writes to the image. It reports SHA-256 and checks exact dimensions, alpha policy, palette tolerance, declared grid geometry, occupied cells, and cell-edge gutters. Occupancy is explicit: alpha for transparent sheets or background-color comparison for opaque sheets. A nonzero exit means regenerate; do not repair the pixels.
7. Inspect each candidate with `view_image` at original detail. For transformations, compare against every reference and apply the checklist in [references/imagegen-and-visual-qa.md](references/imagegen-and-visual-qa.md). Automated checks cannot establish character identity, silhouette fidelity, pose meaning, cell ordering, or icon legibility.
8. Record the prompt, reference paths, original ImageGen output, SHA-256 digest, deterministic check result, visual-QA notes, and decision in `imagegen-assets.json`. Read [references/registry-and-regeneration.md](references/registry-and-regeneration.md) for allowed states and regeneration rules.
9. Accept only when deterministic checks pass and visual QA explicitly passes. Preserve rejected generations only if repository policy permits. On regeneration, declare a new candidate path or version instead of overwriting the previous candidate. If the runtime project needs a separate installed path, copy the accepted PNG byte-for-byte and verify the digest again.

## Apply type-specific gates

### Faithful sprite sheets

- Preserve subject identity, proportions, costume/part layout, outline language, palette intent, view direction, and animation meaning from the reference.
- Declare row-major cell order in the prompt and manifest. Use alpha occupancy for transparent PNG sheets. Use background-color occupancy when the approved source/runtime contract requires an opaque solid background such as pure white. Keep fixed cell dimensions and an unoccupied gutter in either mode.
- Reject merged frames, reordered poses, duplicate/missing frames, clipped silhouettes, inconsistent scale or ground line, and invented accessories even when structural checks pass.
- Generate the whole sheet in one ImageGen call when cross-frame consistency matters. Do not generate cells separately and composite them.

### Individual game assets

- Declare the runtime role, camera/view, silhouette, anchor, target dimensions, transparency, and required empty margin.
- Reject unexplained shadows, backgrounds, text, extra props, or lighting that conflicts with the game's established art direction.
- Keep separate runtime responsibilities as separate generated assets. Do not bake labels, counters, or mutable state into a raster unless the game specification owns that text in the asset.

### App icons

- Generate at the final requested square dimensions and declare whether the delivery target forbids alpha. Default to `transparency: "forbidden"` for store-ready icon files unless the target repository states otherwise.
- Preserve the approved hero symbol and brand colors. Reject tiny text, thin details, misleading badges, transparency when forbidden, and a composition that fails at thumbnail size.
- Produce each materially different icon size with ImageGen when exact pixels are required. Do not downsample a master within this workflow.

## Report the outcome

Return the accepted file paths and dimensions, manifest and registry paths, deterministic check result, visual-QA decision, digest verification, and any rejected or blocked jobs. State clearly when work stopped before raster generation because ImageGen or a required reference was unavailable.
