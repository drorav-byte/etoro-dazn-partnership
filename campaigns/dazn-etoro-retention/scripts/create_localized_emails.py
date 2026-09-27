from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "translations"
GLOSSARY = Path(r"C:\Users\drorav\.codex\plugins\cache\etoro-marketing-automation\marketing-automation-codex\0.27.1\shared\dictionaries\global\glossary.json")
ENGLISH_MASTERS = {
    "email-1": {
        "source": ROOT / "DAZN-etoro-Germany-email-1-component-composed-v1.html",
        "approved_native_sha256": "9f664bf09247d53c1c242647f5a4281cbfad1d8c37a721d159d738faccd271d1",
    },
    "email-2": {
        "source": ROOT / "DAZN-etoro-Germany-email-2-reminder-v1.html",
        "approved_native_sha256": "8ce23d3b0b4e423d86a4eae7e0a54441d1717e6490bd26e460c4d1bbba1e9aa2",
    },
}


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def apply_replacements(source: str, replacements: list[tuple[str, str]], label: str) -> str:
    output = source
    for old, new in replacements:
        if old not in output:
            raise RuntimeError(f"{label}: source string not found: {old[:100]}")
        output = output.replace(old, new)
    return output


def email1(locale: str, source: str) -> str:
    if locale == "de-DE":
        replacements = [
            ('<html lang="en"', '<html lang="de-DE"'),
            ('role="article" lang="en"', 'role="article" lang="de-DE"'),
            ("Get 2 Months of DAZN FREE + Up to €300 in Rewards!", "2 Monate DAZN GRATIS + bis zu 300 € an Prämien!"),
            ("Your €20 reward is applied. Claim your DAZN benefit and see what comes next.", "Deine 20-€-Prämie wurde bereits gutgeschrieben. Kopiere deinen DAZN-Code und sichere dir dein zweimonatiges Abo."),
            ("Football and motorsport athletes", "Fußball- und Motorsportler"),
            ("PARTNERSHIP", "PARTNERSCHAFT"),
            ("YOUR BENEFITS &nbsp;•&nbsp; READY TO CLAIM", "DEINE VORTEILE &nbsp;•&nbsp; BEREIT ZUM EINLÖSEN"),
            ("Your €20 free share reward has already been applied. Copy your DAZN coupon to enjoy 2 months free, use your trading discount, and complete the 6 month deposit mission to unlock all eligible rewards.", "Deine Prämie in Form einer Gratisaktie im Wert von 20 € wurde bereits gutgeschrieben. Kopiere deinen DAZN-Gutscheincode, um 2 Monate kostenlos zu genießen, nutze deinen Rabatt auf Trading-Provisionen und schließe die 6-monatige Einzahlungsmission ab, um alle verfügbaren Prämien freizuschalten."),
            ("1 · Claim your DAZN subscription", "1 · DAZN-Abo einlösen"),
            ("Copy your DAZN coupon", "DAZN-Gutscheincode kopieren"),
            ("Copy the code below, then go to DAZN and use it to claim your two-month subscription.", "Kopiere den Code unten, gehe dann zu DAZN und löse ihn für dein zweimonatiges Abo ein."),
            ("Use on DAZN", "Auf DAZN einlösen"),
            ("Coupon code shown for layout only. The live email must render the issued, non-expired code for the eligible user.", "Der angezeigte Gutscheincode dient nur als Platzhalter. In der Live-E-Mail wird der gültige, noch nicht abgelaufene Code des berechtigten Nutzers angezeigt."),
            ("New to investing? Good to know!", "Neu beim Investieren? Gut zu wissen!"),
            ("Start small and explore at your own pace:", "Starte klein und erkunde die Möglichkeiten in deinem Tempo:"),
            ("Invest from €50 with ", "Investiere ab 50 € in "),
            ("fractional shares", "Bruchteile von Aktien"),
            ("Pay zero commission on ", "Zahle keine Provision für "),
            (">ETFs</a>", ">ETFs</a>"),
            ("Practice risk-free with a virtual portfolio.", "Übe risikofrei mit einem virtuellen Portfolio."),
            ("Automatically copy experienced investors with ", "Kopiere automatisch erfahrene Anleger mit "),
            ("Join a regulated, Nasdaq-listed platform founded in 2007.", "Nutze eine regulierte, an der Nasdaq notierte Plattform, die 2007 gegründet wurde."),
            ("YOUR MATCHDAY STARTS HERE", "DEIN SPIELTAG BEGINNT HIER"),
            ("Complete the matchday missions", "Schließe deine Spieltagsmissionen ab"),
            ("Some benefits are already in play. The rest are waiting for your next move.", "Einige Vorteile sind bereits im Spiel. Die nächsten warten auf deinen Zug."),
            (">Completed</div>", ">Abgeschlossen</div>"),
            ("€20 reward already applied", "20-€-Prämie bereits gutgeschrieben"),
            ("Your first-deposit reward was applied through the signup flow. Nothing else is needed for this step.", "Deine Prämie für die erste Einzahlung wurde im Anmeldeprozess gutgeschrieben. Für diesen Schritt musst du nichts weiter tun."),
            (">Claim</div>", ">Einlösen</div>"),
            ("Copy and use your DAZN coupon", "DAZN-Gutscheincode kopieren und verwenden"),
            ("Copy the code above and use it on DAZN to claim your two-month subscription.", "Kopiere den Code oben und löse ihn bei DAZN für dein zweimonatiges Abo ein."),
            (">Use</div>", ">Nutzen</div>"),
            ("Use your 50% trading discount", "Deinen 50-%-Rabatt auf Trading-Provisionen nutzen"),
            ("Apply your exclusive trading-commission discount to eligible activity, subject to the full terms.", "Wende deinen exklusiven Rabatt auf Trading-Provisionen auf berechtigte Aktivitäten an. Es gelten die vollständigen Bedingungen."),
            (">Build</div>", ">Aufbauen</div>"),
            ("Complete the 6-month deposit mission", "6-monatige Einzahlungsmission abschließen"),
            ("Deposit €100 or more each month into an eligible zero-commission ETF using recurring investment. After 6 months, qualifying deposits can receive a 10% promotional bonus, capped at €300 and paid manually.", "Zahle jeden Monat mindestens 100 € in einen berechtigten provisionsfreien ETF ein und nutze dafür einen Sparplan. Nach 6 Monaten können Einzahlungen, die die Voraussetzungen erfüllen, eine Werbeprämie von 10 % erhalten, begrenzt auf 300 €, die manuell ausgezahlt wird."),
            ("Start the 6-month mission", "6-monatige Mission starten"),
            ("ARRIVE BY 30 SEPTEMBER", "BIS ZUM 30. SEPTEMBER"),
            ("Benefits are subject to eligibility and full terms. The 6-month benefit is a promotional bonus based on qualifying deposits, calculated after the applicable period and paid manually. Investments can go down as well as up and your capital is at risk. Product availability and German wording require approval. Concept mockup, not approved customer-facing copy.", "Vorteile unterliegen der Berechtigung und den vollständigen Bedingungen. Der Vorteil für die 6-monatige Laufzeit ist eine Werbeprämie auf Basis von Einzahlungen, die die Voraussetzungen erfüllen, und wird nach dem jeweiligen Zeitraum berechnet und manuell ausgezahlt. Investitionen können im Wert fallen oder steigen; dein Kapital ist einem Risiko ausgesetzt. Die Produktverfügbarkeit und die deutsche Formulierung bedürfen der Genehmigung. Konzept-Mockup, noch nicht als Kundenkommunikation freigegeben."),
        ]
    else:
        replacements = [
            ('<html lang="en"', '<html lang="es-ES"'),
            ('role="article" lang="en"', 'role="article" lang="es-ES"'),
            ("Get 2 Months of DAZN FREE + Up to €300 in Rewards!", "¡2 meses de DAZN GRATIS + hasta 300 € en recompensas!"),
            ("Your €20 reward is applied. Claim your DAZN benefit and see what comes next.", "Tu recompensa de 20 € ya se ha aplicado. Copia tu código de DAZN y consigue dos meses de suscripción."),
            ("Football and motorsport athletes", "Futbolistas y pilotos de automovilismo"),
            ("PARTNERSHIP", "COLABORACIÓN"),
            ("YOUR BENEFITS &nbsp;•&nbsp; READY TO CLAIM", "TUS BENEFICIOS &nbsp;•&nbsp; LISTOS PARA RECLAMAR"),
            ("Your €20 free share reward has already been applied. Copy your DAZN coupon to enjoy 2 months free, use your trading discount, and complete the 6 month deposit mission to unlock all eligible rewards.", "Tu recompensa de 20 € en forma de acción gratis ya se ha aplicado. Copia tu cupón de DAZN para disfrutar de 2 meses gratis, usa tu descuento en las comisiones de trading y completa la misión de depósitos de 6 meses para desbloquear todas las recompensas a las que puedas optar."),
            ("1 · Claim your DAZN subscription", "1 · Reclama tu suscripción de DAZN"),
            ("Copy your DAZN coupon", "Copia tu cupón de DAZN"),
            ("Copy the code below, then go to DAZN and use it to claim your two-month subscription.", "Copia el código que aparece abajo, ve a DAZN y úsalo para reclamar tus dos meses de suscripción."),
            ("Use on DAZN", "Usar en DAZN"),
            ("Coupon code shown for layout only. The live email must render the issued, non-expired code for the eligible user.", "El código mostrado es solo un marcador de posición. El email real debe mostrar el código válido y no caducado emitido para el usuario que cumple los requisitos."),
            ("New to investing? Good to know!", "¿Acabas de empezar a invertir? Te interesa saberlo:"),
            ("Start small and explore at your own pace:", "Empieza poco a poco y explora a tu ritmo:"),
            ("Invest from €50 with ", "Invierte desde 50 € en "),
            ("fractional shares", "fracciones de acciones"),
            ("Pay zero commission on ", "Paga cero comisiones al invertir en "),
            ("Practice risk-free with a virtual portfolio.", "Practica sin riesgo con una cartera virtual."),
            ("Automatically copy experienced investors with ", "Copia automáticamente a inversores con experiencia usando "),
            ("Join a regulated, Nasdaq-listed platform founded in 2007.", "Únete a una plataforma regulada, cotizada en el Nasdaq y fundada en 2007."),
            ("YOUR MATCHDAY STARTS HERE", "TU JORNADA DE PARTIDO EMPIEZA AQUÍ"),
            ("Complete the matchday missions", "Completa las misiones de la jornada"),
            ("Some benefits are already in play. The rest are waiting for your next move.", "Algunos beneficios ya están en juego. El resto te espera para tu próximo movimiento."),
            (">Completed</div>", ">Completado</div>"),
            ("€20 reward already applied", "Recompensa de 20 € ya aplicada"),
            ("Your first-deposit reward was applied through the signup flow. Nothing else is needed for this step.", "Tu recompensa por el primer depósito se aplicó durante el registro. No tienes que hacer nada más en este paso."),
            (">Claim</div>", ">Reclama</div>"),
            ("Copy and use your DAZN coupon", "Copia y usa tu cupón de DAZN"),
            ("Copy the code above and use it on DAZN to claim your two-month subscription.", "Copia el código de arriba y úsalo en DAZN para reclamar tus dos meses de suscripción."),
            (">Use</div>", ">Usa</div>"),
            ("Use your 50% trading discount", "Usa tu descuento del 50 % en trading"),
            ("Apply your exclusive trading-commission discount to eligible activity, subject to the full terms.", "Aplica tu descuento exclusivo en las comisiones de trading a las operaciones que cumplan los requisitos. Consulta todas las condiciones."),
            (">Build</div>", ">Construye</div>"),
            ("Complete the 6-month deposit mission", "Completa la misión de depósitos de 6 meses"),
            ("Deposit €100 or more each month into an eligible zero-commission ETF using recurring investment. After 6 months, qualifying deposits can receive a 10% promotional bonus, capped at €300 and paid manually.", "Deposita 100 € o más cada mes en un ETF elegible sin comisiones utilizando una inversión recurrente. Después de 6 meses, los depósitos que cumplan los requisitos pueden recibir una recompensa promocional del 10 %, con un máximo de 300 €, que se abonará manualmente."),
            ("Start the 6-month mission", "Inicia la misión de 6 meses"),
            ("ARRIVE BY 30 SEPTEMBER", "COMPLÉTALO ANTES DEL 30 DE SEPTIEMBRE"),
            ("Benefits are subject to eligibility and full terms. The 6-month benefit is a promotional bonus based on qualifying deposits, calculated after the applicable period and paid manually. Investments can go down as well as up and your capital is at risk. Product availability and German wording require approval. Concept mockup, not approved customer-facing copy.", "Los beneficios están sujetos a elegibilidad y a las condiciones completas. El beneficio de 6 meses es una recompensa promocional basada en depósitos que cumplen los requisitos, calculada después del periodo aplicable y abonada manualmente. Las inversiones pueden subir o bajar de valor y tu capital está en riesgo. La disponibilidad de los productos y la redacción para España requieren aprobación. Mockup conceptual; no es un texto aprobado para clientes."),
        ]
    return apply_replacements(source, replacements, f"email-1 {locale}")


