# Store Asset Specs

Use this as a production guardrail, not as a substitute for final official verification. Store requirements can change. For upload-ready work, re-check:

- Apple App Store Connect screenshot specs: https://developer.apple.com/help/app-store-connect/reference/app-information/screenshot-specifications
- Apple App Store Connect upload guide: https://developer.apple.com/help/app-store-connect/manage-app-information/upload-app-previews-and-screenshots/
- Google Play preview assets: https://support.google.com/googleplay/android-developer/answer/9866151

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
| Text coverage | Keep overlays under 20% when Google Play is in scope |

Always preserve a clean gameplay capture separately. Do not flatten the only source file with captions.
