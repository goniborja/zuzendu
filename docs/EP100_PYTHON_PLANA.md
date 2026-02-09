# ZUZENDU v3 — EP100 KALKULUA PYTHON-EN (Opción B)
# Claude Desktop-erako inplementazio-plana

---

## ARAZOA

Modeloak EP100 kalkulatzen du eta ZL nota jartzen du aldi berean.
Horrek "anclaje sesioa" sortzen du: nota erabakitzen du lehenengo 
eta gero akatsak bilatzen ditu justifikatzeko. Ondorioz:
- EP100=1.89 baina ZL=6 (inkoherentea)
- EP100 aldatzen da iteraziotik iteraziora nota berdinarekin

## KONPONKETA

Python-ek EP100 kalkulatu eta ZL nota doitu, modeloaren JSON-a jaso ondoren.
API dei BAKARRA mantentzen da (kostu gehigarririk ez).

## FLUXU BERRIA

```
1. API deia → modeloak JSON itzultzen du (akats_taldeak + notak)
2. Python-ek akats_taldeak-etik EP100 birkalkulatzen du
3. Python-ek EP100 banda egiaztatzen du
4. ZL nota banda-barruan ez badago → Python-ek doitzen du
5. Nota finala birkalkulatzen du
6. JSON eguneratua gordetzen du
```

## INPLEMENTAZIOA

### 1. Funtzio berria: `calcular_ep100(akats_taldeak, hitz_kopurua)`

Fitxategia: `src/ep100.py` (modulu berria)