def email2(locale: str, source: str) -> str:
    if locale == "de-DE":
        replacements = [
            ('<html lang="en"', '<html lang="de-DE"'),
            ("Explore more of your etoro benefits", "Entdecke weitere Vorteile bei etoro"),
            ("Your DAZN code is still available. Your €20 reward is already applied. See what comes next.", "Dein DAZN-Code ist noch verfügbar. Deine 20-€-Prämie wurde bereits gutgeschrieben. Entdecke, was als Nächstes kommt."),
            ("Football and Formula 1 athletes from DAZN sports coverage", "Fußball- und Formel-1-Athleten aus dem DAZN-Sportangebot"),
            ("PARTNERSHIP", "PARTNERSCHAFT"),
            ("&bull; YOUR BENEFITS ARE WAITING", "&bull; DEINE VORTEILE WARTEN AUF DICH"),
            ("You've already unlocked your first benefit", "Dein erster Vorteil ist bereits freigeschaltet"),
            ("Your €20 free share reward has already been applied. If you haven’t started your two-month DAZN subscription yet, your code is still available: ", "Deine Prämie in Form einer Gratisaktie im Wert von 20 € wurde bereits gutgeschrieben. Wenn du dein zweimonatiges DAZN-Abo noch nicht gestartet hast, ist dein Code weiterhin verfügbar: "),
            ("Use it on DAZN", "Auf DAZN einlösen"),
            (" to claim your free two-month subscription.", " und dein kostenloses zweimonatiges Abo aktivieren."),
            ("The code shown is a layout placeholder. The live email must render the eligible user’s issued, unexpired code.", "Der angezeigte Code dient nur als Platzhalter. In der Live-E-Mail wird der gültige, noch nicht abgelaufene Code des berechtigten Nutzers angezeigt."),
            ("WHAT COMES NEXT", "WAS KOMMT ALS NÄCHSTES"),
            ("Make more of your etoro account", "Mach mehr aus deinem etoro-Konto"),
            ("DAZN is one benefit already waiting for you. The six-month mission gives you more ways to explore etoro, from investing small amounts to following experienced investors.", "DAZN ist ein Vorteil, der bereits auf dich wartet. Die 6-monatige Mission eröffnet dir weitere Möglichkeiten, etoro zu entdecken – vom Investieren kleiner Beträge bis zum Folgen erfahrener Anleger."),
            ("Fractional shares", "Bruchteile von Aktien"),
            ("Buy part of a stock—from NVIDIA, Tesla, adidas, Ferrari or Mercedes-Benz—and start investing from €10.", "Kaufe einen Teil einer Aktie – zum Beispiel von NVIDIA, Tesla, adidas, Ferrari oder Mercedes-Benz – und starte mit 10 €."),
            ("Zero-commission ETFs", "ETFs ohne Provision"),
            ("Follow a basket of investments in one fund, including an ETF that tracks the S&amp;P 500.*", "Investiere mit einem Fonds in einen Korb von Anlagen, darunter ein ETF, der den S&amp;P 500 abbildet.*"),
            ("Recurring investment", "Sparplan"),
            ("Invest a set amount into an eligible ETF each month.", "Investiere jeden Monat einen festen Betrag in einen geeigneten ETF."),
            ("See how other investors trade, then copy their positions in one click. Minimum investment: $200.*", "Sieh dir an, wie andere Anleger investieren, und kopiere ihre Positionen mit einem Klick. Mindestanlage: 200 USD.*"),
            ("*Eligibility, minimums, fees and other terms apply. Investments can go down as well as up.", "*Es gelten Teilnahmevoraussetzungen, Mindestbeträge, Gebühren und weitere Bedingungen. Der Wert von Investitionen kann steigen oder fallen."),
            ("Explore stocks", "Aktien entdecken"),
            ("ARRIVE BY 30 SEPTEMBER", "BIS ZUM 30. SEPTEMBER"),
            ("Benefits are subject to eligibility and full terms. The €20 reward was applied through the signup flow. Product availability and German wording require approval. Concept mockup, not approved customer-facing copy.", "Vorteile unterliegen der Berechtigung und den vollständigen Bedingungen. Die 20-€-Prämie wurde im Anmeldeprozess gutgeschrieben. Die Produktverfügbarkeit und die deutsche Formulierung bedürfen der Genehmigung. Konzept-Mockup, noch nicht als Kundenkommunikation freigegeben."),
        ]
    else:
        replacements = [
            ('<html lang="en"', '<html lang="es-ES"'),
            ("Explore more of your etoro benefits", "Descubre más beneficios de etoro"),
            ("Your DAZN code is still available. Your €20 reward is already applied. See what comes next.", "Tu código de DAZN sigue disponible. Tu recompensa de 20 € ya se ha aplicado. Descubre lo que viene."),
            ("Football and Formula 1 athletes from DAZN sports coverage", "Futbolistas y pilotos de Fórmula 1 de la cobertura deportiva de DAZN"),
            ("PARTNERSHIP", "COLABORACIÓN"),
            ("&bull; YOUR BENEFITS ARE WAITING", "&bull; TUS BENEFICIOS TE ESPERAN"),
            ("You've already unlocked your first benefit", "Ya tienes desbloqueado tu primer beneficio"),
            ("Your €20 free share reward has already been applied. If you haven’t started your two-month DAZN subscription yet, your code is still available: ", "Tu recompensa de 20 € en forma de acción gratis ya se ha aplicado. Si todavía no has empezado tus dos meses de suscripción a DAZN, tu código sigue disponible: "),
        ("Use it on DAZN", "Úsalo en DAZN"),
            (" to claim your free two-month subscription.", " para activar tus dos meses gratis."),
            ("The code shown is a layout placeholder. The live email must render the eligible user’s issued, unexpired code.", "El código mostrado es solo un marcador de posición. El email real debe mostrar el código válido y no caducado emitido para el usuario que cumple los requisitos."),
            ("WHAT COMES NEXT", "LO QUE VIENE"),
            ("Make more of your etoro account", "Saca más partido a tu cuenta de etoro"),
            ("DAZN is one benefit already waiting for you. The six-month mission gives you more ways to explore etoro, from investing small amounts to following experienced investors.", "DAZN es uno de los beneficios que ya tienes disponibles. La misión de 6 meses te ofrece más formas de explorar etoro, desde invertir pequeñas cantidades hasta seguir a inversores con experiencia."),
            ("Fractional shares", "Fracciones de acciones"),
            ("Buy part of a stock—from NVIDIA, Tesla, adidas, Ferrari or Mercedes-Benz—and start investing from €10.", "Compra una parte de una acción —por ejemplo, de NVIDIA, Tesla, adidas, Ferrari o Mercedes-Benz— y empieza a invertir desde 10 €."),
            ("Zero-commission ETFs", "ETF sin comisiones"),
            ("Follow a basket of investments in one fund, including an ETF that tracks the S&amp;P 500.*", "Sigue una cesta de inversiones a través de un solo fondo, incluido un ETF que sigue el S&amp;P 500.*"),
            ("Recurring investment", "Inversión recurrente"),
            ("Invest a set amount into an eligible ETF each month.", "Invierte cada mes una cantidad fija en un ETF elegible."),
            ("See how other investors trade, then copy their positions in one click. Minimum investment: $200.*", "Consulta cómo invierten otras personas y copia sus posiciones con un solo clic. Inversión mínima: 200 USD.*"),
            ("*Eligibility, minimums, fees and other terms apply. Investments can go down as well as up.", "*Se aplican los requisitos de elegibilidad, mínimos, comisiones y otras condiciones. El valor de las inversiones puede subir o bajar."),
            ("Explore stocks", "Explorar acciones"),
            ("ARRIVE BY 30 SEPTEMBER", "COMPLÉTALO ANTES DEL 30 DE SEPTIEMBRE"),
            ("Benefits are subject to eligibility and full terms. The €20 reward was applied through the signup flow. Product availability and German wording require approval. Concept mockup, not approved customer-facing copy.", "Los beneficios están sujetos a elegibilidad y a las condiciones completas. La recompensa de 20 € se aplicó durante el registro. La disponibilidad de los productos y la redacción para España requieren aprobación. Mockup conceptual; no es un texto aprobado para clientes."),
        ]
    return apply_replacements(source, replacements, f"email-2 {locale}")


