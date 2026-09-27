# DAZN/eToro localization QA — 23 September 2026

## Scope

Generated localized drafts for both approved English masters:

- Email 1: German (`de-DE`) and Spanish (`es-ES`)
- Email 2: German (`de-DE`) and Spanish (`es-ES`)

The approved English master remains the source of truth for Email 1. Email 2 now includes illustrative stock examples (NVIDIA, Tesla, adidas, Ferrari and Mercedes-Benz) and QQQ/Nasdaq-100 ETF context; it is not production-approved. Structure, destinations, aliases, dynamic coupon placeholder, and approved visual assets remain unchanged. Copy was adapted for local German and Spanish usage rather than translated word-for-word. The glossary was applied for `CopyTrader` and `Portfolio`; recurring-investment language is localized as `Sparplan` in German and `Inversión recurrente` in Spanish.

## Static checks

All four files passed:

- Correct document language: `de-DE` or `es-ES`.
- No common English copy residue in visible campaign text.
- Email 1: 74 tables, 5 links, 5 `_blank` targets.
- Email 2: 10 tables, 5 links, 5 `_blank` targets; example copy renders in the fractional-shares and ETF cards.
- All approved destination URLs preserved exactly from the corresponding English master.
- Dynamic coupon placeholder `DAZN-XXXX-XXXX` retained.
- Local preview assets resolve from the translation directory.
- Email 1 internal article language metadata matches the locale.

## Responsive/rendered checks

Rendered in the local browser preview at 320, 375, 390, 414, 480, 600, 768, and 1024 px widths: 32 viewport checks across the four variants.

Result: passed.

- No horizontal overflow.
- No broken images.
- All mission/product cards are equal height at each tested viewport.
- Header, hero, coupon placeholder, localized copy, cards, CTA, and disclaimer render in the narrow mobile preview.

## Release status

Email 1 remains derived from the approved English master. Email 2 and its localized variants are revised mockups and are not production-approved. Localized-market compliance, legal wording, eligibility, and destination-link review remain pending human approval. No SFMC upload, overwrite, send, schedule, or journey activation was performed.

## SHA-256

- `email-1-de-DE.html`: `b56caf91f69efd65a0eee6526351dea7d5cc661e036353f79678356f8b4b2f28`
- `email-1-es-ES.html`: `42ebde0ae610eebea01fb8c65f99650c5cbf0bf5403cf94b603ce732bea04ac6`
- `DAZN-etoro-Germany-email-2-reminder-v1.html` mockup: `d56e7779238f0026fa46e8f3b0d78460bbd9afd9887db63cfef5a33b16fa612c`
- SFMC Email 2 candidate: `beee8d9a7b73d493770334ace2739350322eeb20afda1d29a582d0cb1ca7a060`
- `email-2-de-DE.html`: `26b3a4a08b472150272ce31afc98e6cfa0759fc628558ce97ceed3f99f8dec2c`
- `email-2-es-ES.html`: `21cca56ac434064673e3edf40c4f36ed138f28efb5e4c1fd2254dc50b4ab9b1a`
