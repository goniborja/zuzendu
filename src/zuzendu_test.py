# -*- coding: utf-8 -*-
"""
ZUZENDU v3 — Fase 1.3: Script minimoa
Testua → Anthropic API → JSON ebaluazioa → data/emaitzak/

Erabilera:
  python src/zuzendu_test.py testua.txt
  python src/zuzendu_test.py testua.txt --kodea 3A017 --maila DBH4
  echo "Nire testua..." | python src/zuzendu_test.py -
  python src/zuzendu_test.py testua.txt --testu-mota iritzi_artikulua --modua zirriborroa
"""

import argparse
import json
import sys
import re
from datetime import datetime
from pathlib import Path

import anthropic
from dotenv import load_dotenv
import os

# Proiektuaren erroa (src/ karpetaren gurasoa)
ROOT = Path(__file__).resolve().parent.parent

load_dotenv(ROOT / ".env")

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")


def load_text(source: str) -> str:
    """Testua irakurri fitxategitik edo stdin-etik."""
    if source == "-":
        return sys.stdin.read().strip()
    path = Path(source)
    if not path.exists():
        sys.exit(f"ERROREA: Fitxategia ez da aurkitu: {path}")
    return path.read_text(encoding="utf-8").strip()


def load_config() -> tuple[str, str, dict[str, str]]:
    """Sistema-prompt, errubrika JSON eta gramatika TSVak kargatu."""
    prompt_path = ROOT / "config" / "sistema_prompt.txt"
    rubric_path = ROOT / "config" / "errubrika.json"
    grammar_dir = ROOT / "config" / "gramatika"

    if not prompt_path.exists():
        sys.exit(f"ERROREA: {prompt_path} ez da aurkitu")
    if not rubric_path.exists():
        sys.exit(f"ERROREA: {rubric_path} ez da aurkitu")

    sistema_prompt = prompt_path.read_text(encoding="utf-8")
    errubrika_json = rubric_path.read_text(encoding="utf-8")

    # Gramatika TSVak kargatu (00_AURKIBIDEA.tsv eta euskal_gramatika.tsv salbu)
    gramatika = {}
    skip = {"00_AURKIBIDEA.tsv", "euskal_gramatika.tsv"}
    if grammar_dir.exists():
        for tsv in sorted(grammar_dir.glob("*.tsv")):
            if tsv.name not in skip:
                gramatika[tsv.name] = tsv.read_text(encoding="utf-8")

    return sistema_prompt, errubrika_json, gramatika


def build_ataza_fitxa(args: argparse.Namespace) -> str:
    """Ataza-fitxa sortu argumentuetatik."""
    fitxa = {
        "maila": args.maila,
        "testu_mota": args.testu_mota,
        "zuzenketa_modua": args.modua,
    }
    if args.egitekoa:
        fitxa["egitekoa"] = args.egitekoa
    if args.hitz_min or args.hitz_max:
        fitxa["hitz_kopurua"] = {
            "min": args.hitz_min or 80,
            "max": args.hitz_max or 250,
        }
    return json.dumps(fitxa, ensure_ascii=False, indent=2)


def build_user_message(
    errubrika_json: str,
    gramatika: dict[str, str],
    ataza_fitxa: str,
    kodea: str,
    testua: str,
) -> str:
    """Erabiltzaile-mezua eraiki: errubrika + gramatika + ataza-fitxa + testua."""
    hitz_kopurua = len(testua.split())

    parts = []

    # 1. Errubrika
    parts.append("═══ ERRUBRIKA (config/errubrika.json) ═══")
    parts.append(errubrika_json)

    # 2. Gramatika erreferentziak
    parts.append("\n═══ GRAMATIKA ERREFERENTZIAK (config/gramatika/) ═══")
    for filename, content in gramatika.items():
        parts.append(f"\n--- {filename} ---")
        parts.append(content)

    # 3. Ataza-fitxa
    parts.append("\n═══ ATAZA-FITXA ═══")
    parts.append(ataza_fitxa)

    # 4. Ikaslearen testua
    parts.append("\n═══ IKASLEAREN TESTUA ═══")
    parts.append(f"Kodea: {kodea}")
    parts.append(f"Hitz kopurua: {hitz_kopurua}")
    parts.append(f"\n{testua}")

    return "\n".join(parts)


