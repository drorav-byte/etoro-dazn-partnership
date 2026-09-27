# Email 1 planned v2 — source and component manifest

## Source manifest

- **Headpic:** existing approved campaign headpic, hosted on the campaign S3 path:
  `dazn-germany-football-headpic.png?v=1`
- **etoro logo:** transparent local mockup asset derived from the approved wordmark:
  `assets/etoro-logo-official-transparent.png`
- **DAZN logo:** supplied boxed white mark used as a separate local mockup asset:
  `assets/dazn-boxed-logo-white.png`
- **Mission artwork:** transparent sport/achievement marks saved in the campaign assets and hosted on the campaign S3 path:
  `football-reward-v8.png` uses only the Bundesliga mark; `football-coupon-v8.png` uses only the international football; `know-better-medal-trading-discount-v3.png` is a realistic brushed-gold medal treatment based on the user-provided medal reference and Know Better icon rules; and `fiba-cup-six-months-v3.png` is a realistic brushed-gold trophy based on the supplied FIBA cup silhouette and matched to the medal style. No text, logos, badges, checks, or percentages are embedded in the revised medal or FIBA cup.
- **Coupon value:** mockup-only value `DAZN-XXXX-XXXX`. Production must replace it with the issued, non-expired coupon field and suppress the email if no valid code exists.
- **Product screenshots:** none used. This email does not claim to show an etoro product screen, so no Splinter capture was required.

## Component audit

- **Primary/headpic treatment:** aligned to `kb-text-section-primary-headpic-v1` as the active Know Better headpic reference.
- **Mission list:** aligned to `icons-list-carded-dark-v1`, the active Know Better carded-list reference for separated requirements.
- **Coupon/status module:** campaign-specific component gap. It is a simple coupon-value and action block, not an invented trading-platform interface.
- **Footer:** Know Better dark-surface treatment with a signal-green deadline label, muted body color, and repo font stack; no separate `Disclaimer` heading is shown, per creative direction. Final wording requires Regul8/legal approval before production.

## Copy order implemented

1. €20 reward already applied.
2. Copy and use the DAZN coupon for the two-month subscription.
3. Use the 50% trading-commission discount.
4. Complete the six-month deposit mission.

DAZN remains the hero and the primary action is `Use on DAZN`. The etoro deposit action is the secondary CTA.

## QA status

- Source file created as a separate planned version; prior mockup preserved.
- HTML structure and UTF-8 content reviewed.
- Responsive rules included for 640px and mobile widths.
- Rendered QA passed at 700, 640, 600, 480, 375, 320, 280, and 240px: no horizontal overflow; all four mission cards remain equal height at every tested width; all four new 256x256 icons loaded.
- New Know Better/DAZN sport marks were inspected at high resolution and rendered at 64px card size in the same four-step order as the message hierarchy.
- The selected icons are uploaded to the approved production S3 prefix and both URLs return HTTP 200. Exact local SHA-256 values: medal `f1a6ec8fcaf5082f7c7f498456be2625320f7940beba513928f6764d4523b767`; FIBA cup `5490f1757b7851752592644fb01fa15bfe861997af24f00f49042654f3716aed`.
- The supplied DAZN source marks remain unchanged, while the new medal and trophy use transparent generated artwork. No text, logo, check, percentage, progress, or other secondary glyph is embedded in the new images. Human KB_Critique is still required before production release.
- The matching co-branded header is locally verified in Email 1 and uses the native dark header background with no frame line above the headpic. SFMC production was not changed for this header revision; Code Snippet `419416`, HTML Controller `419417`, and `MarketCampaigns` association `755` remain the previously verified production reference.
- Customer-facing send readiness remains blocked until the coupon data field, approved disclaimer, bonus cap, eligibility, German wording, and human QA are confirmed.

## Responsive QA — 2026-09-23

- Tested the local rendered email at 320, 375, 390, 414, 480, 600, 768, and 1024px viewport widths.
- No horizontal overflow was detected at any tested width; document width stayed within the viewport.
- Headpic and all four mission icons preserved their source aspect ratios. Header marks remained separate and undistorted.
- Primary DAZN and deposit CTAs stayed inside the viewport at all tested widths.
- Result: local responsive QA pass. SFMC/client-specific rendering and dark-mode QA still require the native BaseTemplate/controller preview.

## SFMC pre-write candidate — 2026-09-23

- Native Email 1 candidate SHA-256: `9f664bf09247d53c1c242647f5a4281cbfad1d8c37a721d159d738faccd271d1`.
- Existing production reference remains Code Snippet `419416`, HTML Controller `419417`, Campaign Tag `MarketCampaigns` (`755` from the last verified readback).
- S3 hosting for the new transparent eToro and boxed DAZN header assets completed; each public URL returned HTTP 200.

## SFMC write/readback — 2026-09-23

- Production Code Snippet `09072026_DAZNPartenershipE1`: asset ID `419416`, updated in place.
- Production HTML Controller `09072026_DAZNPartenershipE1_email`: asset ID `419417`, updated in place.
- Campaign Tag `MarketCampaigns`: ID `755`; association verified after write.
- Candidate SHA-256 and readback SHA-256 both equal `9f664bf09247d53c1c242647f5a4281cbfad1d8c37a721d159d738faccd271d1`.
- No send, schedule, journey publish, or activation was performed.
