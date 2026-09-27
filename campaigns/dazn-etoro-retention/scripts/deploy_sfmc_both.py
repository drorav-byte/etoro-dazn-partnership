from __future__ import annotations

import argparse
import hashlib
import json
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from prepare_sfmc_candidates import BASE_TEMPLATE_ID, VARIABLES_ID, controller, native_content


ROOT = Path(__file__).resolve().parents[1]
ENV_FILE = Path(r"C:\Users\drorav\OneDrive - globaltrad\Documents\Work\Devolution Files\env.production")
TAG_NAME = "MarketCampaigns"
BASE_BATCH = {
    "email1": {"batch_id": "dazn-etoro-20260924-001", "approved_by": "Dror Avni", "source_sha256": "bb182e3fe71022b82187ee6335fd06439023cbff844da2ce69f7dd3d81f865ec"},
    "email2": {"batch_id": "dazn-etoro-20260924-002", "approved_by": "Dror Avni", "source_sha256": "1214d358564b083d7ff471c2343913f48689f6c2bc906add7ddef7218cf10a4c"},
}


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_env(path: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            out[key.strip()] = value.strip().strip('"').strip("'")
    return out


def request_json(url: str, *, method: str = "GET", token: str = "", body: object | None = None) -> tuple[int, object]:
    payload = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=payload, headers=headers, method=method), timeout=60) as response:
            raw = response.read().decode("utf-8")
            return response.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            detail: object = json.loads(raw)
        except json.JSONDecodeError:
            detail = raw[:2000]
        return exc.code, detail


def auth(cfg: dict[str, str]) -> str:
    status, data = request_json(
        cfg["SFMC_AUTH_BASE_URL"].rstrip("/") + "/v2/token",
        method="POST",
        body={"grant_type": "client_credentials", "client_id": cfg["SFMC_CLIENT_ID"], "client_secret": cfg["SFMC_CLIENT_SECRET"], "account_id": cfg["SFMC_ACCOUNT_ID"]},
    )
    if status != 200 or not isinstance(data, dict) or not data.get("access_token"):
        raise RuntimeError(f"SFMC authentication failed: HTTP {status}: {str(data)[:500]}")
    return str(data["access_token"])


def api(cfg: dict[str, str], token: str, path: str, *, method: str = "GET", body: object | None = None) -> object:
    status, data = request_json(cfg["SFMC_REST_BASE_URL"].rstrip("/") + path, method=method, token=token, body=body)
    if status < 200 or status >= 300:
        raise RuntimeError(f"SFMC {method} {path} failed: HTTP {status}: {str(data)[:1200]}")
    return data


def find_asset(cfg: dict[str, str], token: str, name: str) -> dict | None:
    query = urllib.parse.urlencode({"$page": "1", "$pagesize": "200", "$filter": f"name eq '{name.replace(chr(39), chr(39) * 2)}'"})
    data = api(cfg, token, f"/asset/v1/content/assets?{query}")
    items = data.get("items") if isinstance(data, dict) else []
    matches = [item for item in (items or []) if isinstance(item, dict) and item.get("name") == name]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple exact assets found for {name}")
    return matches[0] if matches else None


def asset_type(asset: dict | None) -> str:
    return str(((asset or {}).get("assetType") or {}).get("name") or "")


def campaign_tag(cfg: dict[str, str], token: str) -> dict:
    data = api(cfg, token, "/hub/v1/campaigns?$page=1&$pagesize=200")
    items = data.get("items") if isinstance(data, dict) else []
    matches = [item for item in (items or []) if isinstance(item, dict) and str(item.get("name") or item.get("Name") or "").strip() == TAG_NAME]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one Campaign Tag named {TAG_NAME}; found {len(matches)}")
    return matches[0]


def current_content(cfg: dict[str, str], token: str, asset_id: int) -> str:
    data = api(cfg, token, f"/asset/v1/content/assets/{asset_id}")
    return str((data or {}).get("content") or "")


def current_controller(cfg: dict[str, str], token: str, asset_id: int) -> str:
    data = api(cfg, token, f"/asset/v1/content/assets/{asset_id}")
    return str((((data or {}).get("views") or {}).get("html") or {}).get("content") or "")