def extract_json(response_text: str) -> dict:
    """JSON atera erantzunetik, markdown code fences kendu behar badira."""
    text = response_text.strip()
    # ```json ... ``` formatua kendu
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    return json.loads(text)


def save_result(result: dict, kodea: str) -> Path:
    """Emaitza JSON gisa gorde data/emaitzak/ karpetan."""
    output_dir = ROOT / "data" / "emaitzak"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{kodea}_{timestamp}.json"
    output_path = output_dir / filename

    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="ZUZENDU v3 — Testua ebaluatu Anthropic API bidez"
    )
    parser.add_argument(
        "testua",
        help="Testu-fitxategiaren bidea, edo '-' stdin-etik irakurtzeko",
    )
    parser.add_argument("--kodea", default="test", help="Ikaslearen kodea (adib. 3A017)")
    parser.add_argument("--maila", default="DBH4", choices=["DBH3", "DBH4"], help="Maila")
    parser.add_argument(
        "--testu-mota",
        default="iritzi_artikulua",
        choices=[
            "iritzi_artikulua", "gutun_formala", "gutun_informala",
            "deskribapena", "hausnarketa", "gidoia", "narrazioa", "laburpena",
        ],
        help="Testu-mota",
    )
    parser.add_argument(
        "--modua",
        default="azken_bertsioa",
        choices=["zirriborroa", "azken_bertsioa"],
        help="Zuzenketa-modua",
    )
    parser.add_argument("--egitekoa", default=None, help="Egitekoaren deskribapena")
    parser.add_argument("--hitz-min", type=int, default=None, help="Gutxieneko hitz kopurua")
    parser.add_argument("--hitz-max", type=int, default=None, help="Gehieneko hitz kopurua")

    args = parser.parse_args()

    if not API_KEY:
        sys.exit("ERROREA: ANTHROPIC_API_KEY ez dago konfiguratuta .env fitxategian")

    # 1. Testua kargatu
    testua = load_text(args.testua)
    if not testua:
        sys.exit("ERROREA: Testua hutsik dago")
    print(f"Testua kargatuta: {len(testua.split())} hitz")

    # 2. Konfigurazioa kargatu
    sistema_prompt, errubrika_json, gramatika = load_config()
    print(f"Konfigurazioa kargatuta: errubrika + {len(gramatika)} gramatika fitxategi")

    # 3. Mezuak prestatu
    ataza_fitxa = build_ataza_fitxa(args)
    user_message = build_user_message(
        errubrika_json, gramatika, ataza_fitxa, args.kodea, testua
    )
    print(f"Mezua prestatuta: {len(user_message)} karaktere")

    # 4. API deia
    print(f"API deia egiten ({MODEL})...")
    client = anthropic.Anthropic(api_key=API_KEY)

    response = client.messages.create(
        model=MODEL,
        max_tokens=8192,
        system=sistema_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    response_text = response.content[0].text
    print(f"Erantzuna jasota: {response.usage.input_tokens} input / {response.usage.output_tokens} output token")

    # 5. JSON parseatu
    try:
        result = extract_json(response_text)
    except json.JSONDecodeError as e:
        # Erantzuna gorde debug-erako
        debug_path = save_result({"raw_response": response_text, "error": str(e)}, f"{args.kodea}_debug")
        sys.exit(f"ERROREA: JSON parseatzean huts egin du. Debug gordeta: {debug_path}")

    # 6. Emaitza gorde
    output_path = save_result(result, args.kodea)
    print(f"Emaitza gordeta: {output_path}")

    # 7. Laburpena pantailaratu
    if "laburpena" in result:
        lab = result["laburpena"]
        print(f"\n{'=' * 50}")
        print(f"NOTA: {lab.get('biribiltzea', '?')}/10 -- {lab.get('heziberri_maila', '?')}")
        print(f"{'=' * 50}")
        if "orokorra" in lab:
            print(lab["orokorra"])
        print()


if __name__ == "__main__":
    main()
