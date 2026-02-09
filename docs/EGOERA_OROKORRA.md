# ZUZENDU v3 — Proiektuaren egoera orokorra

**Azken eguneraketa:** 2026-02-09 (arratsaldea)

---

## Eginda (Fase 1)

### Kalibrazioa v6
- KAL-001 a KAL-004 kalibratuta, **95% gelaxka ≤1 puntu** desbideratzea
- 6 parche aplikatu `config/sistema_prompt.txt`-ean
- Validazio akademikoa: Larraitz Uria tesia (UPV-EHU 2009), Bertol Arrieta (2010), Maritxalar MUGARRI (1999)

### `src/ep100.py` — EP100 Python post-prozesatzea
- EP100 gordina eta pisuduna Python-etik birkalkulatuta (modeloaren datuak gainidazten)
- Erderakada faltsuen iragazkia (modeloak sortutako erderakada faltsuak deskontatu)
- ZL nota doikuntza: ±1 max EP100 bandaren arabera
- `biribildu()`: 5 azpitik ROUND_HALF_DOWN, 5+ ROUND_HALF_UP (Decimal)
- `lortu_ep100_fidagarria()`: gordina/pisuduna ratio > 3 denean, gordina erabili

### `src/ia_detekzioa.py` — IA detekzio independentea (v1)
- API dei separatuan, ebaluazioa BAINO LEHEN
- 7 seinale (S1-S7), 0-3 bakoitza, max 21
- **Bug konpondua:** modeloaren `ia_puntuazioa` ez fidatu, Python-etik S1-S7 batura kalkulatu
- Atalaseak (v2): **BAXUA (0-7)**, **ERTAINA (8-13)**, **ALTUA (14-21)**
- ALTUA: testua blokeatu, ez ebaluatu
- ERTAINA: ebaluatu + irakasle berrikusketa oharra
- BAXUA: ebaluatu normalean

### `src/docx2txt.py` — Bihurtzailea
- `.docx` fitxategiak `.txt` bihurtu
- Txantiloi-goiburuak eta placeholder-ak iragazten ditu

### `src/zuzendu.py` — Pipeline nagusia
- Karpeta osoa prozesatu: taldea/maila automatikoki path-etik
- `--mota` parametroa testu-motarako
- `--fitxategia` fitxategi bakarra prozesatzeko
- Emaitzak `emaitzak/[TALDEA]/[AKTIBITATEA]/` karpetan gordetzen ditu

### `src/zuzendu_test.py` — Pipeline zaharra (fitxategi bakarra)
- Pipeline: IA detekzioa → ebaluazio API deia → EP100 post-prozesatzea → JSON gordetzea
- Output fitxategiaren izena = sarrerako fitxategiaren stem

### `config/sistema_prompt.txt`
- 6 parche kalibrazioan zehar
- IA DETEKZIOA atala gehituta (0. atala, baina modeloak ignoratu egin zuen → ia_detekzioa.py-ra mugitu)
- Erderakada faltsuak murrizteko argibideak

---

## DBH4B — Idazlan-koadernoa (lehen tanda)

13 testu prozesatuta. Emaitzak:

| Ikaslea | S1-S7 | Maila | Egoera | Nota | AB | AK | BLH | ZL | EP100g | EP100p |
|---|:---:|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Ahetz | 0 | BAXUA | Ebaluatua | 2 | 3 | 2 | 3 | 2 | 22.28 | 2.14 |
| **Amets** | **20** | **ALTUA** | **BLOKEATUA** | - | - | - | - | - | - | - |
| Ander | 1 | BAXUA | Ebaluatua | 6 | 3 | 7 | 6 | 7 | 2.60 | 1.62 |
| Euskara | 1 | BAXUA | Ebaluatua | 7 | 8 | 7 | 7 | 7 | 3.62 | 1.81 |
| Harriet | 1 | BAXUA | Ebaluatua | 3 | 3 | 4 | 4 | 2 | 20.40 | 2.83 |
| **Iset** | **20** | **ALTUA** | **BLOKEATUA** | - | - | - | - | - | - | - |
| Maia | 1 | BAXUA | Ebaluatua | 6 | 2 | 8 | 7 | 6 | 3.06 | 1.34 |
| Maria | 3 | BAXUA | Ebaluatua | 7 | 8 | 7 | 6 | 7 | 2.00 | 0.84 |
| Oier | 1 | BAXUA | Ebaluatua | 4 | 2 | 4 | 5 | 4 | 9.97 | 2.69 |
| **Paula** | **18** | **ALTUA** | **BLOKEATUA** | - | - | - | - | - | - | - |
| Penelope | 1 | BAXUA | Ebaluatua | 5 | 3 | 5 | 6 | 5 | 11.06 | 3.93 |
| **Solafa** | **18** | **ALTUA** | **BLOKEATUA** | - | - | - | - | - | - | - |
| Telmo | 8 | ERTAINA | Ebaluatua + oharra | 6 | 4 | 6 | 6 | 6 | 3.99 | 1.99 |

