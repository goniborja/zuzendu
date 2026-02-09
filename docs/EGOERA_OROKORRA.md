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
- Mailak: BAXUA (0-5), ERTAINA (6-10), ALTUA (11-15), OSO_ALTUA (16-21)
- ALTUA+: testua blokeatu, ez ebaluatu
- ERTAINA: ebaluatu + irakasle berrikusketa oharra

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

### IA detekzio bug-a: `ia_puntuazioa` vs seinaleen batura
- Modeloak `ia_puntuazioa` eta `seinaleak` (S1-S7) independenteki sortzen ditu
- `ia_puntuazioa` EZ da S1-S7 batura — modeloak batez bestekoa edo beste formula bat erabiltzen du
- Ondorioz, blokeatzeko atalasea (>=11) ez da inoiz aktibatzen
- **Adibidea:** Paula — seinaleak batura = 19 (OSO_ALTUA), baina ia_puntuazioa = 2.3 (BAXUA)
- **Konponbidea:** Python-etik kalkulatu seinaleen batura, modeloaren ia_puntuazioa-ri ez fidatu

### 13 testuen emaitzak (azken exekuzioa)

| Ikaslea | Nota | AB | AK | BLH | ZL | EP100g | EP100p | Hitzak | IA_punt | IA_maila | S1-S7 batura |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---|:---:|
| Ahetz | 4 | 6 | 4 | 2 | 4 | 26.24 | 2.83 | 743 | 0.0 | BAXUA | 0 |
| Amets | 8 | 8 | 7 | 9 | 8 | 0.24 | 0.20 | 1247 | 9.0 | ERTAINA | 20 |
| Ander | 8 | 8 | 7 | 8 | 8 | 2.63 | 2.30 | 456 | 0.5 | BAXUA | 1 |
| Euskara | 7 | 8 | 7 | 7 | 7 | 2.12 | 1.54 | 518 | 0.5 | BAXUA | 1 |
| Harriet | 7 | 8 | 7 | 6 | 5 | 7.52 | 1.96 | 918 | 0.3 | BAXUA | 1 |
| Iset | 7 | 8 | 7 | 8 | 7 | 1.45 | 0.77 | 1038 | 2.0 | BAXUA | 16 |
| Maia | 8 | 9 | 8 | 8 | 8 | 2.37 | 1.66 | 845 | 0.5 | BAXUA | 1 |
| Maria | 8 | 8 | 8 | 8 | 8 | 1.01 | 0.79 | 891 | 1.4 | BAXUA | 11 |
| Oier | 6 | 6 | 5 | 5 | 6 | 6.98 | 1.80 | 917 | 0.3 | BAXUA | 1 |
| Paula | 9 | 9 | 9 | 8 | 9 | 0.60 | 0.54 | 838 | 2.3 | BAXUA | 19 |
| Penelope | 7 | 8 | 7 | 5 | 7 | 9.35 | 2.64 | 738 | 0.5 | BAXUA | 1 |
| Solafa | 7 | 8 | 7 | 7 | 7 | 3.58 | 1.28 | 782 | 2.3 | BAXUA | 17 |
| Telmo | 7 | 8 | 7 | 7 | 7 | 3.20 | 1.96 | 562 | 1.3 | BAXUA | 11 |

---

## Falta

- [ ] IA detekzio bug-a konpondu: Python-etik S1-S7 batura kalkulatu
- [ ] 13 testuen emaitzak berrikusi (IA bug-a konpondu ondoren berriz pasa)
- [ ] Irakaslearen berrikusketa: notak egiaztatu (AB altuegi izan daiteke?)
- [ ] Commit eta push emaitza guztiekin
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