```python
"""EP100 kalkulua — Python-en, ez modeloan."""

# Larritasun-pisuak
PISUAK = {
    "minor": 1,
    "major": 2,
    "critical": 3
}

# ZL kodeak SOILIK (LH/OK ez kontatu — Parche 4)
ZL_KODEAK = {"ZL-ORT", "ZL-KAS", "ZL-ADI", "ZL-SIN", "ZL-PUN", "ZL-ERD"}

def da_zl_kodea(akats_id: str) -> bool:
    """Akats bat ZL motakoa den egiaztatu."""
    for kode in ZL_KODEAK:
        if akats_id.startswith(kode):
            return True
    return False

def kalkulatu_ep100_gordina(akats_taldeak: list, hitz_kopurua: int) -> float:
    """EP100 gordina kalkulatu: (sum(kopurua × pisua)) × 100 / hitz_kopurua"""
    guztira = 0
    for taldea in akats_taldeak:
        if not da_zl_kodea(taldea.get("akats_id", "")):
            continue  # LH, OK, etab. ez kontatu
        kopurua = taldea.get("kopurua", 0)
        larritasuna = taldea.get("larritasuna", "minor")
        pisua = PISUAK.get(larritasuna, 1)
        guztira += kopurua * pisua
    
    if hitz_kopurua <= 0:
        return 0.0
    return round(guztira * 100 / hitz_kopurua, 2)

def aplikatu_errepikapen_araua(akats_taldeak: list) -> float:
    """
    Errepikapen araua: akats-talde bakoitzeko:
      - Lehen instantzia: pisu osoa (minor=1, major=2, critical=3)
      - Bigarren instantzia: pisuaren erdia
      - Gainontzekoak: 0
    """
    pisu_totala = 0.0
    for taldea in akats_taldeak:
        if not da_zl_kodea(taldea.get("akats_id", "")):
            continue
        kopurua = taldea.get("kopurua", 0)
        larritasuna = taldea.get("larritasuna", "minor")
        pisua = PISUAK.get(larritasuna, 1)
        
        if kopurua >= 1:
            pisu_totala += pisua        # Lehen instantzia
        if kopurua >= 2:
            pisu_totala += pisua * 0.5  # Bigarren instantzia
        # 3+ instantziak: 0
    
    return pisu_totala

def kalkulatu_ep100_pisuduna(akats_taldeak: list, hitz_kopurua: int) -> float:
    """EP100 pisuduna: errepikapen araua aplikatu."""
    pisu_totala = aplikatu_errepikapen_araua(akats_taldeak)
    if hitz_kopurua <= 0:
        return 0.0
    return round(pisu_totala * 100 / hitz_kopurua, 2)

def lortu_ep100_banda(ep100_pisuduna: float) -> dict:
    """EP100 bandatik ZL hasiera-puntua lortu."""
    if ep100_pisuduna <= 2:
        return {"banda": "bikaintasuna", "zl_hasiera": 9, "zl_tartea": (9, 10)}
    elif ep100_pisuduna <= 5:
        return {"banda": "aurreratua", "zl_hasiera": 7, "zl_tartea": (7, 8)}
    elif ep100_pisuduna <= 10:
        return {"banda": "tartekoa", "zl_hasiera": 5, "zl_tartea": (5, 6)}
    elif ep100_pisuduna <= 18:
        return {"banda": "oinarrizkoa", "zl_hasiera": 3, "zl_tartea": (3, 4)}
    else:
        return {"banda": "hasiberria", "zl_hasiera": 1, "zl_tartea": (1, 2)}

def doitu_zl_nota(modelo_zl: int, ep100_pisuduna: float) -> dict:
    """
    Modeloak emandako ZL nota EP100 bandarekin koherentea den egiaztatu.
    Ez bada, doitu ±1 marjinarekin.
    Itzuli: {"zl_nota": int, "doitua": bool, "arrazoia": str}
    """
    banda = lortu_ep100_banda(ep100_pisuduna)
    zl_min, zl_max = banda["zl_tartea"]
    
    # ±1 marjina onartu (modeloak kualitatiboa kontuan hartzen du)
    marjin_min = zl_min - 1
    marjin_max = zl_max + 1
    
    if marjin_min <= modelo_zl <= marjin_max:
        return {
            "zl_nota": modelo_zl,
            "doitua": False,
            "arrazoia": f"Modeloaren ZL={modelo_zl} koherentea EP100={ep100_pisuduna} "
                        f"({banda['banda']}, tartea {zl_min}-{zl_max}) ±1 marjinarekin"
        }
    else:
        # Doitu: banda-hasierara eraman
        zl_berria = banda["zl_hasiera"]
        return {
            "zl_nota": zl_berria,
            "doitua": True,
            "arrazoia": f"DOITUA: Modeloaren ZL={modelo_zl} ez da koherentea "
                        f"EP100={ep100_pisuduna} ({banda['banda']}, tartea {zl_min}-{zl_max}). "
                        f"ZL={zl_berria} ezarri da."
        }
```

### 2. Post-prozesatzea `zuzendu_test.py`-n

`src/zuzendu_test.py`-n, API deiari erantzuna jaso ondoren:

