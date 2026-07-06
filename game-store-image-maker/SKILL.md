---
name: game-store-image-maker
description: Create App Store and Google Play promotional images for mobile game listings, including screenshot sets, feature graphics, creative direction, Japanese/English taglines, ASO-oriented shot plans, and image-generation prompts from gameplay captures, app icons, brand assets, and game briefs. Use when Codex or Claude needs to plan, critique, generate, localize, or QA mobile game store visuals while respecting store asset requirements and avoiding misleading or competitor-copying designs.
---

# Game Store Image Maker

## Overview

Turn a game brief plus base gameplay images into store-listing visuals that make the gameplay promise obvious in the first second. Prioritize actual in-game experience, readable hooks, strong first-three screenshots, and platform-safe copy over generic advertising decoration.

## Workflow

1. Create or identify the project workspace. Use `references/project-workflow.md` and, when useful, copy `assets/project-template/` so source inputs, working drafts, and exports stay separate.
2. Collect inputs. If the user has not provided enough detail, use `references/input-brief-template.md` as the intake format and save the completed brief under `materials/`.
3. Identify the target deliverable: App Store screenshots, Google Play screenshots, Google Play feature graphic, cross-store concept board, prompt pack, localization pass, or QA review.
4. If output dimensions, upload readiness, or platform compliance matters, read `references/store-asset-specs.md`. For production upload work, verify the latest official Apple and Google specs before final export.
5. Analyze the base images and brief internally:
   - genre, camera, core loop, win condition, progression, player fantasy
   - target player desire, anxiety, curiosity, and download trigger
   - strongest gameplay proof visible in screenshots
   - icon colors, UI style, character/world motifs, brand constraints
   - claims that must not be invented
6. Build a screenshot narrative before writing prompts. Use the first three assets to answer:
   - What is this game?
   - Why is it satisfying?
   - What makes it different enough to try?
7. Save editable planning files in `working/`, then write final upload or handoff files to `exports/` only after QA:
   - concise creative diagnosis
   - asset list and sizes
   - screenshot sequence table
   - per-image art direction
   - image-generation prompt and negative prompt
   - copy/tagline options
   - QA checklist

## Creative Rules

- Make the game screen the hero. Use generated art, effects, characters, or props only to frame or amplify true gameplay.
- Do not create fake gameplay, fake UI, fake rewards, fake rankings, or unsupported social proof.
- Do not copy competitor screenshots, captions, characters, UI, or composition. Borrow only category-level patterns.
- Keep overlay text short. One clear promise per image is usually enough.
- Use large, localized, high-contrast typography. For Japanese, favor compact punch lines over translated English rhythm.
- Treat the first three screenshots as a connected mini-funnel, not isolated posters.
- Keep store visuals legible at phone thumbnail size. Fine detail, tiny text, and busy backgrounds usually fail.
- Avoid generic device mockup templates unless they clarify the game. For Google Play games, prioritize actual in-game experience.
- If using AI image generation, preserve gameplay accuracy and use the provided captures as the visual source of truth.
- When source images and export sizes differ, create the target-size canvas first, fill it with a simple brand-colored background, then place the source gameplay image on top without distortion. Use padding, background extension, or designed empty space before cropping key gameplay UI.

## Screenshot Sequence

Default sequence for a 5-8 image set:

1. Hook: the clearest, most exciting gameplay state plus the strongest promise.
2. Core loop: show what the player repeatedly does.
3. Differentiator: mechanic, theme, control, challenge, or fantasy that separates the game.
4. Progression: upgrades, collections, levels, builds, story, or unlocks.
5. Reward: win moment, combo, loot, transformation, score, or satisfying completion.
6. Mode depth: events, bosses, multiplayer, puzzles, customization, or daily content.
7. Social or competitive proof, only if truly in the game.
8. World/brand closer: a memorable scene that reinforces the icon and store identity.

For 3 images, use Hook / Core Loop / Differentiator. For a single feature graphic, compress the hook and differentiator into one clean scene without small UI.

## Output Format

When planning a full set, use this table:

| Asset | Store | Size / ratio | Base image | User promise | Composition | Copy | Prompt notes | QA notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

For each image-generation prompt, include:

- target canvas and platform
- exact base image(s) to preserve
- size-fitting method: contain-on-canvas, safe crop, same-ratio scale, or background extension
- foreground gameplay moment
- background treatment
- typography text and placement
- color palette tied to the icon/game UI
- allowed enhancements
- prohibited changes
- export notes

## References

- Read `references/project-workflow.md` when setting up or updating a game-specific working folder.
- Read `references/input-brief-template.md` when the user needs an intake sheet or when required information is missing.
- Read `references/store-asset-specs.md` when producing upload-ready dimensions or platform guardrails.
- Read `references/design-playbook.md` when choosing composition patterns, sequence strategy, or prompt phrasing.

## Assets

- Use `assets/project-template/` as a starter folder for reusable game store image projects. Copy it into the user's requested working location and rename the root folder for the game.
