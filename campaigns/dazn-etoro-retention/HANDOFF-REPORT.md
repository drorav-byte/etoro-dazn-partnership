# DAZN x etoro Retention — Full Campaign Handoff

**Handoff date:** 2026-09-27  
**Campaign folder:** `campaigns/dazn-etoro-retention`  
**Repository:** `https://github.com/drorav-byte/etoro-dazn-partnership`  
**Working branch at handoff:** `feat/dazn-etoro-retention`

This document is the operating handoff for the DAZN x etoro retention campaign. It is written so another marketer, designer, or Marketing Automation operator can open the repository, understand the complete email/design system, make a controlled change, QA it, and upload the correct assets to SFMC.

## 1. Current production status

### SFMC

| Asset | Type | Content ID | Controller ID | Status |
|---|---|---:|---:|---|
| `09072026_DAZNPartenershipE1` | Code Snippet | `419416` | `419417` | English Email 1 updated and read back |
| `09072026_DAZNPartenershipE2` | Code Snippet | `421288` | `421289` | Existing English Email 2 preserved |
| `09072026_DAZNPartenershipE1_LANG` | Code Snippet | `421322` | `421323` | German, Spanish, English fallback updated |
| `09072026_DAZNPartenershipE2_LANG` | Code Snippet | `421324` | `421325` | German, Spanish, English fallback updated |

All four controller assets are associated with the existing SFMC Campaign Tag **MarketCampaigns**, tag ID `755`. No send, schedule, journey activation, or test send was performed as part of this handoff.

### Production content hashes

| Asset | Candidate/readback SHA-256 |
|---|---|
| English Email 1 | `bb182e3fe71022b82187ee6335fd06439023cbff844da2ce69f7dd3d81f865ec` |
| English Email 2 candidate | `1214d358564b083d7ff471c2343913f48689f6c2bc906add7ddef7218cf10a4c` |
| LANG package | `02664d9bada111092454547b1481e72059717bfa4a8734c2e83ab154b96e620a` |
| Email 1 LANG content | `a61a6ac22086322aab7c4d60b1bd460a478031b5789e0d717293bda5ede5dde6` |
| Email 2 LANG content | `08456958f0cb65746bdf22739d0eedcc6d1d52f2dcb0baf37dd561e85c7e8fc7` |

### Approval records

The approved write records were:

```text
CONFIRM_WRITE | batch_id=dazn-etoro-20260924-001 | approved_by=Dror Avni | source_sha256=bb182e3fe71022b82187ee6335fd06439023cbff844da2ce69f7dd3d81f865ec
CONFIRM_WRITE | batch_id=dazn-etoro-20260924-002 | approved_by=Dror Avni | source_sha256=1214d358564b083d7ff471c2343913f48689f6c2bc906add7ddef7218cf10a4c
CONFIRM_WRITE | batch_id=dazn-etoro-20260924-003 | approved_by=Dror Avni | source_sha256=02664d9bada111092454547b1481e72059717bfa4a8734c2e83ab154b96e620a
```

The English Email 1 overwrite was separately authorized after the headpic repair:

```text
I authorize overwriting the existing English Email 1 SFMC asset.
```

## 2. Journey and message strategy

The campaign is a four-email retention journey for German DAZN sport fans who register with etoro. The first week contains three touches; Email 4 is later and reinforces the habit.

| Email | Timing | Role | Primary action |
|---|---|---|---|
| E1 — The benefits are waiting | Immediately after qualifying deposit/V3 completion and actual coupon issuance | Present the complete benefit stack; make DAZN the hero | Copy the DAZN coupon, then use it on DAZN |
| E2 — More benefits to explore | Reminder after E1; suppress after redemption where the journey supports it | Explain etoro products simply without repeating the full E1 layout | Explore stocks/products |
| E3 — Build the six-month run | Day 5–7 | Encourage the qualifying monthly deposit routine | Start recurring investment / make the deposit |
| E4 — Keep your place in the season | Around day 30 or next deposit window | Reinforce progress and the next monthly action | Make the next deposit |

### E1 copy and structure

- **Subject:** `Get 2 Months of DAZN FREE + Up to €300 in Rewards!`
- **Preheader:** `Your €20 reward is applied. Claim your DAZN benefit and see what comes next.`
- **Opening message:** The €20 free-share reward is already applied; copy the DAZN coupon, claim two free months, use the trading discount, and complete the six-month deposit mission to unlock eligible rewards.
- **Main module order:** header → sport headpic → status line → DAZN coupon → completed €20 reward → trading discount → six-month deposit mission → beginner/product bullets → deposit CTA → disclaimer/footer.
- **Dynamic field:** the production candidate renders `AttributeValue("DAZN_CouponCode")` as `%%=v(@DAZN_CouponCode)=%%`. The source mockup placeholder `DAZN-XXXX-XXXX` is not a live coupon.
- **DAZN CTA:** `https://www.dazn.com/`
- **Deposit CTA:** `https://www.etoro.com/deposit`

