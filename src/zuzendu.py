# -*- coding: utf-8 -*-
"""
ZUZENDU v3 — Karpeta osoa prozesatzeko pipeline-a.

Karpeta-pathetik metadatuak automatikoki ateratzen ditu:
  idazlanak/DBH4B/01_narrazioa/  →  taldea=DBH4B, maila=DBH4, mota=narrazioa

Erabilera:
  python src/zuzendu.py idazlanak/DBH4B/01_narrazioa/
  python src/zuzendu.py idazlanak/DBH4B/01_narrazioa/ --modua zirriborroa
  python src/zuzendu.py idazlanak/DBH4B/01_narrazioa/ --fitxategia Telmo  # bakarra
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv
from ep100 import post_prozesatu
from ia_detekzioa import ia_detekzioa, sortu_blokeo_json
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ── Proiektuaren erroa (src/ karpetaren gurasoa) ──────────────────────────
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

console = Console()

EXPECTED_KEYS = {"kodea", "ebaluazioa", "laburpena", "akats_taldeak", "EP100", "meta"}

# Testu-mota mapa: karpeta-izenetik testu-motara
MOTA_MAPA = {
    "narrazioa": "narrazioa",
    "iritzi_artikulua": "iritzi_artikulua",
    "iritzia": "iritzi_artikulua",
    "gutun_formala": "gutun_formala",
    "gutun_informala": "gutun_informala",
    "deskribapena": "deskribapena",
    "hausnarketa": "hausnarketa",
    "gidoia": "gidoia",
    "laburpena": "laburpena",
}


def sanitize(text: str) -> str:
    """Kontsolarako bateragarri ez diren karaktereak kendu (Windows cp1252)."""
    replacements = {"\u2192": "->", "\u2190": "<-", "\u2014": "--", "\u2013": "-",
                    "\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"',
                    "\u2026": "...", "\u2022": "*", "\u00b7": "*"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text.encode("cp1252", errors="replace").decode("cp1252")


# ── Karpeta-pathetik metadatuak atera ────────────────────────────────────

def atera_metadatuak(karpeta: Path) -> dict:
    """
    Karpeta-pathetik taldea, maila eta mota atera.

    Adib: idazlanak/DBH4B/01_narrazioa/
      → taldea=DBH4B, maila=DBH4, mota=narrazioa
    """
    parts = karpeta.resolve().parts

    # Taldea bilatu: DBH[34][AB] patroia
    taldea = None
    for part in parts:
        if re.match(r"^DBH[34][AB]$", part, re.IGNORECASE):
            taldea = part.upper()
            break

    if not taldea:
        console.print("[red]ERROREA:[/] Ezin da taldea atera karpetatik. "
                       "Espero: .../DBH4B/... edo .../DBH3A/...")
        sys.exit(1)

    # Maila: DBH4B → DBH4, DBH3A → DBH3
    maila = taldea[:4]

    # Mota: azken karpeta-izenetik (01_narrazioa → narrazioa)
    azken_karpeta = karpeta.resolve().name
    # Zenbakia kendu hasieratik: "01_narrazioa" → "narrazioa"
    mota_raw = re.sub(r"^\d+_", "", azken_karpeta).lower()
    mota = MOTA_MAPA.get(mota_raw, mota_raw)

    if mota not in MOTA_MAPA.values():
        console.print(f"[yellow]ABISUA:[/] Testu-mota ezezaguna: '{mota}' "
                       f"(karpetatik: '{azken_karpeta}'). 'iritzi_artikulua' erabiliko da.")
        mota = "iritzi_artikulua"

    return {"taldea": taldea, "maila": maila, "mota": mota}


# ── Konfigurazioa kargatu ─────────────────────────────────────────────────

def load_config() -> tuple[str, str, dict[str, str]]:
    """Sistema-prompt, errubrika eta gramatika TSVak kargatu."""
    prompt_path = ROOT / "config" / "sistema_prompt.txt"
    rubric_path = ROOT / "config" / "errubrika.json"
    grammar_dir = ROOT / "config" / "gramatika"

    for p in (prompt_path, rubric_path):
        if not p.exists():
            console.print(f"[red]ERROREA:[/] {p} ez da aurkitu")
            sys.exit(1)

    sistema_prompt = prompt_path.read_text(encoding="utf-8")
    errubrika = rubric_path.read_text(encoding="utf-8")

    gramatika = {}
    skip = {"00_AURKIBIDEA.tsv", "euskal_gramatika.tsv"}
    if grammar_dir.exists():
        for tsv in sorted(grammar_dir.glob("*.tsv")):
            if tsv.name not in skip:
                gramatika[tsv.name] = tsv.read_text(encoding="utf-8")

    return sistema_prompt, errubrika, gramatika


# ── Erabiltzaile-mezua eraiki ─────────────────────────────────────────────

def build_user_message(
    errubrika: str,
    gramatika: dict[str, str],
    kodea: str,
    maila: str,
    mota: str,
    hitzak: int,
    modua: str,
    testua: str,
) -> str:
    """Erabiltzaile-mezua eraiki XML etiketekin."""
    parts = []
    parts.append("<errubrika>")
    parts.append(errubrika)
    parts.append("</errubrika>")

    for filename, content in gramatika.items():
        parts.append(f'<gramatika_fitxategia fitxategia="{filename}">')
        parts.append(content)
        parts.append("</gramatika_fitxategia>")

    hitz_info = str(hitzak) if hitzak > 0 else "zuk kontatu"
    parts.append("<ataza_metadatuak>")
    parts.append(f"kodea: {kodea}")
    parts.append(f"maila: {maila}")
    parts.append(f"testu_mota: {mota}")
    parts.append(f"hitz_kopurua: {hitz_info}")
    parts.append(f"zuzenketa_modua: {modua}")
    parts.append("</ataza_metadatuak>")

    parts.append("<ikaslearen_testua>")
    parts.append(testua)
    parts.append("</ikaslearen_testua>")

    return "\n".join(parts)


# ── JSON atera eta baliozkoztatu ──────────────────────────────────────────

def extract_json(response_text: str) -> dict:
    """JSON atera erantzunetik."""
    text = response_text.strip()
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def validate_json(data: dict) -> list[str]:
    """Espero diren gako nagusiak egiaztatu."""
    return sorted(EXPECTED_KEYS - set(data.keys()))


# ── Emaitzak gorde ────────────────────────────────────────────────────────

def save_json(data: dict, izena: str, output_dir: Path) -> Path:
    """JSON emaitza gorde karpeta egokian."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{izena}_{ts}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_raw(text: str, izena: str, output_dir: Path) -> Path:
    """Raw erantzuna gorde."""
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{izena}_{ts}_raw.txt"
    path.write_text(text, encoding="utf-8")
    return path


