from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from deploy_sfmc_both import (
    ENV_FILE,
    VARIABLES_ID,
    BASE_TEMPLATE_ID,
    api,
    asset_type,
    auth,
    campaign_tag,
    controller,
    current_content,
    current_controller,
    find_asset,
    load_env,
)


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "qa" / "sfmc-lang-candidates" / "manifest.json"
TAG_NAME = "MarketCampaigns"


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def read_candidate(item: dict) -> str:
    return Path(item["path"]).read_text(encoding="utf-8")


def upsert_lang(cfg: dict[str, str], token: str, *, item: dict, approval: dict[str, str] | None, apply: bool, report: dict) -> None:
    name = item["name"]
    controller_name = item["controller"]
    native = read_candidate(item)
    candidate_hash = sha256(native)
    if candidate_hash != item["sha256"]:
        raise RuntimeError(f"Candidate changed after manifest generation: {name}")
    existing_content = find_asset(cfg, token, name)
    existing_controller = find_asset(cfg, token, controller_name)
    if existing_content and asset_type(existing_content) != "codesnippetblock":
        raise RuntimeError(f"{name} exists with wrong type {asset_type(existing_content)}")
    if existing_controller and asset_type(existing_controller) != "htmlemail":
        raise RuntimeError(f"{controller_name} exists with wrong type {asset_type(existing_controller)}")
    entry = {
        "name": name,
        "controller": controller_name,
        "candidate_sha256": candidate_hash,
        "candidate_bytes": len(native.encode("utf-8")),
        "existing_content_id": (existing_content or {}).get("id"),
        "existing_controller_id": (existing_controller or {}).get("id"),
        "operation": "update" if existing_content or existing_controller else "create",
    }
    if existing_content:
        entry["prewrite_content_sha256"] = sha256(current_content(cfg, token, int(existing_content["id"])))
    if existing_controller:
        entry["prewrite_controller_sha256"] = sha256(current_controller(cfg, token, int(existing_controller["id"])))
    report["assets"].append(entry)
    if not apply:
        return
    if not approval or approval.get("approved_by") != "Dror Avni" or approval.get("command") != "CONFIRM_WRITE":
        raise RuntimeError("LANG production write requires CONFIRM_WRITE and approved_by=Dror Avni")
    if approval.get("source_sha256") != report["package_sha256"]:
        raise RuntimeError("Approval hash does not match the LANG package hash")
    content_payload = {"name": name, "assetType": {"id": 220, "name": "codesnippetblock"}, "content": native}
    if existing_content:
        content_id = int(existing_content["id"])
        api(cfg, token, f"/asset/v1/content/assets/{content_id}", method="PATCH", body={"content": native})
        content_operation = "updated"
    else:
        written = api(cfg, token, "/asset/v1/content/assets", method="POST", body=content_payload)
        content_id = int(written["id"])
        content_operation = "created"
    controller_payload = {
        "name": controller_name,
        # SFMC limits customerKey to 36 characters. Keep a deterministic,
        # unique key derived from the LANG asset name without the suffix.
        "customerKey": f"{name}_EM",
        "assetType": {"id": 208, "name": "htmlemail"},
        "data": {"email": {"options": {"characterEncoding": "utf-8"}}},
        "views": {
            "subjectline": {"content": "%%=TREATASCONTENT(@subject)=%%"},
            "preheader": {"content": "%%=TREATASCONTENT(@preheader)=%%"},
            "html": {"content": controller(content_id)},
        },
    }
    if existing_controller:
        controller_id = int(existing_controller["id"])
        api(
            cfg,
            token,
            f"/asset/v1/content/assets/{controller_id}",
            method="PATCH",
            body={k: v for k, v in controller_payload.items() if k not in {"name", "customerKey", "assetType"}},
        )
        controller_operation = "updated"
    else:
        written = api(cfg, token, "/asset/v1/content/assets", method="POST", body=controller_payload)
        controller_id = int(written["id"])
        controller_operation = "created"
    tag_id = int(report["campaign_tag_id"])
    assoc = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    assoc_items = (assoc.get("items") or []) if isinstance(assoc, dict) else []
    if not any(str(x.get("itemID") or "") == str(controller_id) and str(x.get("type") or "").upper() == "CMS_ASSET" for x in assoc_items):
        api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets", method="POST", body={"ids": [str(controller_id)], "type": "CMS_ASSET"})
    verify_assoc = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    verify_items = (verify_assoc.get("items") or []) if isinstance(verify_assoc, dict) else []
    if not any(str(x.get("itemID") or "") == str(controller_id) and str(x.get("type") or "").upper() == "CMS_ASSET" for x in verify_items):
        raise RuntimeError(f"Campaign association readback failed for {controller_name}")
    readback = current_content(cfg, token, content_id)
    readback_controller = current_controller(cfg, token, controller_id)
    if sha256(readback) != candidate_hash:
        raise RuntimeError(f"Content hash mismatch for {name}")
    if f'ContentBlockById("{content_id}")' not in readback_controller or f'ContentBlockById("{BASE_TEMPLATE_ID}")' not in readback_controller or f'ContentBlockById("{VARIABLES_ID}")' not in readback_controller:
        raise RuntimeError(f"Controller wiring readback failed for {controller_name}")
    entry.update({
        "content_id": content_id,
        "controller_id": controller_id,
        "content_operation": content_operation,
        "controller_operation": controller_operation,
        "readback_content_sha256": sha256(readback),
        "readback_controller_sha256": sha256(readback_controller),
        "campaign_association_verified": True,
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--command", default="")
    parser.add_argument("--batch-id", default="")
    parser.add_argument("--approved-by", default="")
    parser.add_argument("--source-sha256", default="")
    args = parser.parse_args()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    cfg = load_env(ENV_FILE)
    token = auth(cfg)
    tag = campaign_tag(cfg, token)
    tag_id = int(tag.get("id") or tag.get("ID"))
    if tag.get("name") != TAG_NAME:
        raise RuntimeError(f"Unexpected campaign tag: {tag.get('name')}")
    approval = {"command": args.command, "batch_id": args.batch_id, "approved_by": args.approved_by, "source_sha256": args.source_sha256}
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": cfg.get("SFMC_ENV"),
        "account_id": cfg.get("SFMC_ACCOUNT_ID"),
        "asset_mode": manifest["asset_mode"],
        "campaign_tag_name": TAG_NAME,
        "campaign_tag_id": tag_id,
        "campaign_tag_readback": tag,
        "package_sha256": manifest["package_sha256"],
        "approval": approval if args.apply else None,
        "mutation_performed": False,
        "assets": [],
    }
    for item in manifest["assets"]:
        upsert_lang(cfg, token, item=item, approval=approval, apply=args.apply, report=report)
    report["mutation_performed"] = args.apply
    report["send_or_activation_performed"] = False
    out = ROOT / "qa" / "sfmc-lang-production-write-20260923.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
