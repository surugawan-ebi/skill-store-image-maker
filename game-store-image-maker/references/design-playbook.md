# Design Playbook

Use this when choosing the visual strategy, screenshot order, or image-generation prompts.

## What Store Game Images Need To Do

The store image is not a poster alone. It is a fast explanation of gameplay, genre, promise, and trust. Good game store visuals usually combine:

- a real gameplay moment
- one short user benefit or action phrase
- high-contrast focal point
- icon-consistent color palette
- large readable type
- progression across the first three screenshots
- proof that the game is playable, not just attractive

## Sequence Archetypes

### Puzzle / Match / Brain

1. Show the satisfying board state or puzzle action.
2. Show the rule or input: match, draw, merge, sort, solve, aim.
3. Show the twist: obstacles, boosters, physics, time pressure, hidden clues.
4. Show rewards, levels, collections, or daily challenges.

Copy angles: "つなげて連鎖", "一手で逆転", "ひらめきで突破", "毎日新しいパズル".

### Hypercasual / Arcade

1. Show the one-touch action with motion.
2. Show danger or obstacle.
3. Show collection, combo, or near-miss thrill.
4. Show skins, levels, or score chase.

Copy angles: "かわして進め", "タイミング勝負", "集めて強化", "止まらない爽快感".

### RPG / Action / Battle

1. Show combat impact or boss scale.
2. Show team, character skill, or weapon fantasy.
3. Show growth: gear, unlocks, rarity, build.
4. Show story world, event, guild, or PvP if real.

Copy angles: "編成で勝つ", "必殺技を叩き込め", "仲間を育てる", "巨大ボスに挑め".

### Simulation / Tycoon / City

1. Show the finished fantasy: city, shop, farm, park, room, island.
2. Show the action: build, merge, serve, harvest, decorate.
3. Show expansion and upgrades.
4. Show characters, customers, collections, or events.

Copy angles: "理想の街をつくる", "育てて広げる", "お店を大きく", "自由にデコる".

### Cozy / Narrative / Collection

1. Show emotional world or main character.
2. Show interaction: talk, decorate, discover, collect.
3. Show progression or story reveal.
4. Show seasonal/event variety.

Copy angles: "小さな物語を集める", "自分だけの部屋へ", "癒やしの時間", "今日も会いに行く".

## Composition Patterns

### Gameplay Hero

Use one real screenshot as the center. Add a large caption above or below, then a small controlled effect that points to the action. Best when the gameplay is visually self-explanatory.

Prompt skeleton:

```text
Create a [platform/size] mobile game store screenshot using [base image] as the exact gameplay source. Preserve the game UI and visible mechanics. Make the gameplay board the hero, with a large readable [language] headline "[copy]" occupying no more than [limit]% of the image. Use [palette] derived from the app icon. Add subtle motion streaks, glow, or shape accents only where they clarify [action]. Do not invent characters, rewards, UI, rankings, or store badges. Export as [format].
```

### Split Moment

Show before/after or problem/solution in one image. Use a diagonal, card, or layered cut only if it clarifies the mechanic. Avoid generic left/right templates.

### Panoramic Set

Create a connected background across 3 screenshots, but keep each screenshot useful alone. This works for worlds, runners, RPG, and simulation games. Put the clearest gameplay in screenshot 1 or 2.

### Character Plus Gameplay

Use character art to draw attention, but keep the in-game screen visible enough to explain play. Do not let character art turn the asset into a misleading key visual.

### Feature Graphic

Use fewer words and larger shapes than screenshots. The feature graphic often appears with overlays or video controls, so keep the center/focal area clean and avoid tiny gameplay UI. It should feel like an extension of the icon and game world, not a duplicate of the icon.

## Japanese Copy Rules

- Use short action verbs and concrete nouns.
- Prefer 5-12 Japanese characters for the main phrase when possible.
- Avoid long explanations, weak abstractions, and literal English translation.
- Use punctuation sparingly.
- Use small secondary copy only when the main phrase would otherwise be unclear.
- Do not use unsupported superlatives such as "No.1", "最高", "大人気", or "今だけ" unless legally verified and platform-safe.
- Avoid direct CTAs when Google Play is in scope.

Examples by purpose:

| Purpose | Japanese directions |
| --- | --- |
| Core action | "なぞって消す", "積んで突破", "狙って一撃" |
| Reward | "連鎖が気持ちいい", "宝箱を解放", "一手で逆転" |
| Progression | "育てて強く", "街が広がる", "仲間を集める" |
| Challenge | "難問に挑め", "反射神経で勝つ", "ボスを崩せ" |
| Cozy | "毎日少しずつ", "自分だけの庭", "物語を集める" |

## Prompt Pack Format

For each asset, output:

```markdown
### [Asset name]
- Goal:
- Base image:
- Canvas:
- Copy:
- Composition:
- Style:
- Preserve:
- May enhance:
- Must avoid:

Prompt:
"""
[full image prompt]
"""

Negative prompt:
"""
fake gameplay, fake UI, unreadable text, tiny captions, copied competitor layout, app store badges, download CTA, ranking claims, excessive clutter, cropped important UI, distorted characters, inconsistent icon colors
"""
```

## QA Checklist

- Does screenshot 1 make the genre and action clear without reading the description?
- Do the first three screenshots avoid repeating the same promise?
- Is every claim visible in the game or supported by the brief?
- Is overlay text readable at thumbnail size?
- Is the text short enough for localization?
- Is gameplay still visible after decoration?
- Are icon, UI, and store images visually connected?
- Are forbidden ranking, price, promo, testimonial, or CTA claims absent?
- Are competitor characters, layouts, and taglines avoided?
- Are source captures preserved separately from edited exports?
