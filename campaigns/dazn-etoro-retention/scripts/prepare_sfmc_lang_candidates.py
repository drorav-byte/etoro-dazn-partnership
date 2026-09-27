from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from prepare_sfmc_candidates import ROOT, native_content


OUT = ROOT / "qa" / "sfmc-lang-candidates"
LOCALES = ("de-DE", "es-ES")
EMAILS = {
    "email1": {
        "source": ROOT / "DAZN-etoro-Germany-email-1-component-composed-v1.html",
        "translations": {
            "de-DE": ROOT / "translations" / "email-1-de-DE.html",
            "es-ES": ROOT / "translations" / "email-1-es-ES.html",
        },
        "name": "09072026_DAZNPartenershipE1_LANG",
        "controller": "09072026_DAZNPartenershipE1_LANG_email",
        "subjects": {
            "en-GB": "Get 2 Months of DAZN FREE + Up to €300 in Rewards!",
            "de-DE": "2 Monate DAZN GRATIS + bis zu 300 € an Prämien!",
            "es-ES": "¡2 meses de DAZN GRATIS + hasta 300 € en recompensas!",
        },
        "preheaders": {
            "en-GB": "Your €20 reward is already applied. Copy your DAZN code and claim your two-month subscription.",
            "de-DE": "Deine 20-€-Prämie wurde bereits gutgeschrieben. Kopiere deinen DAZN-Code und sichere dir dein zweimonatiges Abo.",
            "es-ES": "Tu recompensa de 20 € ya se ha aplicado. Copia tu código de DAZN y consigue dos meses de suscripción.",
        },
    },
    "email2": {
        "source": ROOT / "DAZN-etoro-Germany-email-2-reminder-v1.html",
        "translations": {
            "de-DE": ROOT / "translations" / "email-2-de-DE.html",
            "es-ES": ROOT / "translations" / "email-2-es-ES.html",
        },
        "name": "09072026_DAZNPartenershipE2_LANG",
        "controller": "09072026_DAZNPartenershipE2_LANG_email",
        "subjects": {
            "en-GB": "Explore more of your etoro benefits",
            "de-DE": "Entdecke weitere Vorteile bei etoro",
            "es-ES": "Descubre más beneficios de etoro",
        },
        "preheaders": {
            "en-GB": "Your DAZN code is still available. Your €20 reward is already applied. See what comes next.",
            "de-DE": "Dein DAZN-Code ist noch verfügbar. Deine 20-€-Prämie wurde bereits gutgeschrieben. Entdecke, was als Nächstes kommt.",
            "es-ES": "Tu código de DAZN sigue disponible. Tu recompensa de 20 € ya se ha aplicado. Descubre lo que viene.",
        },
    },
}


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def amp_escape(value: str) -> str:
    return value.replace('"', '""')


def native_for(path: Path, *, subject: str, preheader: str) -> str:
    return native_content(path, subject=subject, preheader=preheader)


def lang_content(email: dict) -> str:
    branches: list[tuple[str, str]] = []
    for locale in LOCALES:
        branches.append(
            (
                locale,
                native_for(
                    email["translations"][locale],
                    subject=email["subjects"][locale],
                    preheader=email["preheaders"][locale],
                ),
            )
        )
    english = native_for(
        email["source"],
        subject=email["subjects"]["en-GB"],
        preheader=email["preheaders"]["en-GB"],
    )
    output = [
        "%%[",
        'IF Lowercase(@Language) == "de-de" THEN',
        "]%%",
        branches[0][1].rstrip(),
        "%%[",
        'ELSEIF Lowercase(@Language) == "es-es" THEN',
        "]%%",
        branches[1][1].rstrip(),
        "%%[",
        'ELSE',
        '    SET @fallback = "en-GB"',
        "]%%",
        english.rstrip(),
        "%%[",
        "ENDIF",
        "]%%",
        "",
    ]
    return "\n".join(output)


def validate(email: dict, content: str) -> dict:
    hrefs = re.findall(r'<a\b[^>]*\bhref="([^"]+)"', content, flags=re.I)
    branches = {
        "de-DE": content.count('Lowercase(@Language) == "de-de"'),
        "es-ES": content.count('Lowercase(@Language) == "es-es"'),
        "en-fallback": content.count('SET @fallback = "en-GB"'),
    }
    checks = {
        "has_all_language_branches": branches == {"de-DE": 1, "es-ES": 1, "en-fallback": 1},
        "no_local_asset_refs": not re.search(r'(?:src|href)="(?:\.\./)?assets/', content, flags=re.I),
        "no_semantic_sections": not re.search(r"<(?:section|article)\b", content, flags=re.I),
        "all_links_tracked": bool(hrefs) and all("@TrackingLink" in href for href in hrefs),
        "all_links_blank": len(hrefs) == len(re.findall(r'<a\b[^>]*target="_blank"', content, flags=re.I)),
        "dynamic_coupon": "v(@DAZN_CouponCode)" in content,
        "localized_subjects": all(email["subjects"][x] in content for x in ("en-GB", "de-DE", "es-ES")),
    }
    if not all(checks.values()):
        raise RuntimeError(json.dumps({"email": email["name"], "checks": checks}, ensure_ascii=False))
    return {
        "name": email["name"],
        "controller": email["controller"],
        "bytes": len(content.encode("utf-8")),
        "sha256": sha256_bytes(content.encode("utf-8")),
        "anchors": len(hrefs),
        "tracking_links": sum("@TrackingLink" in href for href in hrefs),
        "blank_targets": len(re.findall(r'<a\b[^>]*target="_blank"', content, flags=re.I)),
        "language_branches": branches,
        "checks": checks,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    assets = []
    for email in EMAILS.values():
        content = lang_content(email)
        path = OUT / f"{email['name']}.html"
        path.write_text(content, encoding="utf-8")
        item = validate(email, content)
        item["path"] = str(path)
        assets.append(item)
    package_hash = sha256_bytes("\n".join(item["sha256"] for item in assets).encode("ascii"))
    manifest = {
        "campaign_id": "dazn-etoro-retention",
        "environment": "production",
        "asset_mode": "new_LANG_assets_with_english_fallback",
        "fallback_locale": "en-GB",
        "locales": ["de-DE", "es-ES", "en-GB"],
        "campaign_tag": {"name": "MarketCampaigns", "id": 755},
        "package_sha256": package_hash,
        "assets": assets,
        "not_performed": ["SFMC mutation", "send", "schedule", "journey activation"],
    }
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
