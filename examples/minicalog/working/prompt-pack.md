# Prompt Pack

These prompts are for future ImageGen revisions. The bundled JPEGs are an immutable snapshot of an already completed production run and are preserved as documentation. Do not recreate or edit them with a programmatic compositor; use ImageGen for any new raster version.

## 01 Hook

- Goal: Show that the collection can be scanned visually.
- Base image: `materials/source/gameplay/02-grid-collection.jpg`
- Canvas: 1080x1920 and 1290x2796 portrait
- Copy: `コレクションをひと目で`
- Preserve: exact screenshot UI, car photos, tabs, search, filter, bottom navigation
- May enhance: subtle dark background, red/gold/blue accent lines, soft shadow around screenshot
- Must avoid: fake cars, fake UI, extra badges, download CTA, ranking claims

Prompt:
"""
Create a portrait mobile app store screenshot using the provided Minicalog collection grid screenshot as the exact source UI. Preserve the real app screen and visible car photos. Place the screenshot as the hero on a dark premium background with subtle red, gold, and blue accents inspired by the app UI. Add a large readable Japanese headline "コレクションをひと目で" and smaller subcopy "写真つきで、持っているトミカを整理" above the screenshot. Do not invent UI, cars, rankings, store badges, or download calls to action.
"""

Negative prompt:
"""
fake gameplay, fake UI, fake car models, unreadable text, tiny captions, copied competitor layout, app store badges, download CTA, ranking claims, excessive clutter, cropped important UI, distorted screenshots
"""

## 02 Core Loop

- Base image: `materials/source/gameplay/01-detail-owned.jpg`
- Copy: `持ってる・ほしいを記録`

Prompt:
"""
Create a portrait mobile app store screenshot using the provided Minicalog detail screen as the exact source UI. Preserve the toy photo, release date, status buttons, and tags. Use a dark premium background with a soft red/blue accent and a large Japanese headline "持ってる・ほしいを記録" plus subcopy "詳細画面からワンタップで更新". Do not invent sync, backup, account, ranking, or official-affiliation claims.
"""

## 03 Discovery

- Base image: `materials/source/gameplay/04-tag-list.jpg`
- Copy: `タグで探しやすい`

Prompt:
"""
Create a portrait mobile app store screenshot using the provided Minicalog tag list screenshot as the exact source UI. Preserve the grouped list, search, filter, and navigation. Add the headline "タグで探しやすい" and subcopy "シリーズや作品ごとにすばやく表示" in large readable Japanese type. Use subtle blue and gold accents that match the UI. Do not cover the list content with text.
"""
