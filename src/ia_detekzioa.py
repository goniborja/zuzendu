# -*- coding: utf-8 -*-
"""
ZUZENDU v3 — IA detekzioa API dei independentean.

Testua aztertu eta IA bidez sortua izan daitekeen ebaluatu,
zuzenketa-pipeline-a hasi AURRETIK.
"""

import json
import re

import anthropic

IA_PROMPT = """Aztertu testu hau eta erabaki ea DBH4 mailako ikasle batek idatzi duen ala IA bidez sortua izan daitekeen.

Puntuatu 0-3 seinale bakoitza:
S1. Perfekzio susmagarria (ia akatsik gabe DBH mailan)
S2. Hiztegi ez-naturala (C1/C2 hitzak DBH ikasle batean)
S3. Egitura perfektua (sarrera-garapena-ondorioa perfektua)
S4. Tonu robotikoa (pertsonalitate gabekoa)
S5. Luzera susmagarria (800+ hitz DBH4n)
S6. Akats-patroi naturalen falta
S7. Kalitate uniformea hasieratik bukaeraraino

Erantzun JSON SOILIK:
{"ia_puntuazioa": X, "seinaleak": {"S1": X, "S2": X, "S3": X, "S4": X, "S5": X, "S6": X, "S7": X}, "iruzkina": "..."}
"""

# Probabilitate-mailak (S1-S7 batura, max 21)
BAXUA = 7      # 0-7:  ebaluatu normalean
ERTAINA = 13   # 8-13: ebaluatu + irakasle-oharra
# 14-21 = ALTUA: blokeatu, ez ebaluatu


def ia_detekzioa(testua: str, api_key: str, model: str) -> dict:
    """
    IA detekzio-analisia egin API dei independente batean.

    Itzuli:
        {
            "ia_puntuazioa": int,
            "seinaleak": {"S1": int, ...},
            "iruzkina": str,
            "maila": "BAXUA" | "ERTAINA" | "ALTUA",
            "blokeatu": bool  # True bada, ez ebaluatu
        }
    """
    client = anthropic.Anthropic(api_key=api_key)

    response = client.messages.create(
        model=model,
        max_tokens=512,
        messages=[{
            "role": "user",
            "content": f"{IA_PROMPT}\n\n<testua>\n{testua}\n</testua>",
        }],
    )

    response_text = response.content[0].text.strip()

    # JSON atera
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", response_text, re.DOTALL)
    if match:
        response_text = match.group(1).strip()

    try:
        result = json.loads(response_text)
    except json.JSONDecodeError:
        return {
            "ia_puntuazioa": 0,
            "seinaleak": {},
            "iruzkina": f"JSON parseatzean huts egin du: {response_text[:200]}",
            "maila": "BAXUA",
            "blokeatu": False,
        }

    # BUG KONPONDUA: modeloaren ia_puntuazioa EZ da fidagarria.
    # Python-etik S1-S7 seinaleen batura kalkulatu eta hori erabili.
    seinaleak = result.get("seinaleak", {})
    batura = sum(seinaleak.get(f"S{i}", 0) for i in range(1, 8))

    # Modeloaren jatorrizko balioa gorde trazabilitaterako
    result["ia_puntuazioa_modelo"] = result.get("ia_puntuazioa", 0)
    result["ia_puntuazioa"] = batura

    if batura <= BAXUA:
        maila = "BAXUA"
    elif batura <= ERTAINA:
        maila = "ERTAINA"
    else:
        maila = "ALTUA"

    result["maila"] = maila
    result["blokeatu"] = batura >= 14

    return result


def sortu_blokeo_json(kodea: str, ia_result: dict) -> dict:
    """IA susmoa altua denean, JSON minimoa sortu ebaluaziorik gabe."""
    return {
        "kodea": kodea,
        "ebaluazioa": {},
        "laburpena": {
            "batez_bestekoa": None,
            "biribiltzea": None,
            "heziberri_maila": None,
            "orokorra": "Testu hau ez da ebaluatu IA bidez sortua izan daitekeelako. Hitz egin zure irakaslearekin.",
        },
        "akats_taldeak": [],
        "EP100": {},
        "meta": {
            "segurtasun_azterketa": {
                "susmagarria": True,
                "ia_puntuazioa": ia_result.get("ia_puntuazioa", 0),
                "seinaleak": ia_result.get("seinaleak", {}),
                "maila": ia_result.get("maila", "ALTUA"),
                "iruzkina": ia_result.get("iruzkina", ""),
                "mezua": "Testu hau IA bidez sortua izan daitekeela susmatzen da. Irakaslearekin hitz egin behar duzu.",
            },
            "irakasle_berrikusketa": {
                "beharrezkoa": True,
                "arrazoiak": [
                    f"IA susmo {ia_result.get('maila', 'ALTUA').lower()} (puntuazioa: {ia_result.get('ia_puntuazioa', 0)}/21)"
                ],
            },
        },
    }
