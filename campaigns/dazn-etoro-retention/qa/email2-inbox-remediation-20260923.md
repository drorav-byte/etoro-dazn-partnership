# Email 2 inbox remediation QA

Date: 2026-09-23

## Root cause

The previously stored SFMC Email 2 Code Snippet (`421288`) used semantic `section`/`article` markup with CSS in the snippet and no presentation tables. The read-only SFMC preflight confirmed that this was the version behind the inbox screenshot where the hero and product modules disappeared.

## Candidate fix

- Source: `DAZN-etoro-Germany-email-2-reminder-v1.html`
- Production asset: `09072026_DAZNPartenershipE2`
- Existing SFMC asset: `421288`
- Existing Email 2 readback SHA-256: `b1703f3cc8974ff3aae35edb7deacb9dea449de5fc64ee7e6e89472d83c3551e`
- New candidate native SHA-256: `8ce23d3b0b4e423d86a4eae7e0a54441d1717e6490bd26e460c4d1bbba1e9aa2`
- Candidate bytes: `13,468`
- Markup: 10 presentation tables, 0 `section` tags, 0 `article` tags, 5 anchors, 5 `_blank` targets
- Production preflight: hosted image replacement, dynamic `DAZN_CouponCode`, and `@TrackingLink` validation passed

## Render QA

The repaired local preview was checked at 320, 375, 390, 414, 480, 600, 768 and 1024px:

- No horizontal overflow at any width.
- Hero heading, DAZN reminder, all four product explanations, disclaimer copy and CTA are present at every width.
- All four product cards render at an equal 194px outer height at every tested width.
- Header logos and the 1280x560 headpic preserve their aspect ratios.
- The visible CTA and all product links remain inside the viewport.

## SFMC status

- Read-only production preflight completed against account `500009133`.
- `MarketCampaigns` read back as campaign tag ID `755`.
- Email 1 candidate still matches its stored production hash.
- Email 2 Code Snippet `421288` and HTML Controller `421289` were updated after the hash-specific confirmation.
- Post-write content readback SHA-256 equals `8ce23d3b0b4e423d86a4eae7e0a54441d1717e6490bd26e460c4d1bbba1e9aa2`.
- Post-write structural readback: 10 tables, 0 `section` tags, 0 `article` tags, 0 local asset references, 5 anchors, 5 `_blank` targets, 5 tracking links, dynamic coupon present, controller wiring verified, and `MarketCampaigns` association verified.
- No send, schedule, Journey publish or activation was performed.

## Release status

The approved table-based Email 2 is now uploaded and read back successfully. The local responsive/inbox-safe preview and the production asset are aligned by hash.