**Ondorioa:** 9 ebaluatuta, 4 blokeatuta (Amets, Iset, Paula, Solafa), 1 irakasle-oharrarekin (Telmo).

---

## Prozesuan

- [ ] DBH4A — Idazlan-koadernoa (entregatzea) prozesatzeke
- [ ] Irakaslearen berrikusketa: 4B notak egiaztatu
- [ ] Irakaslearen berrikusketa: 4 ikasle blokeatuak aztertu
- [ ] DBH3A, DBH3B prozesatu

---

## Hurrengo pausoak (lehentasunen arabera)

### 1. Fase 1 amaitu
- 4A eta gainerako taldeak prozesatu
- Notak berrikusi eta kalibrazioa doitu behar bada

### 2. IA detekzioa v2 — Birplanteatu (GARRANTZITSUA)

> **OHARRA:** `config/sistema_prompt.txt`-eko "0. IA DETEKZIOA" atala kendu behar da (modeloak ignoratzen zuen, orain `ia_detekzioa.py`-n dago). Gainera, prompt-ari minidefentsa galderak sortzeko argibidea gehitu behar zaio.
Deep research-ean oinarrituta, IA detekzioa erabat aldatu behar da. Oraingo S1-S7 sistema ez da nahikoa.

**Ikerketaren ondorio nagusiak:**
- IA detekzio automatikoa (testua bakarrik) ez da fidagarria
- Detektore komertzialak (GPTZero, etab.) ez daude euskararako prestatuta
- Funtzionatzen duena: **triangulazioa** (testua + prozesua + testuingurua + erresistentzia)
- "IA detektatu" ordez: "ikaslearen autoretza ez-koherentziaren probabilitatea" neurtu

**5 domeinu sistema (deep research-etik):**

| Domeinua | Egungo egoera | Inplementagarria? |
|---|---|---|
| 1. Prozesua/jatorria (metadatuak, zirriborroak) | ❌ Ez dugu | ✅ Bai, HTML bidez (Fase 2) |
| 2. Koherentzia testual intra-dokumentua | Partzialki (S7) | ✅ Prompt hobetu |
| 3. Ikaslearen profil longitudinala | ❌ Ez dugu | ✅ Profil akumulatiboa |
| 4. Ebidentzia kognitibo-didaktikoa | Partzialki (S6) | ✅ Prompt hobetu |
| 5. Erresistentzia-probak (minidefentsa) | ❌ Ez dugu | ✅ Galdera automatikoak |

**Erabakiak:**
- S1-S7 mantendu oraingoz (Fase 1), baina Fase 2-an 5 domeinuetara aldatu
- HTML idazketa-tresna inplementatu (Fase 2) → 1. domeinua automatikoki betetzeko
- Ikaslearen erreferentzia-paragrafoa klase-barnean idaztea → profil longitudinalaren hasiera
- Minidefentsa galdera automatikoak sortzea → testu GUZTIENTZAT, ez bakarrik susmagarrientzat

### 3. Fase 2 — HTML idazketa-tresna + IA detekzio aurreratua
Ikus IMPLEMENTATION.md Fase 2 zehaztasunetarako.

---

## Fitxategi-egitura

```
zuzendu_v3/
  config/
    sistema_prompt.txt       # Sistema prompt-a (ebaluazioa)
    errubrika.json           # Heziberri errubrika
    gramatika/               # 11 gramatika TSV
  src/
    zuzendu.py               # Pipeline nagusia (karpeta osoa)
    zuzendu_test.py          # Pipeline zaharra (fitxategi bakarra)
    ep100.py                 # EP100 post-prozesatzea
    ia_detekzioa.py          # IA detekzio independentea (v1: S1-S7)
    docx2txt.py              # .docx → .txt bihurtzailea
  idazlanak/                 # Sarrerako testuak, taldeka
    DBH3A/
    DBH3B/
    DBH4A/
      Idazlan-koadernoa (entregatzea)/
    DBH4B/
      Idazlan-koadernoa (entregatzea)/
  emaitzak/                  # JSON emaitzak, taldeka
    DBH3A/
    DBH3B/
    DBH4A/
    DBH4B/
      Idazlan-koadernoa (entregatzea)/
  tests/
    testu_kalibrazioa/       # Kalibrazio-testuak (aparte)
  docs/
    EGOERA_OROKORRA.md       # Dokumentu hau
    IMPLEMENTATION.md        # Inplementazio plana
    referencias/             # Ikerketa akademikoa
```

### Erabilera

```bash
# Karpeta osoa prozesatu:
python src/zuzendu.py "idazlanak/DBH4B/Idazlan-koadernoa (entregatzea)/" --mota narrazioa

# Fitxategi bakarra:
python src/zuzendu.py "idazlanak/DBH4B/Idazlan-koadernoa (entregatzea)/" --fitxategia Telmo --mota narrazioa
```
