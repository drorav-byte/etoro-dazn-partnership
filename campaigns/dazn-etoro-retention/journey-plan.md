# DAZN x etoro Germany — four-email retention journey

**Version:** Reset v2 — planning draft
**Audience:** 7,000 German DAZN sport fans who register with etoro; includes freemium and churned-user test cells and people with little or no investing experience.
**Primary objective:** Turn the DAZN-led acquisition into a completed benefit journey and a repeat-deposit habit.
**Primary message:** Two months of DAZN is the hero. The etoro rewards and product features explain why the user should complete the next action and keep going.

## Journey principle

The user should understand the whole value exchange in the first email, with the DAZN coupon available immediately, then receive one clear action at a time:

1. See the full benefits and understand what is available now versus after qualifying actions.
2. Claim the DAZN subscription by copying the coupon code in Email 1 and using it on DAZN.
3. Build the six-month deposit habit with recurring investment and an eligible zero-commission ETF.
4. Return for the next monthly action and discover simple, non-intimidating etoro features.

The first week contains three emails. The fourth email is deliberately later so it reinforces a behaviour rather than repeating the acquisition message.

## Four-email plan

| Email | Timing and entry rule | Job to be done | Main message | Primary action | Secondary value layer |
|---|---|---|---|---|---|
| **E1 — The benefits are waiting** | Immediately when the DAZN coupon is issued after the user completes the required V3/qualifying deposit step; target this within the first registration week | Make the full offer legible and get the user to claim DAZN | **Get 2 months of DAZN plus more benefits from etoro** | Primary: `Copy your DAZN code`, then `Use on DAZN` → `https://www.dazn.com/`. Secondary: `Pick a stock & deposit` → `https://www.etoro.com/deposit` | Coupon code, €20 first-deposit reward status, 50% trading-commission discount, six-month deposit bonus, eligible zero-commission ETFs, and recurring investment |
| **E2 — Use your DAZN benefit** | Day 2–3 after E1; suppress after a verified DAZN redemption | Remove redemption friction and return the user to the benefit | **Your 2 months of DAZN are ready to use** | `Use on DAZN` → `https://www.dazn.com/` | Re-state the coupon expiry and show the next etoro benefit action without repeating the full offer |
| **E3 — Build the six-month run** | Day 5–7 after E1; suppress if the user already completed the six-month setup | Convert reward interest into a repeatable monthly action | **Keep the benefits moving: deposit €100+ each month** | `Set up recurring investment` → final approved recurring-investment destination | Eligible zero-commission ETFs, 10% promotional bonus on qualifying deposits after six months, and 50% discount subject to terms |
| **E4 — Keep your place in the season** | Around day 30 after E1 or the next monthly deposit window; branch on progress | Reinforce the habit and introduce the simplest next product idea | **Your next month is part of the plan** | `Make this month’s deposit` → `https://www.etoro.com/deposit` | Progress-to-six-month view; virtual portfolio/demo; CopyTrader with risk/history context; interest on eligible balances only if current German terms are approved |

### E1 content architecture: strongest message first

E1 must not make the user assemble the offer from several emails. The hierarchy is:

1. **DAZN hero and coupon:** “Get 2 months of DAZN.” Show the issued coupon code in the first email with copy instructions.
2. **Short-term benefits:** “Your €20 first-deposit reward is applied” when true, plus the 50% trading-commission discount, each with its eligibility/status clearly labelled.
3. **Long-term benefit:** “Keep depositing for six months and you may receive a promotional bonus equal to 10% of qualifying deposits, up to the approved cap, paid manually after the calculation period.”
4. **Simple route:** “Pick an eligible stock or ETF, deposit, then choose a monthly routine.”
5. **Beginner reassurance:** eligible zero-commission ETFs, recurring investment, low-fee information, virtual portfolio/demo, and CopyTrader education are supporting explanations—not competing heroes.

Suggested E1 subject line: **Your 2 months of DAZN and more are waiting**
Suggested E1 preheader: **Your €20 reward is applied. Claim your DAZN benefit and see what comes next.**
Suggested E1 opening paragraph: **Your €20 reward is already applied. Copy your DAZN coupon to claim a 2-month free DAZN subscription, use your trading discount and complete the six-month deposit mission to receive all qualifying benefits.**

The coupon-code block belongs in E1. Never show a placeholder code in a live email. E1 must be gated on a real, non-expired coupon value.

## Message and channel rules

