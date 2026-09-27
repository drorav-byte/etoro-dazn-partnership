# DAZN x etoro localization and SFMC preflight QA — 2026-09-24

## Scope

- Email 1 and Email 2 English masters.
- German (`de-DE`) and Spanish (`es-ES`) localized mockups.
- New LANG assets retain English (`en-GB`) as the fallback branch.
- Campaign tag readback: `MarketCampaigns` (ID `755`); tracking group `MarketCampaigns`, subgroup `Marketing`.

## Local render checks

- English, German, and Spanish Email 2 previews loaded all header and hero images.
- Email 2 has four equal-height cards (`194px` in the local desktop render) and no horizontal overflow.
- Email 1 German and Spanish previews have four equal-height challenge cards (`196px`), no visible card icons, loaded images, blank-target links, and no horizontal overflow.
- Email 2 copy is localized rather than word-for-word: the stocks card says users can start from `10 €`; the ETF card says `ETFs ohne Provision` / `ETF sin comisiones` and mentions an ETF tracking the `S&P 500`.
- Dynamic coupon placeholder remains `DAZN-XXXX-XXXX` locally and is converted to `%%=v(@DAZN_CouponCode)=%%` in native candidates.

## Candidate checks

- LANG candidate package: `02664d9bada111092454547b1481e72059717bfa4a8734c2e83ab154b96e620a`.
- Email 1 LANG: `a61a6ac22086322aab7c4d60b1bd460a478031b5789e0d717293bda5ede5dde6`.
- Email 2 LANG: `08456958f0cb65746bdf22739d0eedcc6d1d52f2dcb0baf37dd561e85c7e8fc7`.
- English Email 1 native candidate: `bb182e3fe71022b82187ee6335fd06439023cbff844da2ce69f7dd3d81f865ec`.
- English Email 2 native candidate: `1214d358564b083d7ff471c2343913f48689f6c2bc906add7ddef7218cf10a4c`.
- LANG candidate validation passed: all branches present, all links tracked, all links target `_blank`, no local asset references, dynamic coupon present.

## SFMC readback

- Production account: `500009133`.
- English Email 1 existing Code Snippet/controller: `419416` / `419417`; existing content hash `9f664bf09247d53c1c242647f5a4281cbfad1d8c37a721d159d738faccd271d1`.
- English Email 2 existing Code Snippet/controller: `421288` / `421289`; existing content hash `beee8d9a7b73d493770334ace2739350322eeb20afda1d29a582d0cb1ca7a060`.
- LANG Email 1 existing Code Snippet/controller: `421322` / `421323`.
- LANG Email 2 existing Code Snippet/controller: `421324` / `421325`.
- No SFMC mutation, send, schedule, or journey activation was performed.

## Release blocker

The current English masters are still marked as mockup/compliance-pending in the campaign source. The new candidate hashes also differ from the earlier approvals. Production upload requires fresh exact-hash `CONFIRM_WRITE` approval for the English assets and the LANG package, plus final localized-market/legal approval.
