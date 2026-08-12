# Game Image Skills

This repository contains two portable Codex/Claude-style skills:

- `game-store-image-maker`: create App Store, Google Play, and Instagram promotional image plans for mobile games.
- `game-raster-asset-pipeline`: generate sprite sheets, individual game assets, and app icons with ImageGen, then run immutable-output QA.

```text
game-store-image-maker/
  SKILL.md
  agents/openai.yaml
  references/
  assets/project-template/
game-raster-asset-pipeline/
  SKILL.md
  agents/openai.yaml
  scripts/inspect_raster.py
  references/
  assets/project-template/
```

## Game Raster Asset Pipeline

The raster pipeline turns optional references and a text job manifest into exact-size ImageGen outputs. It validates PNG dimensions, transparency, palette constraints, and sprite-grid occupancy/gutters using either alpha or a declared solid background color, without editing the generated pixels. Visual QA uses supplied references to check identity, silhouette, pose meaning, cell ordering, and thumbnail legibility. Any failed gate requires regeneration rather than programmatic repair.

## What Game Store Image Maker Does

- Turns gameplay captures, app icons, and a game brief into store screenshot concepts.
- Plans Instagram app-promo images for feed posts, carousels, Stories, and Reels.
- Plans the first three screenshots as a mini-funnel: hook, core loop, differentiator.
- Produces per-image art direction, copy, prompts, and negative prompts.
- Keeps production work editable with a `materials/`, `working/`, and `exports/` project structure.
- Includes platform guardrails for App Store and Google Play image assets.
- Handles source/export size mismatches with a canvas-first layout: create the target-size background first, then place gameplay captures on top without distortion.

The skill is designed to avoid common store-image failures: fake gameplay, unsupported claims, tiny unreadable text, copied competitor layouts, misleading rewards, and generic device mockup templates.

## Real Project Example

[`examples/minicalog/`](./examples/minicalog/) contains a documented case study built from real Minicalog app captures. It includes the source screenshots, brief, shot plan, copy bank, ImageGen prompt pack, QA notes, and selected App Store / Google Play / Instagram results.

| Source capture | Store result |
| --- | --- |
| ![Minicalog collection source capture](./examples/minicalog/materials/source/gameplay/02-grid-collection.jpg) | ![Minicalog App Store hook image](./examples/minicalog/exports/app-store/01-hook.jpg) |

The example demonstrates the intended boundary: the app screenshot remains the source of truth, while the surrounding composition explains the product promise without inventing UI or features. The bundled images are documentation examples, not reusable stock assets; see the [asset notice](./examples/minicalog/ASSET-NOTICE.md).

## Raster Asset Policy

Use ImageGen for every new or edited raster deliverable. Do not substitute a programmatic image compositor or a different image generator for final raster assets. If ImageGen is unavailable, Game Store Image Maker stops after the brief, shot plan, copy, and prompt pack; Game Raster Asset Pipeline stops after the job manifest and prompt. Existing captures and accepted outputs may be copied byte-for-byte for documentation or handoff.

## Install

### Codex

Copy the skill folder into your Codex skills directory:

```bash
cp -R game-store-image-maker ~/.codex/skills/
cp -R game-raster-asset-pipeline ~/.codex/skills/
```

Then invoke it with:

```text
Use $game-store-image-maker to create store screenshot concepts and image prompts for my mobile game.
Use $game-raster-asset-pipeline to generate and validate a sprite sheet from my references.
```

### Claude or Other Agents

Point the agent at:

```text
game-store-image-maker/SKILL.md
game-raster-asset-pipeline/SKILL.md
```

For project-based work, also provide:

```text
game-store-image-maker/references/project-workflow.md
game-store-image-maker/assets/project-template/
game-raster-asset-pipeline/references/job-manifest.md
game-raster-asset-pipeline/assets/project-template/
```

## Recommended Project Workflow

For each game, copy the template:

```bash
cp -R game-store-image-maker/assets/project-template my-game-store-images
```

Then organize work like this:

```text
my-game-store-images/
  materials/   source brief, gameplay captures, app icon, brand assets
  working/     shot plans, copy options, prompts, drafts, QA notes
  exports/     final handoff files and manifest
```

For a raster-asset batch, copy the text-only manifest and registry template:

```bash
cp -R game-raster-asset-pipeline/assets/project-template my-game-raster-assets
```

## Repository Validation

Run:

```bash
python3 scripts/validate_skill.py game-store-image-maker
python3 scripts/validate_skill.py game-raster-asset-pipeline
python3 game-raster-asset-pipeline/scripts/inspect_raster.py --self-test
```

The validator checks the skill frontmatter, required metadata, referenced files, and basic project-template files without external Python dependencies.

## License

The source code and planning-document templates are MIT licensed. Raster files under `examples/minicalog/` are excluded from the MIT grant and are provided only for workflow documentation; see the [example asset notice](./examples/minicalog/ASSET-NOTICE.md).