### E2 copy and structure

- **Subject:** `Explore more of your etoro benefits`
- **Preheader:** `Your DAZN code is still available. Your €20 reward is already applied. See what comes next.`
- **Opening message:** The €20 reward is already applied; if the user has not started the DAZN subscription, the issued coupon is still available. The body then focuses on simple etoro product education.
- **Card content:**
  - **Fractional shares:** buy part of a stock, with examples such as NVIDIA, Tesla, adidas, Ferrari, and Mercedes-Benz; the working copy says start investing from €10.
  - **Zero-commission ETFs:** follow a basket of investments in one fund, including an ETF tracking the S&P 500.
  - **Recurring investment:** invest a set amount into an eligible ETF each month.
  - **CopyTrader™:** see how other investors trade, then copy their positions in one click; current working copy states a `$200` minimum investment and must remain subject to final terms.
- **DAZN reminder link:** `https://www.dazn.com/`
- **Product links:**
  - Stocks/fractional shares: `https://www.etoro.com/discover/markets/stocks`
  - ETFs: `https://www.etoro.com/discover/markets/etf?theme=light&mainRegion=Europe%20Developed,Europe%20Emerging&lang=en`
  - CopyTrader: `https://www.etoro.com/discover/people`

## 3. Localization and fallback behavior

The LANG assets are Code Snippets with one renderable language tree per email:

```text
IF Lowercase(@Language) == "de-de" THEN
  German content
ELSEIF Lowercase(@Language) == "es-es" THEN
  Spanish content
ELSE
  SET @fallback = "en-GB"
  English content
ENDIF
```

Production readback confirmed one `de-DE` branch, one `es-ES` branch, and one final `ELSE` branch in both LANG assets. Unknown or unsupported languages therefore receive the English version. The English fallback includes the English subject, preheader, body, links, dynamic coupon field, and Email 1 headpic.

Localized source files:

- [Email 1 German](translations/email-1-de-DE.html)
- [Email 1 Spanish](translations/email-1-es-ES.html)
- [Email 2 German](translations/email-2-de-DE.html)
- [Email 2 Spanish](translations/email-2-es-ES.html)
- [SFMC LANG candidates and manifest](qa/sfmc-lang-candidates/)

## 4. Design system

### Visual direction

The creative combines DAZN sport energy with the etoro Know Better dark-mode system. DAZN is the acquisition hero; etoro benefits are explained as clear next steps. Sport references are editorial framing, not investment-performance claims.

### Layout

- Maximum email width: `640px`.
- Mobile gutters are reduced through responsive CSS; content remains table-based for inbox compatibility.
- Headpics use full-width responsive images with `display:block`, `width:100%`, `height:auto`, and no stretched aspect ratios.
- Cards use equal-height table cells, dark backgrounds, subtle borders, rounded corners, and a restrained green gradient.
- CTAs are table-based rounded buttons with an explicit background color and dark text for Outlook/Gmail compatibility.
- All production links use `_blank` targets and tracking wrappers in the SFMC candidates.
- Logos sit on the native dark header background; do not place them inside white or mismatched frames.

### Working colors

| Token | Value | Use |
|---|---|---|
| Dark background | `#10110E` | Email canvas, header, cards |
| Deep green | `#0F2E1F` | Coupon/card gradient and benefit surfaces |
| etoro green | `#6DFF8A` | Eyebrows, bullets, accents, dashed coupon border |
| CTA green | `#57CC6E` | Primary buttons |
| Warm heading | `#ECEAD1` | Headings and high-emphasis text |
| Muted text | `#BDBBA7` | Body copy and secondary labels |
| Border | `#5B5E57` | Card and header dividers |
| Coupon panel | `#242635` | Dynamic code field |

### Fonts

Use the safe system stack already in the HTML:

```css
-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif
```

Do not introduce a webfont dependency into the sendable HTML. Preserve the existing hierarchy: small uppercase green eyebrow, warm bold heading, muted body copy, and compact green CTA.

### Image roles

- **Email 1 headpic:** football and motorsport athletes, dark sport-led composition.
- **Email 2 headpic:** revised football/motorsport composition used in the reminder email.
- **E1 mission icons:** football reward, football coupon, Know Better medal, FIBA cup. These are expressive DAZN-style sport icons and are not product UI screenshots.
- **Header logos:** transparent etoro logo and boxed white DAZN logo on the native dark background.

