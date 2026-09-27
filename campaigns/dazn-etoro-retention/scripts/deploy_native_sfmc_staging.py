from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = Path(r"C:\Users\drorav\OneDrive - globaltrad\Documents\Work\Devolution Files\env.staging")
MOCKUP = ROOT / "DAZN-etoro-Germany-email-mockup-sendable.html"
EVIDENCE = ROOT / "qa" / "sfmc-production-overwrite-20260914.json"
TAG_NAME = "MarketCampaigns"
SUBGROUP = "Marketing"
TASK_ID = "09072026"
TASK_NAME = "DAZNPartenershipE1"
UI_CAMPAIGN_TAG = "MarketCampaigns"
APPROVED_BY = "Dror Avni"
BASE_TEMPLATE_ID = 410059
VARIABLES_ID = 403137


def sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            values[key.strip()] = value.strip().strip('"').strip("'")
    return values


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
        body={
            "grant_type": "client_credentials",
            "client_id": cfg["SFMC_CLIENT_ID"],
            "client_secret": cfg["SFMC_CLIENT_SECRET"],
            "account_id": cfg["SFMC_ACCOUNT_ID"],
        },
    )
    if status != 200 or not isinstance(data, dict) or not data.get("access_token"):
        raise RuntimeError(f"SFMC authentication failed: HTTP {status}")
    return str(data["access_token"])


def api(cfg: dict[str, str], token: str, path: str, *, method: str = "GET", body: object | None = None) -> object:
    status, data = request_json(cfg["SFMC_REST_BASE_URL"].rstrip("/") + path, method=method, token=token, body=body)
    if status < 200 or status >= 300:
        raise RuntimeError(f"SFMC {method} {path} failed: HTTP {status}: {str(data)[:1200]}")
    return data


def build_native_content() -> str:
    source = MOCKUP.read_text(encoding="utf-8-sig")
    styles = re.findall(r"<style(?:\s[^>]*)?>(.*?)</style>", source, flags=re.IGNORECASE | re.DOTALL)
    body = re.search(r"<body[^>]*>(.*?)</body>", source, flags=re.IGNORECASE | re.DOTALL)
    if not styles or not body:
        raise RuntimeError("Mockup is missing the expected style/body sections")

    html = "\n".join(f"<style>{style}</style>" for style in styles) + "\n" + body.group(1).strip()
    icon_base = "https://etoro-production.s3.eu-west-1.amazonaws.com/e-marketing/MarketingAutomation/AI-Generated/campaigns/dazn-etoro-retention/illustration-icons/"
    expected_icons = {
        "football-reward-v8.png": "v=3",
        "football-coupon-v8.png": "v=3",
        "know-better-medal-trading-discount-v3.png": "v=1",
        "fiba-cup-six-months-v3.png": "v=1",
    }
    for icon_name, version in expected_icons.items():
        hosted_src = f'src="{icon_base}{icon_name}?{version}"'
        if hosted_src not in html:
            raise RuntimeError(f"Expected hosted icon reference not found: {icon_name}")

    replacements = {
        r'(?:alias="go_to_dazn_coupon_redemption"\s+)?href="https://www\.dazn\.com/"': 'alias="go_to_dazn_coupon_redemption" href="%%=RedirectTo(Concat(\'https://www.dazn.com/\', @TrackingLink))=%%"',
        r'(?:alias="start_six_month_deposit_mission"\s+)?href="https://www\.etoro\.com/deposit"': 'alias="start_six_month_deposit_mission" href="%%=RedirectTo(Concat(\'https://www.etoro.com/deposit\', @TrackingLink))=%%"',
    }
    for pattern, new in replacements.items():
        html, count = re.subn(pattern, new, html, count=1)
        if count == 0:
            raise RuntimeError(f"Expected CTA link not found: {pattern}")

    if 'src="assets/' in html:
        raise RuntimeError("Production content still contains local asset paths")

    # SFMC executes this block before the controller renders the shared template.
    ampscript = """%%[
SET @subject = "Your 2 months of DAZN and more are waiting"
SET @preheader = "Your €20 reward is applied. Claim your DAZN benefit and see what comes next."
]%%
"""
    return ampscript + html + "\n"


def controller_html(content_id: int) -> str:
    return (
        "<amp-script>\n%%[\n"
        "var @template, @content, @variables\n"
        "set @HideHeader = 1\n"
        f'set @variables = ContentBlockById("{VARIABLES_ID}")\n'
        f'set @content = ContentBlockById("{content_id}")\n'
        f'set @variables = ContentBlockById("{VARIABLES_ID}")\n'
        f'set @template = ContentBlockById("{BASE_TEMPLATE_ID}")\n'
        "]%%\n"
        "</amp-script>\n"
        "<custom name=\"opencounter\" type=\"tracking\">\n{{@template}}\n</custom>"
    )


