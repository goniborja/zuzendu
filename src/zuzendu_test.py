# -*- coding: utf-8 -*-
"""
ZUZENDU v3 — Fase 1.3: Script minimoa
Testua + config → Anthropic API → JSON ebaluazioa → data/emaitzak/

Erabilera:
  python src/zuzendu_test.py                          # few-shot adibidea erabili
  python src/zuzendu_test.py testua.txt               # fitxategitik
  python src/zuzendu_test.py testua.txt --kodea 3A017 --maila DBH4
  echo "Nire testua..." | python src/zuzendu_test.py --stdin
  python src/zuzendu_test.py testua.txt --mota narrazioa --modua zirriborroa
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
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# ── Proiektuaren erroa (src/ karpetaren gurasoa) ──────────────────────────
ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

console = Console()

# ── Few-shot testu lehenetsia (DBH4-015, 138 hitz) ───────────────────────
TESTU_LEHENETSIA = """\
Pasa den astean nire lagun eta biok kafetegi batean geundela, konturatu \
ginen inguruko nerabe guztiak eskuko telefonoa erabiltzen zutela etengabe. \
Hori harritu gintuen.

Alde batetik, eskuko telefonoak onura asko dakartza. Hala nola, \
informazioa bilatzeko oso erabilgarriak dira eta lagunekin kontaktuan \
egoteko ere bai. Baina beste alde batetik edozein arlotan bezala gauza \
txarrak ere badaude. Esaterako, nerabeak gero eta denbora gehiago \
pasatzen dute pantailen aurrean eta hori ez da ona haien osasunerako.

Nire ustez guraso eta irakasleek konponbide bat bilatu behar dute \
problema honi aurre egiteko. Esate baterako, mugak jarriz eta \
alternatibak proposatuz. Horrela nerabeak modu osasungarrian erabili \
ahalko dute teknologia.

