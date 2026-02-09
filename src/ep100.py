# -*- coding: utf-8 -*-
"""
ZUZENDU v3 — EP100 kalkulua Python-en.
Modeloak akatsak identifikatzen ditu; Python-ek EP100 birkalkulatzen du
eta ZL nota EP100 bandarekin koherentea den egiaztatzen du.
"""

import math

# Larritasun-pisuak
PISUAK = {"minor": 1, "major": 2, "critical": 3}

# ZL kodeak SOILIK (LH/OK ez kontatu)
ZL_AURRIZKIAK = ("ZL-ORT", "ZL-KAS", "ZL-ADI", "ZL-SIN", "ZL-PUN", "ZL-ERD")

# Erderakada faltsuak: modeloak ZL-ERD gisa markatzen ditu baina EZ dira akatsak
ERDERAKADA_FALTSUAK = [
    "ailegatu", "suertatzen", "suertatu", "suposatu", "suposatzen",
    "esfortzu", "esfortzua", "kontzientziatu", "azkenengo", "disrutatu",
]


def da_zl_kodea(akats_id: str | None) -> bool:
    """Akats bat ZL motakoa den egiaztatu."""
    if not akats_id:
        return False
    return akats_id.startswith(ZL_AURRIZKIAK)


def iragazki_erderakada_faltsuak(akats_taldeak: list) -> list:
    """
    ZL-ERD taldeetan erderakada faltsuak detektatu eta _piztua=False markatu.
    Adibidean edo kategorian erderakada faltsuren bat agertzen bada, EP100-tik kanpo utzi.
    """
    for taldea in akats_taldeak:
        akats_id = taldea.get("akats_id") or ""
        if not akats_id.startswith("ZL-ERD"):
            continue
        # Adibidean eta kategorian begiratu
        adibidea = taldea.get("adibidea", {})
        detektatutakoa = adibidea.get("detektatutakoa", "").lower()
        zuzenketa = adibidea.get("zuzenketa", "").lower()
        kategoria = taldea.get("kategoria", "").lower()
        testu_osoa = f"{detektatutakoa} {zuzenketa} {kategoria}"
        for hitza in ERDERAKADA_FALTSUAK:
            if hitza in testu_osoa:
                taldea["_piztua"] = False
                break
    return akats_taldeak


def da_kontatzekoa(taldea: dict) -> bool:
    """Talde bat EP100-n kontatu behar den egiaztatu."""
    if not da_zl_kodea(taldea.get("akats_id", "")):
        return False
    if taldea.get("_piztua") is False:
        return False
    return True


def kalkulatu_ep100_gordina(akats_taldeak: list, hitz_kopurua: int) -> float:
    """EP100 gordina: (sum(kopurua * pisua)) * 100 / hitz_kopurua."""
    guztira = 0
    for taldea in akats_taldeak:
        if not da_kontatzekoa(taldea):
            continue
        kopurua = taldea.get("kopurua", 0)
        pisua = PISUAK.get(taldea.get("larritasuna", "minor"), 1)
        guztira += kopurua * pisua

    if hitz_kopurua <= 0:
        return 0.0
    return round(guztira * 100 / hitz_kopurua, 2)


def kontatu_zl_akatsak(akats_taldeak: list) -> dict:
    """ZL akatsak minor/major/critical kontatu (erderakada faltsuak kanpo)."""
    kontaketak = {"minor": 0, "major": 0, "critical": 0}
    for taldea in akats_taldeak:
        if not da_kontatzekoa(taldea):
            continue
        sev = taldea.get("larritasuna", "minor")
        kontaketak[sev] = kontaketak.get(sev, 0) + taldea.get("kopurua", 0)
    return kontaketak


def aplikatu_errepikapen_araua(akats_taldeak: list) -> float:
    """
    Errepikapen araua talde bakoitzeko:
      1. instantzia -> pisu osoa
      2. instantzia -> pisuaren erdia
      3.+ instantziak -> 0
    """
    pisu_totala = 0.0
    for taldea in akats_taldeak:
        if not da_kontatzekoa(taldea):
            continue
        kopurua = taldea.get("kopurua", 0)
        pisua = PISUAK.get(taldea.get("larritasuna", "minor"), 1)

        if kopurua >= 1:
            pisu_totala += pisua
        if kopurua >= 2:
            pisu_totala += pisua * 0.5
    return pisu_totala


