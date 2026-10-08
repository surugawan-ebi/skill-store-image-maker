# Registry and Regeneration

Track every candidate in `imagegen-assets.json`. The registry is provenance and QA state, not a place to embed image bytes or private prompts.

## Entry contract

Each entry records:

- `asset_id` and `kind`, matching `raster-jobs.json`;
- relative `references`, `prompt_file`, and `output_path`;
- ImageGen as `generator` and a non-secret tool/model label when available;
- `generated_at` as an ISO 8601 timestamp;
- `sha256` of the untouched output;
- optional relative `installed_path` and `installed_sha256` after byte-for-byte runtime placement;
- exact `width` and `height` measured from the file;
- `deterministic_qa`: `pending`, `passed`, or `failed` plus concise issues;
- `visual_qa`: `pending`, `passed`, or `failed` plus concrete notes;
- `decision`: `candidate`, `accepted`, `rejected`, or `blocked`;
- `supersedes` when a regeneration replaces an earlier candidate.

An entry may be `accepted` only when both QA fields are `passed` and the recorded digest matches the file at `output_path`. When `installed_path` is set, `installed_sha256` must match the accepted digest.

## Regenerate instead of repairing

Regenerate when any of these occurs:

- wrong dimensions or file format;
- required transparency missing or forbidden alpha present;
- palette limits exceeded;
- grid geometry, occupancy, or gutter failure;
- reference identity, proportions, silhouette, or requested details drift;
- wrong frame count, order, pose, scale, facing, ground line, or clipping;
- unwanted background, text, watermark, shadow, or extra object;
- app icon fails at thumbnail size.

Change only prompt instructions that correspond to observed failures. Keep accepted constraints stable. Create a new registry entry, link it through `supersedes`, and rerun both QA gates. Never post-process the previous PNG.

## Digest verification

Use a read-only digest command appropriate to the platform, for example:

```bash
shasum -a 256 generated-assets/hero-idle-sheet.png
```

Verify the digest again after placing an accepted output. A changed digest means the accepted pixels were not preserved.