Laburbilduz, eskuko telefonoak tresna onak dira baina kontuz erabili \
behar ditugu."""

EXPECTED_KEYS = {"kodea", "ebaluazioa", "laburpena", "akats_taldeak", "EP100", "meta"}


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


# ── Testua kargatu ────────────────────────────────────────────────────────

def load_text(path: str | None, from_stdin: bool) -> str:
    """Testua irakurri fitxategitik, stdin-etik edo lehenetsia erabili."""
    if from_stdin:
        text = sys.stdin.read().strip()
        if not text:
            console.print("[red]ERROREA:[/] stdin hutsik dago")
            sys.exit(1)
        return text

    if path is None:
        console.print("[yellow]Testu-fitxategirik ez — few-shot adibidea erabiliko da (DBH4-015)[/]")
        return TESTU_LEHENETSIA

    p = Path(path)
    if not p.exists():
        console.print(f"[red]ERROREA:[/] Fitxategia ez da aurkitu: {p}")
        sys.exit(1)
    return p.read_text(encoding="utf-8").strip()


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

    # 1. Errubrika
    parts.append("<errubrika>")
    parts.append(errubrika)
    parts.append("</errubrika>")

    # 2. Gramatika TSVak
    for filename, content in gramatika.items():
        parts.append(f'<gramatika_fitxategia fitxategia="{filename}">')
        parts.append(content)
        parts.append("</gramatika_fitxategia>")

    # 3. Metadatuak
    hitz_info = str(hitzak) if hitzak > 0 else "zuk kontatu"
    parts.append("<ataza_metadatuak>")
    parts.append(f"kodea: {kodea}")
    parts.append(f"maila: {maila}")
    parts.append(f"testu_mota: {mota}")
    parts.append(f"hitz_kopurua: {hitz_info}")
    parts.append(f"zuzenketa_modua: {modua}")
    parts.append("</ataza_metadatuak>")

    # 4. Ikaslearen testua
    parts.append("<ikaslearen_testua>")
    parts.append(testua)
    parts.append("</ikaslearen_testua>")

    return "\n".join(parts)


# ── JSON atera eta baliozkoztatu ──────────────────────────────────────────

def extract_json(response_text: str) -> dict:
    """JSON atera erantzunetik, markdown code fences kendu behar badira."""
    text = response_text.strip()
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def validate_json(data: dict) -> list[str]:
    """Espero diren gako nagusiak egiaztatu. Falta direnak itzuli."""
    return sorted(EXPECTED_KEYS - set(data.keys()))


# ── Emaitzak gorde ────────────────────────────────────────────────────────

def save_json(data: dict, kodea: str) -> Path:
    """JSON emaitza gorde data/emaitzak/ karpetan."""
    output_dir = ROOT / "data" / "emaitzak"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{kodea}_{ts}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return path


def save_raw(text: str, kodea: str) -> Path:
    """Raw erantzuna gorde debug-erako."""
    output_dir = ROOT / "data" / "emaitzak"
    output_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    path = output_dir / f"{kodea}_{ts}_raw.txt"
    path.write_text(text, encoding="utf-8")
    return path


# ── Emaitza pantailaratu ──────────────────────────────────────────────────

def print_summary(result: dict):
    """Laburpen irakurgarria rich bidez."""
    lab = result.get("laburpena", {})
    eb = result.get("ebaluazioa", {})
    ep = result.get("EP100", {})
    akatsak = result.get("akats_taldeak", [])

    # Nota orokorra
    nota = lab.get("biribiltzea", "?")
    maila = lab.get("heziberri_maila", "?")

    color = "green" if nota != "?" and nota >= 7 else "yellow" if nota != "?" and nota >= 5 else "red"
    console.print(Panel(
        f"[bold {color}]{nota}/10[/] — {maila}",
        title="NOTA",
        width=50,
    ))

    # Irizpideen taula
    table = Table(title="Irizpideak", show_lines=True, width=50)
    table.add_column("Irizpidea", width=8)
    table.add_column("Nota", justify="center", width=6)
    table.add_column("Maila", width=14)
    table.add_column("Cap", width=8)

    criteria_map = {
        "AB": "atazaren_betetzea",
        "AK": "antolaketa_koherentzia",
        "BLH": "baliabide_linguistikoen_hedadura",
        "ZL": "zuzentasun_linguistikoa",
    }
    for short, key in criteria_map.items():
        crit = eb.get(key, {})
        n = crit.get("nota", "?")
        m = crit.get("maila", "?")
        c = crit.get("cap_aplikatua") or "-"
        table.add_row(short, str(n), m, c)

    console.print(table)

    # EP100
    if ep:
        console.print(
            f"  EP100: gordina={ep.get('EP100_gordina', '?')} | "
            f"pisuduna={ep.get('EP100_pisuduna', '?')} | "
            f"hitzak={ep.get('hitz_kopurua', '?')} | "
            f"minor={ep.get('minor', 0)} major={ep.get('major', 0)} critical={ep.get('critical', 0)}"
        )

    # Akats-taldeak
    if akatsak:
        console.print(f"\n  Akats-taldeak: {len(akatsak)}")
        for a in akatsak:
            z = " [dim](zalantzazkoa)[/]" if a.get("zalantzazkoa") else ""
            console.print(
                f"    [{a.get('larritasuna', '?')}] {a.get('kategoria', '?')} "
                f"x{a.get('kopurua', '?')} ({a.get('akats_id', '?')}){z}"
            )

    # Lehentasuna
    if lab.get("lehentasuna"):
        console.print(Panel(lab["lehentasuna"], title="Lehentasuna", width=70))

    # Irakasle berrikusketa
    meta = result.get("meta", {})
    ir = meta.get("irakasle_berrikusketa", {})
    if ir.get("beharrezkoa"):
        console.print(Panel(
            "\n".join(ir.get("arrazoiak", [])),
            title="[red]IRAKASLE BERRIKUSKETA BEHAR DA[/]",
            width=70,
        ))


# ── Main ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="ZUZENDU v3 -- Testua ebaluatu Anthropic API bidez",
    )
    parser.add_argument(
        "testua", nargs="?", default=None,
        help="Testu-fitxategiaren bidea. Hutsik utziz gero, few-shot adibidea erabiliko da.",
    )
    parser.add_argument("--stdin", action="store_true", help="Testua stdin-etik irakurri")
    parser.add_argument("--kodea", default="TEST-001", help="Ikaslearen kodea (def: TEST-001)")
    parser.add_argument("--maila", default="DBH4", choices=["DBH3", "DBH4"], help="Maila (def: DBH4)")
    parser.add_argument(
        "--mota", default="iritzi_artikulua",
        choices=[
            "iritzi_artikulua", "gutun_formala", "gutun_informala",
            "deskribapena", "hausnarketa", "gidoia", "narrazioa", "laburpena",
        ],
        help="Testu-mota (def: iritzi_artikulua)",
    )
    parser.add_argument("--hitzak", type=int, default=0, help="Hitz-kopurua (0 = zuk kontatu)")
    parser.add_argument(
        "--modua", default="azken_bertsioa",
        choices=["zirriborroa", "azken_bertsioa"],
        help="Zuzenketa-modua (def: azken_bertsioa)",
    )

    args = parser.parse_args()

    # API key egiaztatu
    if not API_KEY:
        console.print("[red]ERROREA:[/] ANTHROPIC_API_KEY ez dago konfiguratuta .env fitxategian")
        sys.exit(1)

    # 1. Testua kargatu
    testua = load_text(args.testua, args.stdin)
    hitz_kopurua = len(testua.split())
    console.print(f"[dim]Testua kargatuta: {hitz_kopurua} hitz[/]")

    # 2. Konfigurazioa kargatu
    sistema_prompt, errubrika, gramatika = load_config()
    console.print(f"[dim]Konfigurazioa: errubrika + {len(gramatika)} gramatika TSV[/]")

    # 3. Mezua eraiki
    user_message = build_user_message(
        errubrika, gramatika,
        args.kodea, args.maila, args.mota, args.hitzak, args.modua,
        testua,
    )
    console.print(f"[dim]Mezua prestatuta: {len(user_message):,} karaktere[/]")

    # 4. API deia
    console.print(f"[bold]API deia egiten[/] ({MODEL})...")
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
        sys.exit(1)

    response_text = response.content[0].text
    console.print(
        f"[dim]Erantzuna: {response.usage.input_tokens:,} input / "
        f"{response.usage.output_tokens:,} output token[/]"
    )

    # 5. JSON parseatu
    try:
        result = extract_json(response_text)
    except (json.JSONDecodeError, ValueError) as e:
        raw_path = save_raw(response_text, args.kodea)
        console.print(f"[red]ERROREA:[/] JSON parseatzean huts egin du: {e}")
        console.print(f"[dim]Raw erantzuna gordeta: {raw_path}[/]")
        sys.exit(1)

    # 6. JSON baliozkoztatu
    missing = validate_json(result)
    if missing:
        console.print(f"[yellow]ABISUA:[/] JSON-ean gako hauek falta dira: {', '.join(missing)}")

    # 7. Emaitza gorde
    output_path = save_json(result, args.kodea)
    console.print(f"[green]Emaitza gordeta:[/] {output_path}")

    # 8. Laburpena pantailaratu
    console.print()
    print_summary(result)


if __name__ == "__main__":
    main()