def main() -> None:
    OUT.mkdir(exist_ok=True)
    glossary = json.loads(GLOSSARY.read_text(encoding="utf-8"))
    glossary_excerpt = [
        {"source_term": r["source_term"], "locale_id": r["locale_id"], "translation": r["translation"]}
        for r in glossary["records"]
        if r["locale_id"] in {"de-DE", "es-ES"}
        and r["source_term"] in {"CopyTrader", "Portfolio", "Recurring investment"}
    ]
    translations = []
    for email_id, meta in ENGLISH_MASTERS.items():
        source_text = meta["source"].read_text(encoding="utf-8-sig")
        for locale in ("de-DE", "es-ES"):
            translated = email1(locale, source_text) if email_id == "email-1" else email2(locale, source_text)
            # Translation files live one directory below the English masters;
            # keep local preview assets working without changing approved CDN links.
            translated = translated.replace('src="assets/', 'src="../assets/')
            if email_id == "email-1":
                # Keep all four mission cards equal-height on narrow mobile previews;
                # the German/Spanish copy is taller than the English source at 390px.
                translated = translated.replace(
                    ".dzn-card-inner { height: 204px !important; min-height: 204px !important; }",
                    ".dzn-card-inner { height: 266px !important; min-height: 266px !important; }",
                )
                translated = translated.replace(
                    ".dzn-card-inner { height: 264px !important; min-height: 264px !important; }",
                    ".dzn-card-inner { height: 266px !important; min-height: 266px !important; }",
                )
            filename = f"{email_id}-{locale}.html"
            output_path = OUT / filename
            output_path.write_text(translated, encoding="utf-8")
            translations.append({
                "email": email_id,
                "locale": locale,
                "file": str(OUT / filename),
                "approved_english_native_sha256": meta["approved_native_sha256"],
                "english_mockup_source_sha256": sha256_file(meta["source"]),
                "localized_source_sha256": sha256_file(output_path),
                "review_basis": "approved_english_master" if email_id == "email-1" else "english_mockup_revision",
                "glossary_terms_applied": [x for x in glossary_excerpt if x["locale_id"] == locale],
                "compliance_status": (
                    "derived_from_approved_english_master; localized_market_qa_pending"
                    if email_id == "email-1"
                    else "mockup_revision_not_production_approved; localized_market_qa_pending"
                ),
            })
    manifest = {
        "campaign_id": "dazn-etoro-retention",
        "source_locale": "en-GB",
        "target_locales": ["de-DE", "es-ES"],
        "generated_at": "2026-09-23",
        "glossary": {
            "path": str(GLOSSARY),
            "content_hash": glossary["content_hash"],
            "generated_at_utc": glossary["generated_at_utc"],
            "terms_used": glossary_excerpt,
        },
        "translations": translations,
        "not_performed": ["SFMC upload", "send", "schedule", "journey activation"],
    }
    (OUT / "localization-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
