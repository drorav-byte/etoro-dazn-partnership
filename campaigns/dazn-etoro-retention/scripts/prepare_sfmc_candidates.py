from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HOSTED = "https://etoro-production.s3.eu-west-1.amazonaws.com/e-marketing/MarketingAutomation/AI-Generated/campaigns/dazn-etoro-retention/"
BASE_TEMPLATE_ID = 410059
VARIABLES_ID = 403137


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def native_content(source_path: Path, *, subject: str, preheader: str) -> str:
    source = source_path.read_text(encoding="utf-8-sig")
    styles = re.findall(r"<style(?:\s[^>]*)?>(.*?)</style>", source, flags=re.I | re.S)
    body = re.search(r"<body[^>]*>(.*?)</body>", source, flags=re.I | re.S)
    if not styles or not body:
        raise RuntimeError(f"{source_path.name}: expected style and body sections")

    html = "\n".join(f"<style>{style}</style>" for style in styles) + "\n" + body.group(1).strip()
    hosted_assets = {
        "assets/etoro-logo-official-transparent.png": HOSTED + "etoro-logo-official-transparent.png",
        "assets/dazn-boxed-logo-white.png": HOSTED + "dazn-boxed-logo-white.png",
        "assets/dazn-email-1-headpic-v2.png": HOSTED + "dazn-email-1-headpic-v2.png",
        "assets/dazn-email-2-headpic-v3.png": HOSTED + "dazn-email-2-headpic-v3.png",
    }
    for local, remote in hosted_assets.items():
        # Replace the parent-relative form first. Replacing the shorter
        # `assets/...` form first would leave `../https://...` in localized
        # branches and break the header images in SFMC.
        html = html.replace(f"../{local}", remote)
        html = html.replace(local, remote)

    html = html.replace("DAZN-XXXX-XXXX", "%%=v(@DAZN_CouponCode)=%%")
    replacements = {
        r'alias="go_to_dazn_coupon_redemption"\s+href="https://www\.dazn\.com/"': 'alias="go_to_dazn_coupon_redemption" href="%%=RedirectTo(Concat(\'https://www.dazn.com/\', @TrackingLink))=%%"',
        r'alias="learn_fractional_shares"\s+href="https://www\.etoro\.com/discover/markets/stocks"': 'alias="learn_fractional_shares" href="%%=RedirectTo(Concat(\'https://www.etoro.com/discover/markets/stocks\', @TrackingLink))=%%"',
        r'href="https://www\.etoro\.com/discover/markets/stocks"': 'alias="explore_stocks" href="%%=RedirectTo(Concat(\'https://www.etoro.com/discover/markets/stocks\', @TrackingLink))=%%"',
        r'alias="explore_etfs"\s+href="https://www\.etoro\.com/discover/markets/etf\?theme=light&amp;mainRegion=Europe%20Developed,Europe%20Emerging&amp;lang=en"': 'alias="explore_etfs" href="%%=RedirectTo(Concat(\'https://www.etoro.com/discover/markets/etf?theme=light&amp;mainRegion=Europe%20Developed,Europe%20Emerging&amp;lang=en\', @TrackingLink))=%%"',
        r'alias="explore_copytrader"\s+href="https://www\.etoro\.com/discover/people"': 'alias="explore_copytrader" href="%%=RedirectTo(Concat(\'https://www.etoro.com/discover/people\', @TrackingLink))=%%"',
        r'alias="start_six_month_deposit_mission"\s+href="https://www\.etoro\.com/deposit"': 'alias="start_six_month_deposit_mission" href="%%=RedirectTo(Concat(\'https://www.etoro.com/deposit\', @TrackingLink))=%%"',
    }
    for pattern, replacement in replacements.items():
        html, count = re.subn(pattern, replacement, html)
        if count == 0 and ("email-1" in source_path.name or "email-2" in source_path.name):
            # Email 1 and Email 2 intentionally do not contain every destination.
            continue

    if "email-2" in source_path.name:
        if not re.search(r"<table\b", html, flags=re.I):
            raise RuntimeError(f"{source_path.name}: production markup must contain presentation tables")
        if re.search(r"<(?:section|article)\b", html, flags=re.I):
            raise RuntimeError(f"{source_path.name}: semantic section/article markup is not allowed in production")

    if 'src="assets/' in html:
        raise RuntimeError(f"{source_path.name}: local asset reference remains")
    if re.search(r'<a\b(?![^>]*\btarget="_blank")', html, flags=re.I):
        raise RuntimeError(f"{source_path.name}: link without target=_blank remains")
    hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', html, flags=re.I)
    if any("@TrackingLink" not in href for href in hrefs):
        raise RuntimeError(f"{source_path.name}: every production link must include @TrackingLink")

    ampscript = (
        "%%[\n"
        f'SET @subject = "{subject}"\n'
        f'SET @preheader = "{preheader}"\n'
        'SET @DAZN_CouponCode = AttributeValue("DAZN_CouponCode")\n'
        "]%%\n"
    )
    return ampscript + html + "\n"


def controller(content_id: int) -> str:
    return (
        "<amp-script>\n%%[\n"
        "SET @HideHeader = 1\n"
        f'SET @variables = ContentBlockById("{VARIABLES_ID}")\n'
        f'SET @content = ContentBlockById("{content_id}")\n'
        f'SET @template = ContentBlockById("{BASE_TEMPLATE_ID}")\n'
        "]%%\n"
        "</amp-script>\n"
        "<custom name=\"opencounter\" type=\"tracking\">\n{{@template}}\n</custom>"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "qa" / "sfmc-prewrite-20260923.json")
    args = parser.parse_args()
    e1 = native_content(
        ROOT / "DAZN-etoro-Germany-email-1-component-composed-v1.html",
        subject="Get 2 Months of DAZN FREE + Up to €300 in Rewards!",
        preheader="Your €20 reward is already applied. Copy your DAZN code and claim your two-month subscription.",
    )
    e2 = native_content(
        ROOT / "DAZN-etoro-Germany-email-2-reminder-v1.html",
        subject="Explore more of your etoro benefits",
        preheader="Your DAZN code is still available. Your €20 reward is already applied. See what comes next.",
    )
    report = {
        "generated_from": {
            "email1": str(ROOT / "DAZN-etoro-Germany-email-1-component-composed-v1.html"),
            "email2": str(ROOT / "DAZN-etoro-Germany-email-2-reminder-v1.html"),
        },
        "campaign_tag": {"name": "MarketCampaigns", "group": "MarketCampaigns", "subgroup": "Marketing"},
        "assets": [
            {"name": "09072026_DAZNPartenershipE1", "controller": "09072026_DAZNPartenershipE1_email", "existing_reference": {"content_id": 419416, "controller_id": 419417}, "native_sha256": sha256(e1), "bytes": len(e1.encode("utf-8"))},
            {"name": "09072026_DAZNPartenershipE2", "controller": "09072026_DAZNPartenershipE2_email", "existing_reference": "SFMC readback required before upload", "native_sha256": sha256(e2), "bytes": len(e2.encode("utf-8"))},
        ],
        "planned_writes": ["upload/update hosted S3 assets", "create or update Email 1 Code Snippet and controller", "resolve and create/update Email 2 Code Snippet and controller", "associate both controllers to the read-back MarketCampaigns tag"],
        "not_performed": ["S3 upload", "SFMC mutation", "send", "schedule", "journey activation"],
        "qa_gate": "local responsive pass complete; native BaseTemplate/controller preview still required",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
