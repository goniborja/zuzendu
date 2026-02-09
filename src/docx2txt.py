# -*- coding: utf-8 -*-
"""
ZUZENDU — .docx fitxategiak .txt bihurtu.

Erabilera:
    python src/docx2txt.py tests/idazlanak/
    python src/docx2txt.py fitxategi_bat.docx

Goiburu-lerroak (izena, maila, izenburua...) kendu eta
idazlanaren testua bakarrik ateratzen du.
"""

import sys
from pathlib import Path

from docx import Document

# Goiburuko lerroak iragazteko patroi hauek detektatzen dira
GOIBURU_PATROIAK = [
    "XXV. IDAZLAN",
    "DBH 2. Zikloa",
    "DBH 3. Zikloa",
    "Izena eta abizenak:",
    "Maila:",
    "Idazlanaren izenburua:",
    "Esaldi bat (zuretzat",
    "Gogoratu: lerroarte",
    "(Jarraitu idazten",
    "MARRAZKIA",
    "(Txertatu hemen",
]

# Placeholder lerroak (bete gabe dauden txantiloi-eremuak)
PLACEHOLDER_PATROIAK = [
    "(idatzi hemen)",
    "(DBH3 / DBH4)",
    "(jarri zure izenburua)",
    "(idatzi esaldi bat)",
]


def da_goiburua(lerroa: str) -> bool:
    """Lerroa goiburukoa den ala ez."""
    for patroia in GOIBURU_PATROIAK:
        if patroia.lower() in lerroa.lower():
            return True
    return False


def da_placeholdera(lerroa: str) -> bool:
    """Lerroa placeholder hutsa den ala ez."""
    lower = lerroa.lower().strip()
    for p in PLACEHOLDER_PATROIAK:
        if lower == p:
            return True
    return False


def docx_to_txt(docx_path: Path) -> str:
    """Docx fitxategitik idazlanaren testua atera."""
    doc = Document(str(docx_path))

    lerroak = []
    for p in doc.paragraphs:
        testua = p.text.strip()
        if not testua:
            continue
        if da_goiburua(testua):
            continue
        if da_placeholdera(testua):
            continue
        lerroak.append(testua)

    return "\n\n".join(lerroak)


def prozesatu(sarrera: Path) -> list[Path]:
    """Fitxategi bat edo karpeta bat prozesatu. Sortutako .txt fitxategiak itzuli."""
    if sarrera.is_file():
        fitxategiak = [sarrera]
    elif sarrera.is_dir():
        fitxategiak = sorted(sarrera.glob("*.docx"))
    else:
        print(f"ERROREA: {sarrera} ez da fitxategia ez karpeta")
        sys.exit(1)

    if not fitxategiak:
        print(f"Ez da .docx fitxategirik aurkitu: {sarrera}")
        sys.exit(1)

    sortutakoak = []
    for docx_path in fitxategiak:
        testua = docx_to_txt(docx_path)
        if not testua.strip():
            print(f"  HUTSIK: {docx_path.name} (saltatuta)")
            continue

        txt_path = docx_path.with_suffix(".txt")
        txt_path.write_text(testua, encoding="utf-8")
        hitz_kop = len(testua.split())
        print(f"  {txt_path.name} ({hitz_kop} hitz)")
        sortutakoak.append(txt_path)

    return sortutakoak


def main():
    if len(sys.argv) < 2:
        print("Erabilera: python src/docx2txt.py <karpeta_edo_fitxategia>")
        sys.exit(1)

    sarrera = Path(sys.argv[1])
    print(f"Docx -> txt bihurtzen: {sarrera}\n")
    sortutakoak = prozesatu(sarrera)
    print(f"\nGuztira: {len(sortutakoak)} fitxategi sortuta")


if __name__ == "__main__":
    main()