## 5. Source and design repository map

### Authoritative email sources

- [Email 1 sendable HTML](DAZN-etoro-Germany-email-1-component-composed-v1.html)
- [Email 1 MJML source](DAZN-etoro-Germany-email-1-component-composed-v1.mjml)
- [Email 2 sendable HTML](DAZN-etoro-Germany-email-2-reminder-v1.html)

### Local translations

The files in `translations/` are human-readable localized render sources. The production LANG files in `qa/sfmc-lang-candidates/` are the deployable AMPscript branch assets with tracking wrappers and English fallback.

### Assets

| File | Role | SHA-256 |
|---|---|---|
| `assets/dazn-email-1-headpic-v2.png` | E1 headpic | `DE868B12FBD107992B392188BFFBB42F175AEF8A55C87756BF0E2AFB0FFA659F` |
| `assets/dazn-email-2-headpic-v3.png` | E2 headpic | `EC0288A9715F4C3567D086F263694C8B3E380B345C89D7F6240C7AC2F55A6ECA` |
| `assets/etoro-logo-official-transparent.png` | Header etoro logo | verify with `Get-FileHash` before a new upload |
| `assets/dazn-boxed-logo-white.png` | Header DAZN logo | verify with `Get-FileHash` before a new upload |
| `assets/illustration-icons/know-better-medal-trading-discount-v3.png` | E1 trading-discount icon | Creative Studio record in `qa/creative-studio/` |
| `assets/illustration-icons/fiba-cup-six-months-v3.png` | E1 six-month icon | Creative Studio record in `qa/creative-studio/` |
| `assets/illustration-icons/source-dazn/` | User-supplied DAZN icon references | Source material only |

### Scripts

- `scripts/create_localized_emails.py` — regenerates localized HTML from the English sources.
- `scripts/prepare_sfmc_candidates.py` — converts local asset URLs to hosted URLs, adds the dynamic coupon AMPscript, and prepares English native content/controller candidates.
- `scripts/prepare_sfmc_lang_candidates.py` — builds the German/Spanish/English-fallback LANG package and manifest.
- `scripts/deploy_sfmc_both.py` — guarded English asset preflight/write; supports `--email1-only`, `--email2-only`, and `--apply`.
- `scripts/deploy_sfmc_lang.py` — guarded LANG asset preflight/write; preserves Code Snippet asset type.
- `scripts/verify_sfmc_email2_readback.py` — Email 2 readback helper.

### QA and evidence

- [Localization and SFMC preflight QA](qa/localization-qa-20260924.md)
- [Email 1 inbox QA](qa/email1-component-composed-v1-inbox-qa.md)
- [Email 1 source/component manifest](qa/email1-v2-source-component-manifest.md)
- [Email 2 inbox remediation QA](qa/email2-inbox-remediation-20260923.md)
- [Email 2 source manifest](qa/email2-reminder-source-manifest.md)
- [LANG manifest](qa/sfmc-lang-candidates/manifest.json)
- [English prewrite candidate report](qa/sfmc-prewrite-20260924.json)
- [LANG production write report](qa/sfmc-lang-production-write-20260923.json)

### Historical or non-authoritative files

`first-email-mockup.html`, `DAZN-etoro-Germany-email-1-planned-v2.html`, `DAZN-etoro-Germany-email-mockup-sendable.html`, and the `.legacy` file are historical/mockup references. Do not deploy them without rebuilding candidates and re-running QA.

## 6. S3 image locations

Production image bucket: `etoro-production` in `eu-west-1`.

```text
https://etoro-production.s3.eu-west-1.amazonaws.com/e-marketing/MarketingAutomation/AI-Generated/campaigns/dazn-etoro-retention/dazn-email-1-headpic-v2.png
https://etoro-production.s3.eu-west-1.amazonaws.com/e-marketing/MarketingAutomation/AI-Generated/campaigns/dazn-etoro-retention/dazn-email-2-headpic-v3.png
```

The Email 1 headpic was restored to S3 on 2026-09-24 and returned `200 OK`, `Content-Type: image/png`, and `Content-Length: 2,447,513`.

Do not commit or upload credentials. The S3 helper reads credentials through the Marketing Automation environment/key-vault flow. Never put `env.production`, AWS keys, SFMC client secrets, or access tokens in this repository.

## 7. Rebuild and QA workflow

### Local preview

From the repository root, serve the workspace with a local HTTP server and open the authoritative HTML files. Do not preview the raw `file://` path when checking relative assets.

```powershell
python -m http.server 8765
```

Open:

