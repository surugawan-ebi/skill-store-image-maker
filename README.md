# Game Store Image Maker Skill

Create App Store and Google Play promotional image plans for mobile games, including screenshot sequences, Google Play feature graphics, Japanese/English copy, editable prompt packs, and QA checklists.

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
- Plans the first three screenshots as a mini-funnel: hook, core loop, differentiator.
- Produces per-image art direction, copy, prompts, and negative prompts.
- Keeps production work editable with a `materials/`, `working/`, and `exports/` project structure.
- Includes platform guardrails for App Store and Google Play image assets.

The skill is designed to avoid common store-image failures: fake gameplay, unsupported claims, tiny unreadable text, copied competitor layouts, misleading rewards, and generic device mockup templates.

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

MIT
