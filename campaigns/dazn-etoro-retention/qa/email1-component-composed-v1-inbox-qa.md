# Email 1 component-composed v1 inbox QA

Date: 2026-09-15

## Build

- Source: `DAZN-etoro-Germany-email-1-component-composed-v1.mjml`
- Compiled sendable: `DAZN-etoro-Germany-email-1-component-composed-v1.html`
- Compiler: repository `compile_mjml.js`, strict mode
- Compiled size: 47,577 bytes
- Compiled SHA-256: `8A1C3C28E87217AEE16FBA32F98295B76903BAEE2BC3916A7E68AE54B9A766C2`

## Responsive checks

The compiled file was rendered at 700, 640, 600, 480, 375, 320, 280, and 240 pixels.

| Width | Horizontal overflow | Cards | Card heights | Images loaded |
| ---: | :--- | ---: | :--- | ---: |
| 700 | No | 4 | 222, 222, 222, 222 | 7/7 |
| 640 | No | 4 | 220, 220, 220, 220 | 7/7 |
| 600 | No | 4 | 220, 220, 220, 220 | 7/7 |
| 480 | No | 4 | 250, 250, 250, 250 | 7/7 |
| 375 | No | 4 | 310, 310, 310, 310 | 7/7 |
| 320 | No | 4 | 358, 358, 358, 358 | 7/7 |
| 280 | No | 4 | 358, 358, 358, 358 | 7/7 |
| 240 | No | 4 | 500, 500, 500, 500 | 7/7 |

## Content checks

- The €20 first-deposit reward is explicitly marked as already applied.
- The DAZN coupon is the first actionable block and includes copy/use instructions for a two-month subscription.
- The 50% trading discount and six-month deposit mission are presented as future mission steps.
- The deposit CTA points to the agreed placeholder deep link: `https://www.etoro.com/deposit`.
- The deposit CTA is a compact content-width pill (243px in the tested desktop and mobile renders), not a full-width block.
- The custom co-branded header is present inside the email body: hosted white etoro logo and DAZN mark are grouped as a left-aligned lockup, with the desktop partnership label on the right. The shared BaseTemplate header remains hidden to avoid duplication.
- The DAZN and deposit links retain their tracking aliases.
- The current coupon remains `DAZN-XXXX-XXXX` for layout QA; production must inject the eligible user's issued coupon.
- The mission imagery now uses the supplied Bundesliga and international football marks for the first two steps, a polished Know Better medal for the trading discount, and the supplied FIBA cup mark for the six-month mission. The FIBA crop was cleaned to remove residual dark edge pixels. Both revised icons are transparent 256x256 PNGs, uploaded to S3, and loaded in responsive render QA. The displayed card icons remain 64px.
- Deterministic asset QA passed for both revised icons. The exact Creative Studio records are `know-better-medal-trading-discount-v3` (`f1a6ec8fcaf5082f7c7f498456be2625320f7940beba513928f6764d4523b767`) and `fiba-cup-six-months-v3` (`5490f1757b7851752592644fb01fa15bfe861997af24f00f49042654f3716aed`). The sendable HTML is synchronized locally at SHA-256 `BAD15ABAAC8954946220B9D0A051259EC478F4EE8046DDBE4CEC0DF4445B8606`.
- The current disclosure still contains internal approval language and is not a production approval. SFMC was not updated for this icon revision; no send, schedule, or activation was performed.
- Updated headline: `Get 2 Months of DAZN FREE + Up to €300 in Rewards!`.
- Updated opening paragraph uses the approved wording supplied for the €20 free share reward, DAZN coupon, trading discount, and six-month deposit mission.
- Added beginner-friendly section after the DAZN coupon and before the matchday missions:
  - New to investing? Good to know!
  - Start small and explore at your own pace:
  - Invest from €50 with fractional shares.
  - Pay zero commission on ETFs.*
  - Practice risk-free with a virtual portfolio.
  - Automatically copy experienced investors with CopyTrader™.*
  - Join a regulated, Nasdaq-listed platform founded in 2007.
- Linked `fractional shares` to the supplied eToro stocks discovery page, `ETFs` to the supplied eToro ETF discovery page, and `CopyTrader™` to the supplied eToro people discovery page. All three links were verified in the rendered HTML.
- Proofread the supplied beginner copy without changing its context or claims; the two supplied asterisks remain.
- The current SFMC-native content build (including the realistic Know Better medal, realistic FIBA cup, and revised investor intro) is 46,981 bytes and hashes to `e475386a3d206ce7d60e3a3f6d63dfa8b6d991f32f41ae42e84f42f027c41ead`; this hash must be explicitly confirmed before any SFMC write.
- Fresh local browser render readback confirmed the complete email, both revised icons, all benefit links, the deposit CTA, and the disclaimer are present. Structural QA found 5 anchors with 0 missing `_blank` targets, 7 images with 0 missing alt/display checks, and 4 equal-height mission cards in the documented responsive renders.
- Final SFMC production dry-run completed read-only on 2026-09-15: existing Code Snippet `419416` and HTML Controller `419417` were found with the expected asset types, and `MarketCampaigns` tag `755` was read back. Existing content SHA-256 was `2c7e7e5c98609dd4b936dbd4c75349b98063d367a294f352a0f5fcafa997351c`; candidate native-content SHA-256 is `e475386a3d206ce7d60e3a3f6d63dfa8b6d991f32f41ae42e84f42f027c41ead`.
- The previous approved SFMC overwrite remains the production reference; this DAZN-style icon revision is local/S3 only and awaits a separate exact-hash confirmation if it is to replace the current SFMC content.
- The two supplied asterisks are retained in the customer-facing copy. Footnote wording was not supplied and remains a compliance/legal follow-up.

## Result

PASS for local inbox structure and responsive rendering. Pending human copy/compliance approval, footnote text for the two asterisked claims, live coupon-field binding, and a fresh SFMC preview/test-send. The new medal/trophy build is local and S3-ready; SFMC still contains the previously uploaded build until separately authorized.
