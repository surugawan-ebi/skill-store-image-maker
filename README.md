# Game Store Image Maker Skill

Create App Store, Google Play, and Instagram promotional image plans for mobile games, including screenshot sequences, Google Play feature graphics, Instagram feed/Story/Reel creatives, Japanese/English copy, editable prompt packs, and QA checklists.

This repository contains a portable Codex/Claude-style skill:

```text
game-store-image-maker/
  SKILL.md
  agents/openai.yaml
  references/
  assets/project-template/
```

## What This Skill Does

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

Use ImageGen for every new or edited raster deliverable. If ImageGen is unavailable, stop after the brief, shot plan, copy, and prompt pack; do not substitute a programmatic image compositor or a different image generator for the final raster assets. Existing captures and approved exports may be copied unchanged for documentation or handoff.

## Install

### Codex

Copy the skill folder into your Codex skills directory:

```bash
cp -R game-store-image-maker ~/.codex/skills/
```

Then invoke it with:

```text
Use $game-store-image-maker to create store screenshot concepts and image prompts for my mobile game.
```

### Claude or Other Agents

Point the agent at:

```text
game-store-image-maker/SKILL.md
```

For project-based work, also provide:

```text
game-store-image-maker/references/project-workflow.md
game-store-image-maker/assets/project-template/
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

## Repository Validation

Run:

```bash
python3 scripts/validate_skill.py game-store-image-maker
```

The validator checks the skill frontmatter, required metadata, referenced files, and basic project-template files without external Python dependencies.

## License

The source code and planning-document templates are MIT licensed. Raster files under `examples/minicalog/` are excluded from the MIT grant and are provided only for workflow documentation; see the [example asset notice](./examples/minicalog/ASSET-NOTICE.md).
