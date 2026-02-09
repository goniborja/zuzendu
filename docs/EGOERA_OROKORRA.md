# ZUZENDU v3 — Proiektuaren egoera orokorra

**Azken eguneraketa:** 2026-02-09

---

## Eginda

### Kalibrazioa v6
- KAL-001 a KAL-004 kalibratuta, **95% gelaxka ≤1 puntu** desbideratzea
- 6 parche aplikatu `config/sistema_prompt.txt`-ean

### `src/ep100.py` — EP100 Python post-prozesatzea
- EP100 gordina eta pisuduna Python-etik birkalkulatuta (modeloaren datuak gainidazten)
- Erderakada faltsuen iragazkia (modeloak sortutako erderakada faltsuak deskontatu)
- ZL nota doikuntza: ±1 max EP100 bandaren arabera
- `biribildu()`: 5 azpitik ROUND_HALF_DOWN, 5+ ROUND_HALF_UP (Decimal)
- `lortu_ep100_fidagarria()`: gordina/pisuduna ratio > 3 denean, gordina erabili (errepikatze-arauak gehiegi desinflatu duelako)

### `src/ia_detekzioa.py` — IA detekzio independentea
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
- 15 fitxategi sortu `tests/idazlanak/` karpetan

### `src/zuzendu_test.py` — Pipeline osoa
- Pipeline: IA detekzioa -> ebaluazio API deia -> EP100 post-prozesatzea -> JSON gordetzea
- Output fitxategiaren izena = sarrerako fitxategiaren stem (ez --kodea)
- IA emaitzak `meta.segurtasun_azterketa`-n txertatuta
- `sanitize()` funtzioa Windows cp1252 bateragarritasunerako

### `config/sistema_prompt.txt`
- 6 parche kalibrazioan zehar
- IA DETEKZIOA atala gehituta (0. atala)
- Erderakada faltsuak murrizteko argibideak

### 4B lehen tanda
- 13 testu prozesatuta IA detekzioarekin
- Harriet berriz pasatu (lehen max_tokens-ek moztu zuen)

---

## Prozesuan / Bug-ak

### ~~IA detekzio bug-a~~ KONPONDUA + atalaseak doituta

### 4B emaitza finalak (atalase berriak: BAXUA 0-7, ERTAINA 8-13, ALTUA 14-21)

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

## Falta

- [x] IA detekzio bug-a konpondu: Python-etik S1-S7 batura kalkulatu
- [x] Atalaseak doitu: BAXUA 0-7, ERTAINA 8-13, ALTUA 14-21
- [x] 13 testuak berriz pasa pipeline-tik (atalase berriekin)
- [ ] Irakaslearen berrikusketa: 4 ikasle blokeatuak aztertu (Amets, Iset, Paula, Solafa)
- [ ] Irakaslearen berrikusketa: Telmo (ERTAINA, 8/21) berrikusi
- [ ] Irakaslearen berrikusketa: ebaluatutako 8 ikasleen notak egiaztatu
- [ ] Beste talde bat prozesatu (4A, 3A, 3B)

---

## Fitxategi-egitura

```
zuzendu_v3/
  config/
    sistema_prompt.txt    # Sistema prompt-a (IA detekzioa + ebaluazioa)
    errubrika.json        # Heziberri errubrika
    gramatika/            # 11 gramatika TSV
  src/
    zuzendu_test.py       # Pipeline nagusia
    ep100.py              # EP100 post-prozesatzea
    ia_detekzioa.py       # IA detekzio independentea
    docx2txt.py           # .docx -> .txt bihurtzailea
  tests/
    idazlanak/            # 15 testu .txt formatuan
  data/
    emaitzak/             # JSON emaitzak
  docs/
    EGOERA_OROKORRA.md    # Dokumentu hau
```
