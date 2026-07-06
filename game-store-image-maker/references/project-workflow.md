# Project Workflow

Use a project folder whenever the user wants editable, repeatable store-image production rather than a one-off prompt.

## Recommended Folder Structure

```text
[game-slug]-store-images/
  materials/
    brief.md
    asset-inventory.md
    source/
      icons/
      gameplay/
      brand/
      references/
  working/
    shot-plan.md
    copy-bank.md
    prompt-pack.md
    qa-notes.md
    drafts/
  exports/
    app-store/
    google-play/
    manifest.md
```

## Folder Roles

- `materials/`: source of truth. Keep briefs, game specs, source screenshots, icons, logos, brand files, and competitor references here. Do not overwrite original captures.
- `materials/source/gameplay/`: clean gameplay screenshots or video frames. Use descriptive names such as `core-loop-01.png`, `win-moment-01.png`, or `upgrade-screen-01.png`.
- `working/`: editable strategy and generation files. Put shot plans, copy options, prompt packs, draft notes, and QA notes here.
- `working/drafts/`: generated or manually composed drafts that are not final.
- `exports/`: final handoff only. Put upload-ready images, final prompt packs, and a manifest of dimensions, source files, and QA status here.

## Operating Rules

1. Preserve all originals under `materials/source/`.
2. Write assumptions into `materials/brief.md` or `working/shot-plan.md`, not only in chat.
3. Keep every generated image traceable to a base capture, prompt, and copy line.
4. Use `working/` for iterations so the user can tweak copy, order, dimensions, and prompts.
5. Export only files that pass QA and are intended for store upload or handoff.
6. For each export batch, update `exports/manifest.md`.

## Naming

Use names that sort in store order:

```text
appstore-iphone-01-hook.png
appstore-iphone-02-core-loop.png
appstore-iphone-03-differentiator.png
googleplay-phone-01-hook.png
googleplay-feature-graphic-v01.png
```

For drafts, include version numbers:

```text
working/drafts/01-hook-v01.png
working/drafts/01-hook-v02.png
```

## Output Manifest

Every export batch should include:

- file name
- store target
- dimensions
- source gameplay capture
- headline/copy
- prompt file or prompt section
- QA result
- notes for manual upload

## When To Create The Structure

Create it when the user asks to:

- make multiple App Store or Google Play images
- iterate on visual direction
- keep prompts and copy editable
- create upload-ready exports
- hand work to another AI, designer, or image tool

For a quick critique or copy brainstorm, a folder is optional.
