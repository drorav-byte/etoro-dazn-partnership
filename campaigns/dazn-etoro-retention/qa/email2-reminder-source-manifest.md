# Email 2 reminder — source and QA manifest

Date: 2026-09-23

## Source manifest

- Headpic: new image-only composite stored as `assets/dazn-email-2-headpic-v3.png` at 1280x560. It uses supplied football and Formula 1 imagery over a restrained editorial sports background, with no baked-in text or logo strip. Public S3 hosting is still required before production.
- etoro logo: existing official wordmark with its source background removed non-destructively as `assets/etoro-logo-official-transparent.png`, so the native header background shows through.
- DAZN logo: supplied boxed white logo copied locally as `assets/dazn-boxed-logo-white.png` and rendered as a separate responsive header image.
- Product section: text-only Know Better cards with linked product names. No invented platform UI or product screenshot is used.
- Coupon: layout placeholder `DAZN-XXXX-XXXX` with `data-coupon-field="DAZN_CouponCode"`; production must inject the issued, non-expired code and suppress the reminder after verified DAZN redemption.

## Component audit

- Header/headpic: Email 2 has a co-branded etoro/DAZN header and a 1280x560 football-and-F1 headpic shown edge-to-edge without a caption, border or baked-in copy.
- Reminder module: short paragraph with the dynamic coupon inline and one `Use it on DAZN` hyperlink; no large coupon card. The send audience must exclude users with a verified DAZN redemption.
- Product education: four short Know Better cards for fractional shares, eligible ETFs, recurring investment and CopyTrader™; product names link to the supplied etoro destinations where available.
- Design variation: unlike Email 1's co-branded offer hero and mission checklist, Email 2 separates the compact DAZN reminder from the etoro-led “What comes next” product education section in dark mode.
- Footer: retained the dark Know Better treatment and explicit draft/compliance status.

## Splinter/capture status

No product-action screenshot is claimed or used. Splinter capture was not required; the visual assets are the supplied sport imagery plus the generated image-only editorial background, with official logos kept in HTML.

## QA result

- Subject: `Explore more of your etoro benefits` — 36 characters.
- Preheader: `Your DAZN code is still available. Your €20 reward is already applied. See what comes next.` — 91 characters.
- Static source checks passed: viewport meta, 640px max-width wrapper, 639px mobile breakpoint, 1280x560 headpic, separate etoro/DAZN header marks, compact coupon module, four product cards using one shared sizing rule, dynamic coupon placeholder, Know Better body-link styling, and `_blank` targets on all links.
- Rendered-width QA passed in the local browser preview after the new header/headpic refresh. The headpic rendered at 640x280 from its 1280x560 source ratio.

## Compliance caveats

- This is an English draft, not approved customer-facing copy.
- Confirm the CopyTrader™ minimum amount, the zero-commission ETF claim, eligibility, fees and required footnote wording for Germany.
- Route the final English master and disclaimer through the approved compliance workflow before production.

## Open gaps before production

- Bind the issued dynamic coupon field and add the verified redemption suppression rule.
- Confirm the final DAZN redemption URL and coupon expiry handling.
- Replace the draft disclaimer with the approved German-market customer-facing disclaimer.
- Confirm the Email 2 SFMC asset/controller naming and campaign association before upload.

## Responsive QA — 2026-09-23

- Tested the local rendered email at 320, 375, 390, 414, 480, 600, 768, and 1024px viewport widths.
- No horizontal overflow was detected at any tested width; document width stayed within the viewport.
- The 1280x560 headpic preserved its aspect ratio at every tested width, and the header marks remained undistorted.
- DAZN reminder and Explore stocks links stayed inside the viewport at all tested widths; all inspected links target `_blank`.
- Result: local responsive QA pass. SFMC/client-specific rendering and dark-mode QA still require the native BaseTemplate/controller preview.

## Pre-upload asset dry-run — 2026-09-23

- Planned S3 keys were dry-run successfully for the transparent etoro logo, boxed DAZN logo, and Email 2 headpic under the campaign production prefix.
- No S3 mutation was performed in this QA pass.

## SFMC pre-write candidate — 2026-09-23

- Proposed native asset name: `09072026_DAZNPartenershipE2`; proposed controller: `09072026_DAZNPartenershipE2_email`.
- Native Email 2 candidate SHA-256: `b1703f3cc8974ff3aae35edb7deacb9dea449de5fc64ee7e6e89472d83c3551e`.
- Exact Email 2 production asset/controller IDs and the current `MarketCampaigns` association were read back and verified after the approved write.

## SFMC write/readback — 2026-09-23

- Production Code Snippet `09072026_DAZNPartenershipE2`: asset ID `421288`, created.
- Production HTML Controller `09072026_DAZNPartenershipE2_email`: asset ID `421289`, created.
- Campaign Tag `MarketCampaigns`: ID `755`; association verified after write.
- Candidate SHA-256 and readback SHA-256 both equal `b1703f3cc8974ff3aae35edb7deacb9dea449de5fc64ee7e6e89472d83c3551e`.
- No send, schedule, journey publish, or activation was performed.
