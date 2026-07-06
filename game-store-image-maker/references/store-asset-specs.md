# Store and Social Asset Specs

Use this as a production guardrail, not as a substitute for final official verification. Store requirements can change. For upload-ready work, re-check:

- Apple App Store Connect screenshot specs: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
- Apple App Store Connect upload guide: https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/
- Google Play preview assets: https://support.google.com/googleplay/android-developer/answer/9866151
- Meta Ads Guide: https://www.facebook.com/business/ads-guide

Checked: 2026-07-07.

## Apple App Store

- Screenshots: upload 1-10 images per supported platform/device size.
- Formats: `.jpeg`, `.jpg`, `.png`.
- App previews: optional; up to 3 per supported device size and language. App previews appear before screenshots.
- If the UI is the same across sizes/localizations, Apple allows high-resolution required screenshots to scale down to smaller device sizes.
- Production work should target the highest required device classes first, then derive other sizes as needed.

Common iPhone portrait targets from the official screenshot table:

| Display class | Portrait sizes accepted | Landscape sizes accepted |
| --- | --- | --- |
| 6.9 inch | 1260x2736, 1290x2796, 1320x2868 | 2736x1260, 2796x1290, 2868x1320 |
| 6.5 inch | 1284x2778, 1242x2688 | 2778x1284, 2688x1242 |
| 6.3 inch | 1179x2556, 1206x2622 | 2556x1179, 2622x1206 |
| 6.1 inch | 1170x2532, 1125x2436, 1080x2340 | 2532x1170, 2436x1125, 2340x1080 |

Creative guidance:

- Keep the screenshot credible as the product experience.
- Use captions and design treatments to explain, not to obscure gameplay.
- Do not rely on tiny UI text to carry the pitch.
- Avoid claims that may conflict with App Review, age rating, or legal metadata.

## Google Play

### Feature Graphic

- Required for publishing a store listing.
- Format: JPEG or 24-bit PNG, no alpha.
- Size: 1024x500.
- It may be used as the cover for a preview video and in promotional surfaces.
- Use the feature graphic to convey the game experience, core value, context, or story.
- Avoid fine details and avoid prominent duplicated app-icon branding.
- Keep colors related to the icon and in-game style, but avoid pure white, black, or dark gray as dominant backgrounds.
- Localize branding text where appropriate.

### Screenshots

- Minimum: 2 screenshots across device types to publish a store listing.
- Format: JPEG or 24-bit PNG, no alpha.
- Minimum dimension: 320 px.
- Maximum dimension: 3840 px.
- The long side must not be more than twice the short side.
- For recommendation eligibility in game surfaces, provide at least 3 landscape screenshots at 16:9 with minimum 1920x1080, or 3 portrait screenshots at 9:16 with minimum 1080x1920.
- Screenshots should depict actual in-game experience and core content.
- Do not show people interacting with a device unless off-device interaction is core to gameplay.
- Stylized screenshots split across multiple images are allowed, but prioritize visible UI/gameplay in the first three screenshots.
- Taglines should be used only when needed and should not occupy more than 20% of the image.
- Do not include Google Play performance, ranking, accolades, user testimonials, price, or promotional claims.
- Avoid terms such as "Best", "#1", "Top", "New", "Discount", "Sale", or "Million Downloads".
- Avoid calls to action such as "Download now", "Install now", "Play now", or "Try now".
- Avoid small text, busy text backgrounds, notification clutter, carrier names, and partially depleted status indicators.

## Cross-Store Practical Defaults

Use these when the user has no production target yet:

| Deliverable | Default |
| --- | --- |
| Portrait game screenshots | 1080x1920 concept, then upscale/resize to target store size |
| Landscape game screenshots | 1920x1080 concept |
| Google Play feature graphic | 1024x500 |
| App Store iPhone production portrait | Start with 1290x2796 or 1320x2868 if supported by the asset pipeline |
| Instagram feed app-promo post | 1080x1350, 4:5 |
| Instagram square fallback | 1080x1080, 1:1 |
| Instagram Story/Reel app-promo creative | 1080x1920, 9:16 |
| Text coverage | Keep overlays under 20% when Google Play is in scope |

## Instagram Promotion

Use Instagram exports for marketing posts that promote the app outside the stores. Do not treat these as store screenshots; they can be more campaign-like, but gameplay accuracy still matters.

| Placement | Default size | Ratio | Use |
| --- | --- | --- | --- |
| Feed portrait / carousel | 1080x1350 | 4:5 | Default static app-promo post; strongest feed presence |
| Feed square / carousel fallback | 1080x1080 | 1:1 | Safer reuse across grids, thumbnails, and older layouts |
| Feed 3:4 | 1080x1440 | 3:4 | Optional phone-native vertical post when the user wants taller photo-like framing |
| Story / Reel | 1080x1920 | 9:16 | Full-screen vertical promo, teaser, or launch announcement |
| Landscape post | 1080x566 | 1.91:1 | Optional; use only when the game is naturally wide |

Instagram app-promo guidance:

- Prefer `1080x1350` for static feed posts and carousels unless the user needs square compatibility.
- Prefer `1080x1920` for Stories/Reels. Keep essential logo, CTA, and headline away from top and bottom UI overlay areas.
- For a carousel, keep all slides in the same ratio. Use slide 1 as the hook, slide 2 for gameplay, slide 3 for differentiator or reward.
- Organic Instagram posts may use CTA language such as "予約受付中" or "今すぐチェック", but paid ads should be checked against current Meta ad policies.
- Use canvas-first fitting when adapting store screenshots: brand-color background first, gameplay capture on top, app icon/title and one short hook in the empty space.
- Avoid making Instagram creatives that look like fake gameplay, fake reviews, fake rankings, or unsupported store badges.

## Size Mismatch Policy

When the source image does not match the final store size, default to a canvas-first composition:

1. Create the exact target-size canvas.
2. Fill the canvas with a simple brand or game-world background.
3. Place the source gameplay image on top and scale it proportionally.
4. Use empty space for short copy, visual accents, or background extension.
5. Do not stretch gameplay, UI, characters, icons, or text.
6. Do not crop key gameplay UI unless the user explicitly approves or the crop is clearly safe.

Use `contain-on-canvas` for most portrait-to-feature-graphic, landscape-to-portrait, and odd-ratio source images. Use `same-ratio-scale` only when the source and target share the same ratio. Use `safe-crop` only for nonessential edges.

Always preserve a clean gameplay capture separately. Do not flatten the only source file with captions.