- Keep **DAZN and the two-month subscription** in the subject, preheader, hero, or first visible module of the journey.
- Use football and matchday language as a light narrative thread: “next fixture”, “keep your place”, “build the habit”. Do not use sports language to imply investment performance or certainty.
- Make the state explicit: `Completed`, `Ready to claim`, `Next step`, or `Available after six months`.
- Use “reward” in customer-facing copy; do not use the internal term “airdrop”.
- The DAZN subscription is claimed by copying the coupon code in E1 and going to DAZN. It is the email’s primary action; the etoro deposit link is secondary.
- The €20 reward is described as already applied only for users whose qualifying reward has actually been granted.
- Do not mention crypto or CFDs.
- Avoid “guaranteed 10% returns”, “risk-free”, “nothing to lose”, or any wording that turns the promotional bonus into investment performance.
- Use lowercase `etoro` in campaign-facing copy pending the final brand/legal sign-off already recorded for this project.

## Branching and suppression

The journey needs a small state model rather than four identical sends:

| User state | E1 | E2 | E3 | E4 |
|---|---|---|---|---|
| Deposit and V3 complete; DAZN code issued | Full offer plus visible coupon | Use DAZN benefit | Six-month habit setup | Progress and next deposit |
| DAZN code issued and redeemed | Full offer plus coupon and redeemed state | Skip redemption reminder | Six-month habit setup | Progress and next deposit |
| Recurring investment already active | Full offer; acknowledge setup | DAZN redemption | Skip setup instruction; show progress | Monthly progress |
| Reward/reversal or eligibility issue | Hold journey and resolve state | Suppress promotional claim until resolved | Suppress bonus claim | Resolve or exit |

Users who register but have not yet completed the action that issues the DAZN coupon need a separate pre-qualification reminder or service flow; they must not enter this four-email journey with a missing or placeholder code. Email sends should also be suppressed after a verified opt-out, fraud/compliance hold, unresolved reward reversal, or confirmed ineligibility. A DAZN redemption event and qualifying deposit should update the user state so later emails do not repeat completed actions.

## Supporting channels

- **Email:** owns the complete explanation, coupon instructions, terms, and long-form education.
- **In-app card:** persistent checklist showing what is `Completed`, what is `Ready to claim`, and the next qualifying action. It should deep-link to the relevant etoro destination.
- **Push notification:** short reminders only after a known action is pending, such as a code ready to claim or the next monthly deposit window. Push must not introduce a new offer or make a stronger claim than the email.

## Product progression for non-investors

Introduce one concept at a time, always after the DAZN reason to return:

- Start with an eligible stock or ETF and a manageable amount where current German terms allow.
- Explain eligible zero-commission ETFs and the relevant fee schedule in plain language.
- Offer recurring investment as a set-and-forget monthly routine, not an outcome promise.
- Offer virtual portfolio/demo before real funds where the product flow supports it.
- Introduce CopyTrader as something to review, with risk and history visible; it is not advice and does not guarantee results.
- Mention interest only on eligible balances after the current rate, eligibility, and German wording are approved.

## Measurement

Measure the journey by state transition, not opens alone:

- E1 delivery, open, click, and first qualifying deposit.
- E2 coupon-code copy, DAZN redemption, and time from code issue to redemption.
- E3 recurring-investment setup, eligible ETF selection, and month-1 qualifying deposit.
- E4 month-2 and month-6 deposits, active-investor status, and post-offer retention.
- Compare freemium and churned users with an approved control group; do not assume the same cadence or product message will win for both.

## Open decisions and blockers

- Confirm the journey entry event: E1 is now planned as a gated send after V3/qualifying deposit and actual DAZN coupon issuance. Build a separate pre-qualification flow if non-qualified registrants also need email contact.
- Confirm the DAZN plan, code-generation event, code source field, one-time-use rules, redemption URL, expiry, and fallback handling.
- Confirm the €20 reward’s qualifying amount, reward type, timing, reversals, and tax treatment.
- Confirm the 10% bonus qualifying base, current cap (€300 as the current working offer cap), calculation date, manual-payment process, reversals, and German approval.
- Confirm the 50% commission discount scope, duration, eligible instruments, and approved German wording.
- Confirm which zero-commission ETFs, minimum amounts, recurring-investment flow, CopyTrader/demo surfaces, and interest-on-balance terms are available to this audience in Germany.
- Confirm the final E1/E2/E3/E4 send windows, frequency caps, control design, and SFMC campaign/asset naming before implementation.