# ── Ikasle bat prozesatu ─────────────────────────────────────────────────

def prozesatu_ikaslea(
    fitxategia: Path,
    meta: dict,
    sistema_prompt: str,
    errubrika: str,
    gramatika: dict[str, str],
    modua: str,
    output_dir: Path,
) -> dict:
    """
    Ikasle baten testua prozesatu: IA detekzioa → ebaluazioa → post-prozesatzea.
    Itzuli: {"izena": str, "egoera": str, "nota": int|None, "ia_punt": int, ...}
    """
    izena = fitxategia.stem
    kodea = izena.split(" - ")[0].split(".")[0].strip().upper()[:20]
    testua = fitxategia.read_text(encoding="utf-8").strip()
    hitz_kopurua = len(testua.split())

    console.print(f"\n[bold cyan]{izena}[/] ({hitz_kopurua} hitz)")

    # 1. IA detekzioa
    try:
        ia_result = ia_detekzioa(testua, API_KEY, MODEL)
    except anthropic.APIError as e:
        console.print(f"  [yellow]IA detekzio errorea:[/] {e}")
        ia_result = {"ia_puntuazioa": 0, "maila": "BAXUA", "blokeatu": False,
                     "seinaleak": {}, "iruzkina": ""}

    ia_punt = ia_result.get("ia_puntuazioa", 0)
    ia_maila = ia_result.get("maila", "BAXUA")
    seinaleak = ia_result.get("seinaleak", {})
    sein_str = " ".join(f"{k}={v}" for k, v in seinaleak.items()) if seinaleak else "-"
    console.print(f"  IA: {ia_punt}/21 ({ia_maila}) [{sein_str}]")

    # 2. Blokeatu?
    if ia_result.get("blokeatu"):
        console.print(f"  [bold red]BLOKEATUA[/] — IA susmoa altua")
        result = sortu_blokeo_json(kodea, ia_result)
        output_path = save_json(result, izena, output_dir)
        console.print(f"  [dim]-> {output_path.name}[/]")
        return {"izena": izena, "kodea": kodea, "egoera": "BLOKEATUA",
                "nota": None, "ia_punt": ia_punt, "ia_maila": ia_maila}

    # 3. Ebaluazioa
    user_message = build_user_message(
        errubrika, gramatika,
        kodea, meta["maila"], meta["mota"], 0, modua, testua,
    )
    console.print(f"  Ebaluatzen... ", end="")

    try:
        client = anthropic.Anthropic(api_key=API_KEY)
        response = client.messages.create(
            model=MODEL,
            max_tokens=8192,
            system=sistema_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
    except anthropic.APIError as e:
        console.print(f"[red]API ERROREA:[/] {e}")
        return {"izena": izena, "kodea": kodea, "egoera": "ERROREA",
                "nota": None, "ia_punt": ia_punt, "ia_maila": ia_maila}

    response_text = response.content[0].text
    console.print(f"{response.usage.output_tokens:,} token")

    # 4. JSON parseatu
    try:
        result = extract_json(response_text)
    except (json.JSONDecodeError, ValueError) as e:
        save_raw(response_text, izena, output_dir)
        console.print(f"  [red]JSON errorea:[/] {e}")
        return {"izena": izena, "kodea": kodea, "egoera": "JSON_ERROREA",
                "nota": None, "ia_punt": ia_punt, "ia_maila": ia_maila}

    # 5. IA emaitza txertatu
    if "meta" not in result:
        result["meta"] = {}
    result["meta"]["segurtasun_azterketa"] = {
        "susmagarria": ia_maila != "BAXUA",
        "ia_puntuazioa": ia_punt,
        "ia_puntuazioa_modelo": ia_result.get("ia_puntuazioa_modelo", ia_punt),
        "seinaleak": seinaleak,
        "maila": ia_maila,
        "iruzkina": ia_result.get("iruzkina", ""),
    }
    if ia_maila == "ERTAINA":
        ir = result["meta"].setdefault("irakasle_berrikusketa", {})
        ir["beharrezkoa"] = True
        ir.setdefault("arrazoiak", []).append(
            f"IA susmo ertaina (puntuazioa: {ia_punt}/21)"
        )

    # 6. JSON baliozkoztatu
    missing = validate_json(result)
    if missing:
        console.print(f"  [yellow]Gako falta:[/] {', '.join(missing)}")

    # 7. Post-prozesatu
    result = post_prozesatu(result)
    nota = result.get("laburpena", {}).get("biribiltzea", "?")
    egoera = "ERTAINA" if ia_maila == "ERTAINA" else "OK"
    console.print(f"  [green]Nota: {nota}/10[/]  EP100p={result['EP100']['EP100_pisuduna']}")

    # 8. Gorde
    output_path = save_json(result, izena, output_dir)
    console.print(f"  [dim]-> {output_path.name}[/]")

    return {"izena": izena, "kodea": kodea, "egoera": egoera,
            "nota": nota, "ia_punt": ia_punt, "ia_maila": ia_maila,
            "ab": result["ebaluazioa"]["atazaren_betetzea"]["nota"],
            "ak": result["ebaluazioa"]["antolaketa_koherentzia"]["nota"],
            "blh": result["ebaluazioa"]["baliabide_linguistikoen_hedadura"]["nota"],
            "zl": result["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"],
            "ep100p": result["EP100"]["EP100_pisuduna"]}


# ── Laburpen-taula ────────────────────────────────────────────────────────

def print_taula(emaitzak: list[dict], meta: dict):
    """Emaitza guztien laburpen-taula."""
    table = Table(
        title=f"{meta['taldea']} — {meta['mota']}",
        show_lines=True,
    )
    table.add_column("Ikaslea", width=18)
    table.add_column("S1-S7", justify="center", width=5)
    table.add_column("Maila", width=8)
    table.add_column("Egoera", width=12)
    table.add_column("Nota", justify="center", width=4)
    table.add_column("AB", justify="center", width=3)
    table.add_column("AK", justify="center", width=3)
    table.add_column("BLH", justify="center", width=3)
    table.add_column("ZL", justify="center", width=3)
    table.add_column("EP100p", justify="right", width=6)

    for e in sorted(emaitzak, key=lambda x: x["izena"]):
        ia_color = "red" if e["ia_maila"] == "ALTUA" else "yellow" if e["ia_maila"] == "ERTAINA" else ""
        egoera_txt = f"[bold red]{e['egoera']}[/]" if e["egoera"] == "BLOKEATUA" else e["egoera"]

        if e["nota"] is not None:
            nota_color = "green" if e["nota"] >= 7 else "yellow" if e["nota"] >= 5 else "red"
            nota_txt = f"[{nota_color}]{e['nota']}[/{nota_color}]"
        else:
            nota_txt = "-"

        table.add_row(
            e["izena"][:18],
            f"[{ia_color}]{e['ia_punt']}[/{ia_color}]" if ia_color else str(e["ia_punt"]),
            e["ia_maila"],
            egoera_txt,
            nota_txt,
            str(e.get("ab", "-")),
            str(e.get("ak", "-")),
            str(e.get("blh", "-")),
            str(e.get("zl", "-")),
            str(e.get("ep100p", "-")),
        )

    console.print()
    console.print(table)

    # Kontaketak
    ok = sum(1 for e in emaitzak if e["egoera"] == "OK")
    ertaina = sum(1 for e in emaitzak if e["egoera"] == "ERTAINA")
    blok = sum(1 for e in emaitzak if e["egoera"] == "BLOKEATUA")
    err = sum(1 for e in emaitzak if e["egoera"] in ("ERROREA", "JSON_ERROREA"))
    console.print(
        f"\n  Guztira: {len(emaitzak)} | "
        f"[green]OK: {ok}[/] | "
        f"[yellow]Ertaina: {ertaina}[/] | "
        f"[red]Blokeatua: {blok}[/]"
        + (f" | [red]Errorea: {err}[/]" if err else "")
    )


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ZUZENDU v3 — Karpeta osoa prozesatu",
    )
    parser.add_argument(
        "karpeta",
        help="Idazlanen karpeta (adib: idazlanak/DBH4B/01_narrazioa/)",
    )
    parser.add_argument(
        "--modua", default="azken_bertsioa",
        choices=["zirriborroa", "azken_bertsioa"],
        help="Zuzenketa-modua (def: azken_bertsioa)",
    )
    parser.add_argument(
        "--mota", default=None,
        choices=[
            "iritzi_artikulua", "gutun_formala", "gutun_informala",
            "deskribapena", "hausnarketa", "gidoia", "narrazioa", "laburpena",
        ],
        help="Testu-mota gainidatzi (karpetatik ezin bada atera)",
    )
    parser.add_argument(
        "--fitxategia", default=None,
        help="Fitxategi bakar bat prozesatu (izena edo zatia, adib: 'Telmo')",
    )

    args = parser.parse_args()

    if not API_KEY:
        console.print("[red]ERROREA:[/] ANTHROPIC_API_KEY ez dago .env fitxategian")
        sys.exit(1)

    karpeta = Path(args.karpeta)
    if not karpeta.is_dir():
        console.print(f"[red]ERROREA:[/] '{karpeta}' ez da karpeta bat")
        sys.exit(1)

    # Metadatuak pathetik atera
    meta = atera_metadatuak(karpeta)
    if args.mota:
        meta["mota"] = args.mota
    console.print(Panel(
        f"Taldea: [bold]{meta['taldea']}[/]\n"
        f"Maila:  {meta['maila']}\n"
        f"Mota:   {meta['mota']}\n"
        f"Modua:  {args.modua}",
        title="ZUZENDU v3",
        width=40,
    ))

    # .txt fitxategiak bilatu
    fitxategiak = sorted(karpeta.glob("*.txt"))
    if args.fitxategia:
        fitxategiak = [f for f in fitxategiak if args.fitxategia.lower() in f.name.lower()]

    if not fitxategiak:
        console.print("[red]ERROREA:[/] Ez dago .txt fitxategirik karpeta honetan")
        sys.exit(1)

    console.print(f"[dim]{len(fitxategiak)} fitxategi aurkituta[/]")

    # Konfigurazioa kargatu (behin)
    sistema_prompt, errubrika, gramatika = load_config()
    console.print(f"[dim]Konfigurazioa: errubrika + {len(gramatika)} gramatika TSV[/]")

    # Output karpeta kalkulatu: emaitzak/[TALDEA]/[AKTIBITATEA]/
    # karpeta = idazlanak/DBH4B/01_narrazioa → emaitzak/DBH4B/01_narrazioa
    rel_parts = []
    found_taldea = False
    for part in karpeta.resolve().parts:
        if re.match(r"^DBH[34][AB]$", part, re.IGNORECASE):
            found_taldea = True
        if found_taldea:
            rel_parts.append(part)
    output_dir = ROOT / "emaitzak" / "/".join(rel_parts) if rel_parts else ROOT / "emaitzak"
    console.print(f"[dim]Emaitzak → {output_dir.relative_to(ROOT)}[/]")

    # Prozesatu fitxategi bakoitza
    emaitzak = []
    for i, fitx in enumerate(fitxategiak, 1):
        console.print(f"\n{'='*60}")
        console.print(f"[bold][{i}/{len(fitxategiak)}][/] {fitx.name}")
        console.print(f"{'='*60}")

        em = prozesatu_ikaslea(
            fitx, meta, sistema_prompt, errubrika, gramatika, args.modua, output_dir,
        )
        emaitzak.append(em)

    # Laburpen-taula
    console.print(f"\n{'='*60}")
    print_taula(emaitzak, meta)


if __name__ == "__main__":
    main()