def upsert(cfg: dict[str, str], token: str, *, name: str, controller_name: str, native: str, subject: str, preheader: str, approval: dict[str, str], apply: bool, report: dict) -> None:
    existing_content = find_asset(cfg, token, name)
    existing_controller = find_asset(cfg, token, controller_name)
    if existing_content and asset_type(existing_content) != "codesnippetblock":
        raise RuntimeError(f"{name} exists with wrong type {asset_type(existing_content)}")
    if existing_controller and asset_type(existing_controller) != "htmlemail":
        raise RuntimeError(f"{controller_name} exists with wrong type {asset_type(existing_controller)}")
    item = {"name": name, "controller": controller_name, "existing_content_id": (existing_content or {}).get("id"), "existing_controller_id": (existing_controller or {}).get("id"), "candidate_sha256": sha256(native), "candidate_bytes": len(native.encode("utf-8"))}
    if existing_content:
        current = current_content(cfg, token, int(existing_content["id"]))
        item["prewrite_content_sha256"] = sha256(current)
    if existing_controller:
        current = current_controller(cfg, token, int(existing_controller["id"]))
        item["prewrite_controller_sha256"] = sha256(current)
    report["assets"].append(item)
    if not apply:
        return
    if approval.get("approved_by") != "Dror Avni":
        raise RuntimeError(f"Approval mismatch for {name}")
    candidate_hash = sha256(native)
    if approval.get("source_sha256") != candidate_hash:
        raise RuntimeError(f"Approved hash mismatch for {name}: expected {approval.get('source_sha256')}, candidate {candidate_hash}")
    content_payload = {"name": name, "assetType": {"id": 220, "name": "codesnippetblock"}, "content": native}
    if existing_content:
        content_id = int(existing_content["id"])
        api(cfg, token, f"/asset/v1/content/assets/{content_id}", method="PATCH", body={"content": native})
        content_operation = "updated"
    else:
        written = api(cfg, token, "/asset/v1/content/assets", method="POST", body=content_payload)
        content_id = int(written["id"])
        content_operation = "created"
    controller_payload = {"name": controller_name, "customerKey": f"{name}_EMAIL", "assetType": {"id": 208, "name": "htmlemail"}, "data": {"email": {"options": {"characterEncoding": "utf-8"}}}, "views": {"subjectline": {"content": "%%=TREATASCONTENT(@subject)=%%"}, "preheader": {"content": "%%=TREATASCONTENT(@preheader)=%%"}, "html": {"content": controller(content_id)}}}
    if existing_controller:
        controller_id = int(existing_controller["id"])
        api(cfg, token, f"/asset/v1/content/assets/{controller_id}", method="PATCH", body={k: v for k, v in controller_payload.items() if k not in {"name", "customerKey", "assetType"}})
        controller_operation = "updated"
    else:
        written = api(cfg, token, "/asset/v1/content/assets", method="POST", body=controller_payload)
        controller_id = int(written["id"])
        controller_operation = "created"
    tag_id = int(report["campaign_tag_id"])
    assoc = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    items = (assoc.get("items") or []) if isinstance(assoc, dict) else []
    if not any(str(x.get("itemID") or "") == str(controller_id) and str(x.get("type") or "").upper() == "CMS_ASSET" for x in items):
        api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets", method="POST", body={"ids": [str(controller_id)], "type": "CMS_ASSET"})
    verify_assoc = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    verify_items = (verify_assoc.get("items") or []) if isinstance(verify_assoc, dict) else []
    if not any(str(x.get("itemID") or "") == str(controller_id) and str(x.get("type") or "").upper() == "CMS_ASSET" for x in verify_items):
        raise RuntimeError(f"Campaign association readback failed for {controller_id}")
    readback = current_content(cfg, token, content_id)
    readback_controller = current_controller(cfg, token, controller_id)
    if sha256(readback) != sha256(native):
        raise RuntimeError(f"Content hash mismatch for {name}")
    if f'ContentBlockById("{content_id}")' not in readback_controller or f'ContentBlockById("{BASE_TEMPLATE_ID}")' not in readback_controller or f'ContentBlockById("{VARIABLES_ID}")' not in readback_controller:
        raise RuntimeError(f"Controller wiring readback failed for {controller_name}")
    item.update({"content_id": content_id, "controller_id": controller_id, "content_operation": content_operation, "controller_operation": controller_operation, "readback_content_sha256": sha256(readback), "readback_controller_sha256": sha256(readback_controller), "campaign_association_verified": True})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--email1-only", action="store_true")
    parser.add_argument("--email2-only", action="store_true")
    args = parser.parse_args()
    if args.email1_only and args.email2_only:
        parser.error("--email1-only and --email2-only cannot be used together")
    cfg = load_env(ENV_FILE)
    token = auth(cfg)
    tag = campaign_tag(cfg, token)
    report = {"generated_at_utc": datetime.now(timezone.utc).isoformat(), "environment": cfg.get("SFMC_ENV"), "account_id": cfg.get("SFMC_ACCOUNT_ID"), "campaign_tag_name": TAG_NAME, "campaign_tag_id": tag.get("id") or tag.get("ID"), "campaign_tag_readback": tag, "mutation_performed": False, "assets": []}
    e1 = native_content(ROOT / "DAZN-etoro-Germany-email-1-component-composed-v1.html", subject="Get 2 Months of DAZN FREE + Up to €300 in Rewards!", preheader="Your €20 reward is already applied. Copy your DAZN code and claim your two-month subscription.")
    e2 = native_content(ROOT / "DAZN-etoro-Germany-email-2-reminder-v1.html", subject="Explore more of your etoro benefits", preheader="Your DAZN code is still available. Your €20 reward is already applied. See what comes next.")
    if not args.email2_only:
        upsert(cfg, token, name="09072026_DAZNPartenershipE1", controller_name="09072026_DAZNPartenershipE1_email", native=e1, subject="Get 2 Months of DAZN FREE + Up to €300 in Rewards!", preheader="Your €20 reward is already applied. Copy your DAZN code and claim your two-month subscription.", approval=BASE_BATCH["email1"], apply=args.apply, report=report)
    if not args.email1_only:
        upsert(cfg, token, name="09072026_DAZNPartenershipE2", controller_name="09072026_DAZNPartenershipE2_email", native=e2, subject="Explore more of your etoro benefits", preheader="Your DAZN code is still available. Your €20 reward is already applied. See what comes next.", approval=BASE_BATCH["email2"], apply=args.apply, report=report)
    report["mutation_performed"] = args.apply
    report["send_or_activation_performed"] = False
    out = ROOT / "qa" / "sfmc-production-write-20260923.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
