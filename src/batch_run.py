# -*- coding: utf-8 -*-
"""Batch runner: 13 testu guztiak pipeline-tik pasatu."""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TESTS_DIR = ROOT / "tests" / "idazlanak"

# 13 ikasle: (fitxategi izena, kodea)
IKASLEAK = [
    ("Ahetz Fundazuri Txopitea - Idazlan Koadernoa.txt", "AHETZ"),
    ("Amets Arejita Legarretaetxebarria - Idazlan Koadernoa.txt", "AMETS"),
    ("Ander Kepa Elorduy Lebedyeva - Idazlan Koadernoa.txt", "ANDER"),
    ("Euskara Idazlan liburua.txt", "EUSKARA"),
    ("Harriet Sierra Bernal - Idazlan Koadernoa.txt", "HARRIET"),
    ("Iset Salvador Pamparacuatro - Idazlan Koadernoa.txt", "ISET"),
    ("Maia Pertika Etxebarria - Idazlan Koadernoa.txt", "MAIA"),
    ("Maria Herreros Zubizarreta - Idazlan-koadernoa (entregatzea).txt", "MARIA"),
    (" XXV. IDAZLAN KOADERNOAK 2026.txt", "OIER"),
    ("Paula Ciarrusta Sainz-Maza - Idazlan Koadernoa.txt", "PAULA"),
    ("Penelope Naia Andonegui Richards - Idazlan koadernoa.txt", "PENELOPE"),
    ("Solafa Boumarouane Rafiq - Idazlan Koadernoa.txt", "SOLAFA"),
    ("Telmo Elguezabal.txt", "TELMO"),
]


def main():
    script = ROOT / "src" / "zuzendu_test.py"
    ok = 0
    fail = 0

    for fitx, kodea in IKASLEAK:
        path = TESTS_DIR / fitx
        if not path.exists():
            print(f"[SKIP] {kodea}: fitxategia ez da aurkitu: {path}")
            fail += 1
            continue

        print(f"\n{'='*60}")
        print(f"[{ok+fail+1}/13] {kodea}: {fitx}")
        print(f"{'='*60}")

        try:
            result = subprocess.run(
                [sys.executable, str(script), str(path), "--kodea", kodea],
                cwd=str(ROOT),
                timeout=180,
            )
            if result.returncode == 0:
                ok += 1
            else:
                print(f"[ERROR] {kodea}: returncode={result.returncode}")
                fail += 1
        except subprocess.TimeoutExpired:
            print(f"[TIMEOUT] {kodea}: 180s gainditu da")
            fail += 1
        except Exception as e:
            print(f"[ERROR] {kodea}: {e}")
            fail += 1

    print(f"\n{'='*60}")
    print(f"AMAITUTA: {ok} OK, {fail} fail, {ok+fail} guztira")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
