from __future__ import annotations

import json
import re
from pathlib import Path

from deploy_sfmc_both import ENV_FILE, api, auth, campaign_tag, current_content, current_controller, find_asset, load_env


def main() -> None:
    cfg = load_env(ENV_FILE)
    token = auth(cfg)
    content_asset = find_asset(cfg, token, "09072026_DAZNPartenershipE2")
    controller_asset = find_asset(cfg, token, "09072026_DAZNPartenershipE2_email")
    if not content_asset or not controller_asset:
        raise RuntimeError("Email 2 assets were not found")
    content_id = int(content_asset["id"])
    controller_id = int(controller_asset["id"])
    content = current_content(cfg, token, content_id)
    controller = current_controller(cfg, token, controller_id)
    hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', content, flags=re.I)
    tag = campaign_tag(cfg, token)
    tag_id = int(tag.get("id") or tag.get("ID"))
    associated = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    associated_items = (associated.get("items") or []) if isinstance(associated, dict) else []
    association_verified = any(
        str(item.get("itemID") or "") == str(controller_id)
        and str(item.get("type") or "").upper() == "CMS_ASSET"
        for item in associated_items
    )
    result = {
        "content_id": content_id,
        "controller_id": controller_id,
        "bytes": len(content.encode("utf-8")),
        "table_tags": len(re.findall(r"<table\b", content, flags=re.I)),
        "section_tags": len(re.findall(r"<section\b", content, flags=re.I)),
        "article_tags": len(re.findall(r"<article\b", content, flags=re.I)),
        "style_tags": len(re.findall(r"<style\b", content, flags=re.I)),
        "local_asset_refs": len(re.findall(r'(?:src|href)="assets/', content, flags=re.I)),
        "anchors": len(hrefs),
        "blank_targets": len(re.findall(r'<a\b[^>]*target="_blank"', content, flags=re.I)),
        "tracking_links": sum("@TrackingLink" in href for href in hrefs),
        "direct_https_hrefs": sum(href.startswith("http") for href in hrefs),
        "dynamic_coupon": "v(@DAZN_CouponCode)" in content,
        "controller_wiring": all(
            needle in controller
            for needle in (
                'ContentBlockById("421288")',
                'ContentBlockById("410059")',
                'ContentBlockById("403137")',
            )
        ),
        "campaign_tag": {"name": tag.get("name"), "id": tag_id},
        "campaign_association_verified": association_verified,
        "send_or_activation_performed": False,
    }
    if result["section_tags"] or result["article_tags"] or result["local_asset_refs"]:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    if result["anchors"] != result["tracking_links"] or result["anchors"] != result["blank_targets"]:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    if not result["controller_wiring"] or not result["campaign_association_verified"]:
        raise RuntimeError(json.dumps(result, ensure_ascii=False))
    out = Path(__file__).resolve().parents[1] / "qa" / "sfmc-email2-readback-20260923.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