def kalkulatu_ep100_pisuduna(akats_taldeak: list, hitz_kopurua: int) -> float:
    """EP100 pisuduna: errepikapen araua aplikatuta."""
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
    Modeloaren ZL nota EP100 bandarekin koherentea den egiaztatu.
    ZL nota banda barrutian egon BEHAR da. Kanpo badago, GEHIENEZ ±1 doitu:
      - Baxuegi → max +1 igo
      - Altuegi → max -1 jaitsi
    """
    banda = lortu_ep100_banda(ep100_pisuduna)
    zl_min, zl_max = banda["zl_tartea"]

    if modelo_zl < zl_min:
        zl_berria = min(modelo_zl + 1, zl_max)
        return {
            "zl_nota": zl_berria,
            "doitua": True,
            "arrazoia": (
                f"DOITUA: Modeloaren ZL={modelo_zl} baxuegi da "
                f"EP100={ep100_pisuduna} ({banda['banda']}, tartea {zl_min}-{zl_max}). "
                f"ZL={zl_berria} ezarri da (+1 max)."
            ),
        }
    elif modelo_zl > zl_max:
        zl_berria = max(modelo_zl - 1, zl_min)
        return {
            "zl_nota": zl_berria,
            "doitua": True,
            "arrazoia": (
                f"DOITUA: Modeloaren ZL={modelo_zl} altuegi da "
                f"EP100={ep100_pisuduna} ({banda['banda']}, tartea {zl_min}-{zl_max}). "
                f"ZL={zl_berria} ezarri da (-1 max)."
            ),
        }
    else:
        return {
            "zl_nota": modelo_zl,
            "doitua": False,
            "arrazoia": (
                f"Modeloaren ZL={modelo_zl} koherentea EP100={ep100_pisuduna} "
                f"({banda['banda']}, tartea {zl_min}-{zl_max})"
            ),
        }


def biribildu_nota(batez_bestekoa: float) -> float:
    """0.5era behera biribildu: 6.25->6.0, 6.50->6.5, 6.75->7.0."""
    return math.floor(batez_bestekoa * 2) / 2


def post_prozesatu(emaitza: dict) -> dict:
    """
    API-aren JSON emaitza post-prozesatu:
    0. Erderakada faltsuak iragazki
    1. EP100 birkalkulatu Python-en
    2. ZL nota doitu behar bada
    3. Nota finala birkalkulatu
    Modelo-balioak gordetzen ditu trazabilitaterako.
    """
    akats_taldeak = emaitza.get("akats_taldeak", [])
    hitz_kopurua = emaitza.get("EP100", {}).get("hitz_kopurua", 0)

    # 0. Erderakada faltsuak iragazki
    akats_taldeak = iragazki_erderakada_faltsuak(akats_taldeak)
    iragazitakoak = sum(1 for t in akats_taldeak if t.get("_piztua") is False)

    # 1. EP100 birkalkulatu
    ep100_gordina = kalkulatu_ep100_gordina(akats_taldeak, hitz_kopurua)
    ep100_pisuduna = kalkulatu_ep100_pisuduna(akats_taldeak, hitz_kopurua)
    zl_kontaketak = kontatu_zl_akatsak(akats_taldeak)

    # 2. Modelo-balioak gorde trazabilitaterako
    ep100 = emaitza.get("EP100", {})
    ep100["EP100_gordina_modelo"] = ep100.get("EP100_gordina")
    ep100["EP100_pisuduna_modelo"] = ep100.get("EP100_pisuduna")
    ep100["minor_modelo"] = ep100.get("minor")
    ep100["major_modelo"] = ep100.get("major")
    ep100["critical_modelo"] = ep100.get("critical")

    # 3. Python-balioak ezarri
    ep100["EP100_gordina"] = ep100_gordina
    ep100["EP100_pisuduna"] = ep100_pisuduna
    ep100["minor"] = zl_kontaketak["minor"]
    ep100["major"] = zl_kontaketak["major"]
    ep100["critical"] = zl_kontaketak["critical"]
    ep100["kalkulua"] = "python"
    if iragazitakoak > 0:
        ep100["erderakada_faltsuak_iragazita"] = iragazitakoak

    # 4. ZL nota doitu behar bada
    modelo_zl = emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"]
    zl_emaitza = doitu_zl_nota(modelo_zl, ep100_pisuduna)

    emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["zl_modelo"] = modelo_zl
    if zl_emaitza["doitua"]:
        emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"] = zl_emaitza["zl_nota"]
    emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["python_doikuntza"] = zl_emaitza["arrazoia"]

    # 5. Nota finala birkalkulatu
    ab = emaitza["ebaluazioa"]["atazaren_betetzea"]["nota"]
    ak = emaitza["ebaluazioa"]["antolaketa_koherentzia"]["nota"]
    blh = emaitza["ebaluazioa"]["baliabide_linguistikoen_hedadura"]["nota"]
    zl = emaitza["ebaluazioa"]["zuzentasun_linguistikoa"]["nota"]

    batez_bestekoa = (ab + ak + blh + zl) / 4
    biribiltzea = biribildu_nota(batez_bestekoa)

    lab = emaitza.get("laburpena", {})
    lab["batez_bestekoa_modelo"] = lab.get("batez_bestekoa")
    lab["biribiltzea_modelo"] = lab.get("biribiltzea")
    lab["batez_bestekoa"] = round(batez_bestekoa, 2)
    lab["biribiltzea"] = biribiltzea
    lab["python_postprozesatua"] = True

    return emaitza
