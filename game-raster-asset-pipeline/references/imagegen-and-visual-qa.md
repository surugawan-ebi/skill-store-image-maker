# ImageGen Request and Visual QA

## Prompt contract

Include these sections in the saved prompt:

1. `Deliverable`: kind, exact width and height, PNG, alpha policy, and either transparent or exact solid-background treatment.
2. `References`: role of every attached image and which source is authoritative when they conflict.
3. `Must preserve`: identity, silhouette, proportions, palette intent, topology/parts, camera, and any cell-specific poses.
4. `May change`: only the transformations the user requested, such as rendering a supplied character in the established pixel-art language.
5. `Layout`: canvas occupancy, transparent margin, grid rows/columns, row-major cell mapping, ground line, and view direction.
6. `Must not include`: background when transparent, text, watermark, extra objects, duplicated/missing frames, fake UI, unrequested shadows, or cropped content.

For a reference transformation, ask for faithful conversion rather than a loose interpretation. Do not substitute verbal reconstruction when the tool can receive the source image.

## Sprite-sheet request checklist

- Name every cell in row-major order, for example `0 idle front`, `1 walk front A`, `2 walk front B`.
- State the exact cell dimensions and total grid dimensions.
- Require one centered subject per occupied cell and unoccupied gutters. For background-color occupancy, name the exact solid color such as pure white.
- Require consistent character scale, pivot, ground line, lighting, outline weight, and palette across cells.
- State whether mirroring is allowed. Do not assume left/right frames may be mirrored.

## Visual QA

Inspect the generated file with `view_image` at original detail. For transformations, reopen every reference at original detail and compare directly.

Check all assets for:

- subject identity and silhouette;
- exact requested content with no additions or omissions;
- coherent palette, outline, lighting, and texture language;
- clean edges at native size;
- absence of unwanted text, watermark, background, shadow, or clipping;
- intended empty margins and anchor/pivot placement.

Additionally check sprite sheets for:

- exact frame count and row-major cell ordering;
- correct pose or view in each cell;
- consistent scale, ground line, facing direction, and spacing;
- no merged, duplicated, missing, or partially clipped frames;
- no visible content crossing cell boundaries.

Additionally check app icons for:

- one immediately readable focal symbol;
- correct brand identity at native size and thumbnail size;
- no tiny text, delicate edge details, misleading badge, or accidental border;
- opaque corners when alpha is forbidden.

Record a concrete pass/fail note. `Looks good` is insufficient; mention the preserved invariants and any observed deviation.