```python
from ep100 import (
    kalkulatu_ep100_gordina,
    kalkulatu_ep100_pisuduna, 
    doitu_zl_nota
)

def post_prozesatu(emaitza: dict) -> dict:
    """API-aren JSON emaitza post-prozesatu: EP100 birkalkulatu eta ZL doitu."""
    
    akats_taldeak = emaitza.get("akats_taldeak", [])
    hitz_kopurua = emaitza.get("EP100", {}).get("hitz_kopurua", 0)
    
    # 1. EP100 birkalkulatu Python-en
    ep100_gordina = kalkulatu_ep100_gordina(akats_taldeak, hitz_kopurua)
    ep100_pisuduna = kalkulatu_ep100_pisuduna(akats_taldeak, hitz_kopurua)
    
    # 2. Modeloaren EP100 gorde (konparaziorako) eta Python-ekoa ezarri
    modelo_ep100 = emaitza.get("EP100", {}).copy()
    emaitza["EP100"]["EP100_gordina_modelo"] = modelo_ep100.get("EP100_gordina")
    emaitza["EP100"]["EP100_pisuduna_modelo"] = modelo_ep100.get("EP100_pisuduna")
    emaitza["EP100"]["EP100_gordina"] = ep100_gordina
    emaitza["EP100"]["EP100_pisuduna"] = ep100_pisuduna
    emaitza["EP100"]["kalkulua"] = "python"  # Nork kalkulatu duen markatu
    
    # 3. ZL nota doitu behar bada
    modelo_zl = emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"]
    zl_emaitza = doitu_zl_nota(modelo_zl, ep100_pisuduna)
    
    if zl_emaitza["doitua"]:
        emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"] = zl_emaitza["zl_nota"]
        emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["python_doikuntza"] = zl_emaitza["arrazoia"]
    
    # 4. Nota finala birkalkulatu
    ab = emaitza["ebaluazioa"]["atazaren_betetzea"]["nota"]
    ak = emaitza["ebaluazioa"]["antolaketa_koherentzia"]["nota"]
    blh = emaitza["ebaluazioa"]["baliabide_linguistikoen_hedadura"]["nota"]
    zl = emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"]
    
    batez_bestekoa = (ab + ak + blh + zl) / 4
    # Biribiltze-araua: .5 → beherantz (HABE irizpidea)
    import math
    biribiltzea = math.floor(batez_bestekoa) if (batez_bestekoa % 1 == 0.5) else round(batez_bestekoa)
    # Bestela, .5 → round() Python-en bankuaren biribiltzea da, beraz:
    biribiltzea = round(batez_bestekoa, 1)  # 1 dezimalekin utzi
    
    emaitza["laburpena"]["batez_bestekoa"] = round(batez_bestekoa, 2)
    emaitza["laburpena"]["biribiltzea"] = biribiltzea
    emaitza["laburpena"]["python_postprozesatua"] = True
    
    return emaitza
```

### 3. Promptetik EP100 kalkuluaren instrukzioak KENDU

`config/sistema_prompt.txt`-ean:
- EP100 kalkulatzeko instrukzioak MANTENDU (modeloak akatsak kontatu behar ditu)
- BAINA gehitu ohar hau:

```
GARRANTZITSUA: EP100 balioak eta ZL nota Python-ek birkalkulatuko ditu 
zure erantzuna jaso ondoren. Zure lana AKATSAK IDENTIFIKATZEA da zehaztasunez. 
EP100 kalkulua egin ezazu zure JSON-ean, baina jakin ezazu Python-ek 
egiaztatuko duela eta behar izanez gero doituko duela.
Akats bakoitzaren larritasuna (minor/major/critical) ondo markatzea FUNTSEZKOA da,
hortik abiatzen baita EP100 kalkulua.
```

---

## AURREIKUSITAKO EMAITZAK

KAL-002 v3 adibidea:
- Modeloak: EP100_pisuduna=1.89, ZL=6
- Python-ek birkalkulatuko du: EP100 ≈ 1.89 (bat badator)
- Banda: ≤2 → bikaintasuna → ZL tartea 9-10
- Modelo ZL=6, tartea 9-10, ±1 marjina = 8-10+
- 6 < 8 → DOITUA → ZL=9 ezarri

Hmmm, hori gehiegi izan daiteke. Beharbada marjina ±1 ez da nahikoa,
edo akats-detekzioan arazoa dago (akats gutxiegi detektatzen ditu).

BERAZ: lehenengo pausoa `ep100.py` inplementatu eta test bat egin 
KAL-001..004 JSON existitzekin. Ikusi zer ateratzen den Python kalkuluarekin
ALDATU gabe ezer. Diagnostikoa lehenengo.

---

## KOMANDOAK CLAUDE DESKTOP-ERAKO

1. Sortu `src/ep100.py` goiko kodearekin
2. Sortu `tests/test_ep100.py` — `data/emaitzak/` JSON-ak kargatu 
   eta Python EP100 vs modelo EP100 konparatu
3. Exekutatu testa eta erakutsi taula
4. Emaitzen arabera erabaki: post-prozesatzea zuzenean integratu 
   ala akats-detekzioa ere doitu behar den