def exact_campaign_tag(cfg: dict[str, str], token: str) -> dict:
    items: list[dict] = []
    page = 1
    while True:
        data = api(cfg, token, f"/hub/v1/campaigns?$page={page}&$pagesize=200")
        page_items = (data.get("items") or data.get("campaigns") or []) if isinstance(data, dict) else []
        if not isinstance(page_items, list):
            raise RuntimeError("SFMC Campaign Tag response has an unexpected shape")
        items.extend(item for item in page_items if isinstance(item, dict))
        if len(page_items) < 200:
            break
        page += 1
    def label(item: dict) -> str:
        return str(
            item.get("name")
            or item.get("Name")
            or item.get("campaignName")
            or item.get("CampaignName")
            or item.get("campaign")
            or ""
        ).strip()

    matches = [item for item in items if label(item) == TAG_NAME]
    if len(matches) != 1:
        labels = [
            {
                "id": item.get("id") or item.get("ID"),
                "name": item.get("name") or item.get("Name"),
                "campaignCode": item.get("campaignCode") or item.get("code") or item.get("Code"),
            }
            for item in items[:30]
        ]
        raise RuntimeError(
            f"Expected exactly one SFMC Campaign Tag named {TAG_NAME!r}; found {len(matches)}; "
            f"readback sample={labels}"
        )
    return matches[0]


def find_asset(cfg: dict[str, str], token: str, name: str) -> dict | None:
    query = urllib.parse.urlencode({"$page": "1", "$pagesize": "200", "$filter": f"name eq '{name.replace(chr(39), chr(39) * 2)}'"})
    data = api(cfg, token, f"/asset/v1/content/assets?{query}")
    items = data.get("items") if isinstance(data, dict) else []
    matches = [item for item in (items or []) if isinstance(item, dict) and item.get("name") == name]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple exact SFMC assets found for {name!r}")
    return matches[0] if matches else None