```text
http://127.0.0.1:8765/campaigns/dazn-etoro-retention/DAZN-etoro-Germany-email-1-component-composed-v1.html
http://127.0.0.1:8765/campaigns/dazn-etoro-retention/DAZN-etoro-Germany-email-2-reminder-v1.html
```

Check at minimum: 640px, 480px, 375px, 320px, and 280px. Confirm no horizontal scroll, no stretched images, equal-height cards, readable CTA text, loaded S3 images, correct language, and no unresolved local asset paths in deploy candidates.

### Regenerate translations and candidates

```powershell
python campaigns/dazn-etoro-retention/scripts/create_localized_emails.py
python campaigns/dazn-etoro-retention/scripts/prepare_sfmc_candidates.py --output campaigns/dazn-etoro-retention/qa/sfmc-prewrite-YYYYMMDD.json
python campaigns/dazn-etoro-retention/scripts/prepare_sfmc_lang_candidates.py
```

Re-check the candidate hashes after every copy, link, image, or AMPscript change. An approval for an earlier hash is stale after any source change.

### SFMC preflight

The SFMC environment file is outside the repository:

```text
C:\Users\drorav\OneDrive - globaltrad\Documents\Work\Devolution Files\env.production
```

Use read-only mode first:

```powershell
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_both.py --email1-only
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_both.py --email2-only
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_lang.py
```

Before a production write, require a new exact `CONFIRM_WRITE` for each changed candidate hash. Never reuse an old approval after the content hash changes. Writes must be followed by content-hash, controller-wiring, asset-type, and campaign-association readback.

### SFMC write boundaries

```powershell
# English Email 1 only — requires explicit overwrite authorization.
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_both.py --apply --email1-only

# English Email 2 only.
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_both.py --apply --email2-only

# German/Spanish LANG assets with English fallback.
python campaigns/dazn-etoro-retention/scripts/deploy_sfmc_lang.py --apply --command CONFIRM_WRITE --batch-id <batch> --approved-by "Dror Avni" --source-sha256 <lang-package-sha256>
```

These commands update Content Builder assets only. They do not send, schedule, publish, or activate a journey.

## 8. QA checklist before any future upload

- [ ] English source copy and regulated claims are approved.
- [ ] German and Spanish wording has human/local-market QA.
- [ ] DAZN coupon field is populated by the selected audience/data contract.
- [ ] No placeholder `DAZN-XXXX-XXXX` remains in a production candidate.
- [ ] E1 and E2 subject/preheader values match the approved copy.
- [ ] All links resolve, are tracked, and use `_blank`.
- [ ] All images resolve from S3 and preserve aspect ratio.
- [ ] Mobile widths have no horizontal overflow.
- [ ] Cards, CTA, disclaimer, and footer render correctly in the target inbox clients.
- [ ] LANG assets contain `de-DE`, `es-ES`, and final English fallback branches.
- [ ] Unknown language routes to English with `@fallback = "en-GB"`.
- [ ] Candidate hashes are recorded and match the approval strings.
- [ ] `MarketCampaigns` tag ID 755 is read back and associated with the controller.
- [ ] No send, schedule, or journey activation is performed without separate authorization.

## 9. Known blockers and decisions still requiring ownership

The repository contains concept/mockup disclaimer language and working offer claims. Before a customer-facing send, Compliance/Legal and the local market owner must confirm:

- DAZN plan, coupon issuance, expiry, one-time use, and redemption terms.
- Whether the €20 reward is a free share, cash credit, or another reward type.
- The qualifying base and final cap for the six-month 10% promotion; the working email currently says up to €300.
- Scope and duration of the 50% trading discount.
- German and Spanish product availability, minimums, fee claims, CopyTrader minimum, and S&P 500 ETF wording.
- Final disclaimer and the removal of any internal “concept mockup” wording before send.
- Journey entry/suppression rules for coupon issuance, redemption, reward reversal, opt-out, fraud/compliance hold, and ineligible users.

## 10. Quick handoff for the next operator

1. Clone the GitHub repository and check out `feat/dazn-etoro-retention` or the merged campaign branch.
2. Read this file before editing any HTML.
3. Use only the authoritative E1/E2 HTML and MJML sources listed above; ignore legacy mockups for deployment.
4. Make one scoped change at a time.
5. Regenerate translations/candidates if the source changed.
6. Run local responsive and link/image QA.
7. Record new SHA-256 values.
8. Get exact approvals for the new hashes.
9. Run SFMC read-only preflight, then the narrowest `--apply` command.
10. Read back the asset content, controller wiring, asset type, campaign tag, and final mutation boundary.

The repository is the source of truth for design and copy; SFMC readback is the source of truth for production asset state; S3 `200 OK` verification is the source of truth for hosted image availability.