def asset_type(asset: dict | None) -> str:
    return str(((asset or {}).get("assetType") or {}).get("name") or "")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--env-file", type=Path, default=DEFAULT_ENV_FILE)
    parser.add_argument("--confirm", default="")
    parser.add_argument("--batch-id", default="")
    parser.add_argument("--approved-by", default="")
    args = parser.parse_args()

    cfg = load_env(args.env_file)
    if cfg.get("SFMC_ENV", "").lower() not in {"staging", "production"}:
        raise RuntimeError("Unsupported SFMC environment")
    native = build_native_content()
    content_hash = sha256(native)
    freeform_name = f"{TASK_ID}_{TASK_NAME}"
    controller_name = f"{TASK_ID}_{TASK_NAME}_email"
    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": cfg.get("SFMC_ENV", "").lower(),
        "account_id": cfg.get("SFMC_ACCOUNT_ID"),
        "source_file": str(MOCKUP),
        "campaign_tag_name": UI_CAMPAIGN_TAG,
        "tracking_campaign_group": TAG_NAME,
        "tracking_campaign_subgroup": SUBGROUP,
        "task_id": TASK_ID,
        "task_name": TASK_NAME,
        "freeform_name": freeform_name,
        "controller_name": controller_name,
        "native_content_sha256": content_hash,
        "mutation_performed": False,
    }
    token = auth(cfg)
    tag = exact_campaign_tag(cfg, token)
    report["campaign_tag_id"] = tag.get("id") or tag.get("ID")
    report["campaign_tag_readback"] = tag
    existing_content = find_asset(cfg, token, freeform_name)
    existing_controller = find_asset(cfg, token, controller_name)
    report["existing_content"] = {"id": (existing_content or {}).get("id"), "type": asset_type(existing_content)}
    report["existing_controller"] = {"id": (existing_controller or {}).get("id"), "type": asset_type(existing_controller)}
    if existing_content and asset_type(existing_content) != "codesnippetblock":
        raise RuntimeError(f"Existing content asset has wrong type: {asset_type(existing_content)}")
    if existing_controller and asset_type(existing_controller) != "htmlemail":
        raise RuntimeError(f"Existing controller has wrong type: {asset_type(existing_controller)}")

    if existing_content:
        current_content = api(cfg, token, f"/asset/v1/content/assets/{int(existing_content['id'])}")
        current_content_text = str((current_content or {}).get("content") or "")
        report["existing_content_readback_sha256"] = sha256(current_content_text)
        report["existing_content_bytes"] = len(current_content_text.encode("utf-8"))
    if existing_controller:
        current_controller = api(cfg, token, f"/asset/v1/content/assets/{int(existing_controller['id'])}")
        current_controller_html = str((((current_controller or {}).get("views") or {}).get("html") or {}).get("content") or "")
        report["existing_controller_html_sha256"] = sha256(current_controller_html)
        report["existing_controller_html_bytes"] = len(current_controller_html.encode("utf-8"))

    if not args.apply:
        report["planned_operations"] = ["create or update native Code Snippet content", "create or update HTML controller", "associate controller to MarketCampaigns"]
        report["required_confirmation"] = {
            "command": "CONFIRM_WRITE",
            "batch_id": "new unique batch id",
            "approved_by": APPROVED_BY,
            "source_sha256": content_hash,
        }
        EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
        EVIDENCE.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0

    expected_confirmation = "CONFIRM_WRITE"
    if args.confirm != expected_confirmation or not args.batch_id or args.approved_by != APPROVED_BY:
        raise RuntimeError("Apply requires CONFIRM_WRITE, batch ID, and approved_by=Dror Avni")

    content_payload = {"name": freeform_name, "assetType": {"id": 220, "name": "codesnippetblock"}, "content": native}
    if existing_content:
        content_id = int(existing_content["id"])
        written_content = api(cfg, token, f"/asset/v1/content/assets/{content_id}", method="PATCH", body={"content": native})
        content_operation = "updated"
    else:
        written_content = api(cfg, token, "/asset/v1/content/assets", method="POST", body=content_payload)
        content_id = int(written_content["id"])
        content_operation = "created"

    html = controller_html(content_id)
    controller_payload = {
        "name": controller_name,
        "customerKey": f"{TASK_ID}_{TASK_NAME}_EMAIL",
        "assetType": {"id": 208, "name": "htmlemail"},
        "data": {"email": {"options": {"characterEncoding": "utf-8"}}},
        "views": {
            "subjectline": {"content": "%%=TREATASCONTENT(@subject)=%%"},
            "preheader": {"content": "%%=TREATASCONTENT(@preheader)=%%"},
            "html": {"content": html},
        },
    }
    if existing_controller:
        controller_id = int(existing_controller["id"])
        written_controller = api(cfg, token, f"/asset/v1/content/assets/{controller_id}", method="PATCH", body={k: v for k, v in controller_payload.items() if k not in {"name", "customerKey", "assetType"}})
        controller_operation = "updated"
    else:
        written_controller = api(cfg, token, "/asset/v1/content/assets", method="POST", body=controller_payload)
        controller_id = int(written_controller["id"])
        controller_operation = "created"

    tag_id = int(report["campaign_tag_id"])
    associations = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    assoc_items = (associations.get("items") or []) if isinstance(associations, dict) else []
    if not any(str(item.get("itemID") or "") == str(controller_id) and str(item.get("type") or "").upper() == "CMS_ASSET" for item in assoc_items):
        api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets", method="POST", body={"ids": [str(controller_id)], "type": "CMS_ASSET"})
    verify_assoc = api(cfg, token, f"/hub/v1/campaigns/{tag_id}/assets")
    verify_items = (verify_assoc.get("items") or []) if isinstance(verify_assoc, dict) else []
    if not any(str(item.get("itemID") or "") == str(controller_id) and str(item.get("type") or "").upper() == "CMS_ASSET" for item in verify_items):
        raise RuntimeError("Campaign association readback did not contain the controller")
    content_readback = api(cfg, token, f"/asset/v1/content/assets/{content_id}")
    controller_readback = api(cfg, token, f"/asset/v1/content/assets/{controller_id}")
    readback_content = str((content_readback or {}).get("content") or "")
    readback_html = str((((controller_readback or {}).get("views") or {}).get("html") or {}).get("content") or "")
    if sha256(readback_content) != content_hash:
        raise RuntimeError("Content hash readback mismatch")
    if f'ContentBlockById("{content_id}")' not in readback_html or f'ContentBlockById("{BASE_TEMPLATE_ID}")' not in readback_html or f'ContentBlockById("{VARIABLES_ID}")' not in readback_html:
        raise RuntimeError("Controller wiring readback mismatch")
    report.update({
        "mutation_performed": True,
        "batch_id": args.batch_id,
        "approved_by": args.approved_by,
        "content_id": content_id,
        "controller_id": controller_id,
        "content_operation": content_operation,
        "controller_operation": controller_operation,
        "content_readback_sha256": sha256(readback_content),
        "controller_html_sha256": sha256(readback_html),
        "campaign_association_verified": True,
        "human_qa_status": "pending",
        "send_or_activation_performed": False,
    })
    EVIDENCE.parent.mkdir(parents=True, exist_ok=True)
    EVIDENCE.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1)
