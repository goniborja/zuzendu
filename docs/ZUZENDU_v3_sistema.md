# ZUZENDU v3 — ZUZENKETA-SISTEMA BEHIN BETIKOA
# Sistema definitivo de corrección automática — Euskara eta Literatura (DBH 3–4)

---

## 0. DOKUMENTU HONEN HELBURUA

Especificación técnica completa del motor de corrección. Todo lo que necesita la IA para corregir, todo lo que necesita el profesor para configurar, todo lo que necesita el alumno para mejorar. Directamente traducible a `errubrika.json` + `sistema_prompt.txt`.

**Base teórica:** MCER B1 (Companion Volume 2020) · Patrón analítico 4×25% (IELTS/Cambridge) · Micro-indicadores (NAPLAN/e-rater) · Heziberri 2020 · Investigación en feedback formativo (Hattie 2021, Lipnevich 2023) · Sistema híbrido LLM + corrección lingüística.

**Enfoque:** Sistema híbrido y formativo. La IA no es un juez que pone nota — es un corrector inteligente que aplica la rúbrica del profesor, señala errores con pedagogía, y orienta al alumno sobre CÓMO mejorar (feed-forward), no solo QUÉ está mal.

---

## 1. EBALUAZIO-EGITURA / Estructura de evaluación

### 1.1. Eskala

| Nota | Maila | Heziberri |
|------|-------|-----------|
| 9-10 | Bikaintasuna | Bikaintasuna |
| 7-8 | Aurreratua | Maila aurreratua |
| 5-6 | Tartekoa | Tarteko maila |
| 3-4 | Hasiberria | Hasierako maila |
| 0-2 | Lortu gabea | Lortu gabea |

### 1.2. Lau irizpideak (4 × 25%)

| # | Irizpidea | Zer ebaluatzen du |
|---|-----------|-------------------|
| 1 | **ATAZAREN BETETZEA (AB)** | Contenido, cumplimiento del enunciado, desarrollo de ideas, adecuación al tipo de texto y lector |
| 2 | **ANTOLAKETA ETA KOHERENTZIA (AK)** | Estructura, párrafos, conectores, cohesión, formato del tipo textual |
| 3 | **BALIABIDE LINGUISTIKOEN HEDADURA (BLH)** | Variedad de vocabulario, complejidad sintáctica, registro, capacidad expresiva, naturalidad en euskera |
| 4 | **ZUZENTASUN LINGUISTIKOA (ZL)** | Corrección gramatical, morfológica, ortográfica, puntuación, interferencias L1 |

**Nota final = (AB + AK + BLH + ZL) / 4**

Mismos criterios para DBH 3 y DBH 4. Lo que cambia es la expectativa (gestionada en el prompt, no en la rúbrica): en DBH 3 un 5-6 es rendimiento esperable; en DBH 4 se espera 7-8.

### 1.3. Principio clave: separar RIQUEZA de CORRECCIÓN

BLH mide CÓMO DE BIEN se expresa el alumno (variedad, registro, naturalidad). ZL mide CUÁNTO SE EQUIVOCA (errores contables). Un alumno puede usar estructuras simples pero correctas (BLH bajo, ZL alto) o intentar estructuras complejas y fallar (BLH alto, ZL bajo). Son dimensiones independientes. El alumno que arriesga y falla no debe ser penalizado igual que el que ni lo intenta.

---

## 2. ERRUBRIKA OSOA / Rúbrica completa

### 2.1. ATAZAREN BETETZEA (AB) — 25%

**ERRM B1:** "Informazioa eta ideiak gai abstraktu eta zehatzen inguruan transmititu ditzake arrazoizko zehaztasunarekin."

| Nota | Deskribatzailea |
|------|-----------------|
| 9-10 | Eskaerako puntu guztiak sakonki garatuta. Argudio/adibide zehatzak eta egokiak puntu bakoitzeko. Testu-motaren baldintza guztiak beteta (luzera, helburua, hartzailea, erregistroa). Ideia originalak edo ikuspegi pertsonala. |
| 7-8 | Puntu guztiak landuta eta nahiko garatuta. Xehetasun/adibideak gehienetan. Testu-motaren baldintzak ia guztiz beteta. Noizean behin sakonago garatu zitekeen. |
| 5-6 | Puntu gehienak badaude baina batzuk azalekoak. Adibide gutxi edo irregularrak. Oinarrizko baldintzak beteta baina garapenean hutsuneak. |
| 3-4 | Puntu gutxi, ia garatu gabe. Adibiderik ia ez. Genero/helburu/irakurlearekiko egokitzapen eskasa. |
| 0-2 | Gaitik guztiz urrun (off-topic), edo testua laburregia ebaluatzeko. Ez du testu-motaren eskakizunik betetzen. |

### 2.2. ANTOLAKETA ETA KOHERENTZIA (AK) — 25%

**ERRM B1:** "Elementu laburren segida bat lotu dezake sekuentzia konektatu lineal batean."

| Nota | Deskribatzailea |
|------|-----------------|
| 9-10 | Egitura argia eta eraginkorra (sarrera-garapena-ondorioa). Paragrafoak ondo bereizita, ideia nagusi bat bakoitzean. Lotura-hitz ugari, egokiak eta anitzak (hala ere, gainera, horregatik, bestalde...). Erreferentzia-sistema argia. Formatua guztiz errespetatua. |
| 7-8 | Egitura argia. Paragrafoak ongi antolatuta. Lotura-hitz nahikoak, batzuk konplexuak. Akats txikiak koheretzian baina ez dira oztopo. Formatua ia guztiz egokia. |
| 5-6 | Oinarrizko egitura antzematen da baina garapena linealegia edo saltoduna. Paragrafoak badaude baina banaketa ez beti egokia. Oinarrizko lotura-hitzak nagusi (eta, baina, beraz, gero). Noizean behin saltoren bat. |
| 3-4 | Egitura ahula; ideiak nahasita. Paragrafoen banaketa eskasa edo ez-existitzea. Lotura-hitz gutxi, oinarrizkoak edo desegokiak. Salto logiko nabarmenak. |
| 0-2 | Egiturarik ez. Ideiak deskonektatuta. Kohesiorik ia ez. Paragraforik ez. |

### 2.3. BALIABIDE LINGUISTIKOEN HEDADURA (BLH) — 25%

**ERRM B1:** "Hiztegia nahikoa du, zirkumlokuzioekin; mugapen lexikoek errepikapena eragiten dute."

| Nota | Deskribatzailea |
|------|-----------------|
| 9-10 | Hitz-altxor aberatsa eta zehatza; sinonimoak eta esamoldeak tartekatuz errepikapena saihesten du. Perpaus-egitura ugari eta konplexuak (mendekoak, erlatibozkoak, kausazkoak, kontzesiboak). Erregistroa guztiz egokia eta koherentea. Esapide idiomatikoak edo esamolde bereziak naturalki txertatuta. Gaztelaniaren eraginik ia ez da antzematen formulazioan. |
| 7-8 | Hitz-altxor nahikoa eta egokia; birformulazio batzuk. Perpaus-egitura desberdinak, nahiz eta sinpleagoak nagusi. Erregistroa gehienetan egokia. Noizean behin formulazio-zailtasun txikiren bat edo kalko isolatu bat. |
| 5-6 | Oinarrizko hitz-altxorra, nahikoa ataza betetzeko. Errepikapen batzuk alternatiba falta delako. Perpaus sinpleak nagusi, noizean behin konplexuagoak. Erregistroan gorabehera batzuk. Gaztelaniaren eragin partziala formulazioan (kalko batzuk). |
| 3-4 | Hitz-altxor mugatua; errepikapen ugari. Perpaus sinple eta laburrak ia beti. Erregistro desegokia edo aldakorra. Kalko lexiko eta egiturako nabarmenak. Hiztegiaren mugek komunikazioa zailtzen dute. |
| 0-2 | Hitz-altxorra oso urria. Formulazioak komunikazioa eragozten du. Egitura minimoa. Gaztelaniaren eragin sistematikoa. |

### 2.4. ZUZENTASUN LINGUISTIKOA (ZL) — 25%

**ERRM B1:** "Komunikazioa arrazoizko zehaztasunarekin; kontrol orokorrean ona, ama-hizkuntzaren eragin nabarmenarekin; akatsek ez dute ulermena eragozten."

| Nota | Deskribatzailea |
|------|-----------------|
| 9-10 | Akats oso gutxi (EP100 ≤ 2). Ortografia, morfologia eta aditz-morfologia ondo kontrolatuta. Kasuen erabilera zuzena. NOR-NORI-NORK sistema zuzen. Ia interferentziarik ez. |
| 7-8 | Akats batzuk (EP100 3-5) baina ez dute ulermena oztopatzen. Oinarrizko gramatika ondo kontrolatuta. Ortografia eta puntuazioa nahiko zuzenak. Noizean behineko interferentziak. |
| 5-6 | Akats errepikatuak (EP100 6-10), batez ere kasu-marketan, aditz-adostasunean eta puntuazioan. Testua ulergarria baina akatsek irakurketa zailtzen dute batzuetan. Erderakada batzuk. |
| 3-4 | Akats ugari eta sistematikoak (EP100 11-18). Oinarrizko egituretan ere akatsak. Ulermena tarteka zailtzen da. Erderakada ugari. |
| 0-2 | Akats larriak eta oso ugari (EP100 > 18). Testua ia ulertezina. Interferentzia sistematikoak. |

---

## 3. AKATS-KUDEAKETA / Gestión de errores

### 3.1. Akats-sailkapena / Clasificación de errores

Hiru larritasun-maila:

| Larritasuna | Definizioa | Adibideak | Pisua EP100n |
|-------------|-----------|-----------|--------------|
| **Minor** | Ez du komunikazioa kaltetzen | Typo, letra larri falta, koma bat falta | ×1 |
| **Major** | Ulermena zailtzen du | Kasu-marka okerra, NOR-NORK nahasketa, aditz okerra | ×2 |
| **Critical** | Esaldia ulertezin egiten du | Esaldia zentzurik gabe, aditza guztiz okerra | ×3 |

**EP100 pisuduna = (minor×1 + major×2 + critical×3) × 100 / hitz kopurua**

### 3.2. Akats-errepikapen kudeaketa / Penalización decreciente por repetición

**Printzipioa:** Un mismo tipo de error no se penaliza infinitamente. La IA identifica el patrón y penaliza la tendencia, no cada instancia.

**Nola funtzionatzen du:**

1. Akats mota bat lehen aldiz agertzen denean → penalizazio osoa (×1)
2. Bigarren aldiz → penalizazio erdia (×0.5)
3. Hirugarren aldiz eta aurrera → ez du gehiago puntuazioan eragiten, baina feedback-ean agertzen da ("X aldiz gertatu da")

**Adibidea:** Ikasleak ergatiboa (-k) 5 aldiz ahazten du. EP100rako: lehenengo 2 major gisa kontatzen dira (2+1=3 puntu), gainerako 3ak feedback-ean aipatzen dira baina ez dute nota gehiago jaisten. Feedback-ean: "Ergatiboa (-k) 5 aldiz ahaztu duzu. Hau da zure akats nagusia — NOR-NORK egitura landu behar duzu."

**Zergatik:** Ikasle bat ez da zigortzen behin eta berriz gauza beragatik. Akats-patroi bat identifikatu ondoren, garrantzitsuena feedback egokia da, ez nota jaitsi eta jaitsi.

### 3.3. Akats-multzokatzea / Agrupación de errores en el feedback

La IA NO presenta una lista plana de 20 errores. Los agrupa por categoría y presenta un comentario por grupo:

```
AKATS-TALDEAK:

Aditz laguntzailea (4 akats — major):
  "NOR-NORK sistema 4 aldiz nahastu duzu. Adibidez: 'nik ikusi naiz' → 'nik ikusi DUT'.
   Gogoratu: ekintza bat egiten duzunean, laguntzailea DUT/DUGU/DUZU... da."

Ortografia - sibilanteak (3 akats — minor):
  "Z eta S nahastu dituzu 3 aldiz: 'gazte' → 'gazte' (ondo), baina 'zagu' → 'SAGU'.
   Gogoratu: s/z/x bereizketak garrantzi handia du euskaraz."

Erderakadak (2 akats — major):
  "'Sombra' → 'ITZALA'. 'Baina ere' → 'HALA ERE' edo 'BESTALDE'.
   Saiatu gaztelaniazko hitzak eta egiturak euskarazkoekin ordezten."
```

Adierazle nagusiak ematen ditu (2-3 talde gehienez), eta patroi-errepikapena azpimarratzen du.

### 3.4. Zuzenketa-erabakia / Decisión pedagógica de corrección

Ez da akats guztia berdin tratatzen. Akats bakoitzak erabaki bat du: zuzendu beti, batzuetan, edo ez zuzendu.

| Erabakia | Noiz | Adibideak |
|----------|------|-----------|
| **Beti zuzendu** | Akats larriak, komunikazioa kaltetzen dutenak, oinarrizko arau-hausteak | Ergatiboa falta, NOR-NORK nahasketa, off-topic, egiturarik ez |
| **Zuzendu baina neurriz** | Akats moderatuak; guztiak markatu ordez patroia identifikatu | Ortografia-akats errepikatuak (lehen adibidea markatu, gainerakoak zenbatu), puntuazio-arazoak |
| **Aukerakoa / Kontestuaren arabera** | Dialektismoak, estilo-aukerak, minor isolatuak | "Dau" vs "du" (dialektismoa); koma aukerako baten falta; hitz arraro bat batua ez dena |
| **Ez zuzendu** | Akats intentzionalak estiloan, maila gainditzen duten ahaleginak | Elkarrizketa batean kolokialismoaren erabilera; egitura konplexu bat saiatu eta huts egin (saiakera baloratzen da BLH-n) |

**GARRANTZITSUA — Positibo faltsuak minimizatu:** Hobe da akats erreal bat markatu gabe uztea, akats ez den zerbait akats gisa markatzea baino. Positibo faltsuek ikaslearen konfiantza hondatzen dute sisteman. Zalantzarik badago → "zalantzazkoa" markatu.

---

## 4. MUGA-ARAUAK ETA PENALIZAZIOAK / Caps y penalizaciones

### 4.1. Muga-arauak (Caps)

Baldintza larri bat gertatzen denean, irizpide horretan gehienezko nota bat ezartzen da. Deskribatzaileak baino lehenago aplikatzen dira.

| ID | Baldintza | Irizpidea | Gehienezko nota |
|----|-----------|-----------|-----------------|
| CAP-1 | Off-topic | AB | 2/10 |
| CAP-2 | Eskakizunen ≥%50 falta | AB | 4/10 |
| CAP-3 | Luzera < gutxienekoaren %70 | AB | 4/10 |
| CAP-4 | Generoa ez da errespetatzen | AB | 6/10 |
| CAP-5 | Egiturarik ez (sarrera/garapena/ondoriotik 2 falta) | AK | 4/10 |
| CAP-6 | Inkoherentzia iraunkorra | AK | 6/10 |
| CAP-7 | Perpaus sinpleak soilik testu osoan | BLH | 6/10 |
| CAP-8 | Testua ia ulertezina akats kopuruagatik | ZL | 2/10 |

### 4.2. Penalizazio-sistema

Cap arauak ez badira aplikatzen, IAk deskribatzaileen arabera nota jartzen du eta doikuntza txikiak aplika ditzake:

| ID | Penalizazioa | Irizpidea | Balioa | Gehienezko metatze |
|----|-------------|-----------|--------|---------------------|
| PEN-1 | Eskakizun bat garatu gabe | AB | -0.5 | -2.0 |
| PEN-2 | Paragrafo bakarra | AK | -0.5 | -0.5 |
| PEN-3 | Paragrafo batean gai-apurketa | AK | -0.2 | -1.0 |
| PEN-4 | Lotura-hitz okerra (erlazio logiko faltsua) | AK | -0.5 | -1.5 |
| PEN-5 | Errepikapen lexiko nabarmena | BLH | -0.5 | -1.5 |
| PEN-6 | Hitz generikoen gehiegizko erabilera | BLH | -0.3 | -1.0 |
| PEN-7 | Erregistro-nahasketa | BLH | -0.5 | -1.0 |

### 4.3. Bonifikazioak

| ID | Bonifikazioa | Irizpidea | Balioa | Baldintza |
|----|-------------|-----------|--------|-----------|
| BON-1 | Esamolde idiomatiko egokiak | BLH | +0.3 | Kolokazio edo esamolde natural eta egokiak |
| BON-2 | Ikuspegi originala / ideia berria | AB | +0.3 | Planteamendu bereziki interesgarria |
| BON-3 | Kohesio-baliabide aurreratuak | AK | +0.3 | Anafora, elipsi, erreferentzia konplexuak egoki erabiltzen ditu |
| BON-4 | Konplexutasun sintaktiko egokia | BLH/ZL | +0.3 | Egitura konplexuak (baldintza, subjuntiboa, erlatiboak) AKATSIK GABE erabiltzen ditu |

Bonifikazioak ez dute 10/10 gainditzen.

### 4.4. EP100 bandak (ZL irizpiderako)

| Banda | EP100 pisuduna | Nota-tartea |
|-------|----------------|-------------|
| Bikaintasuna | ≤ 2 | 9-10 |
| Aurreratua | 3-5 | 7-8 |
| Tartekoa | 6-10 | 5-6 |
| Hasiberria | 11-18 | 3-4 |
| Lortu gabea | > 18 | 0-2 |

**EP100 normalizazioa:** Dentsitate bidez neurtzen da, ez bolumen absolutuz. 5 akats 100 hitzetan (%5) ≠ 5 akats 300 hitzetan (%1.7). Horrela, luze idazten duenak ez du zigorra jasotzen luze idazteagatik.

---

## 5. AKATS-KATALOGOA / Catálogo de fallos tipificados

### 5.1. Atazaren betetzea (AB)

| ID | Akatsa | Larritasuna | Zuzendu? | Ekintza |
|----|--------|-------------|----------|---------|
| TB-1 | Off-topic | Critical | Beti | → CAP-1 |
| TB-2 | Eskakizun-falta (≥%50) | Major | Beti | → CAP-2 |
| TB-3 | Garapen eskasa (adibiderik/argudiorik ez) | Media | Beti | → PEN-1 |
| TB-4 | Generoa ez du errespetatzen | Major | Beti | → CAP-4 |
| TB-5 | Erregistro desegokia | Media-Major | Beti | → PEN-7 |
| TB-6 | Luzera insuficientea (<70% min) | Major | Beti | → CAP-3 |
| TB-7 | Informazio garrantzirik gabea (relleno) | Minor-Major | Partziala | Komenta feedback-ean baina ez penalizatu larriki minor bada |

### 5.2. Antolaketa eta koherentzia (AK)

| ID | Akatsa | Larritasuna | Zuzendu? | Ekintza |
|----|--------|-------------|----------|---------|
| OK-1 | Egiturarik ez | Major | Beti | → CAP-5 |
| OK-2 | Paragrafo-banaketa eskasa | Major | Beti | → PEN-2, PEN-3 |
| OK-3 | Lotura-hitz eskasak / errepikatzaileak | Media | Beti | Feedback + gomendio |
| OK-4 | Lotura-hitz okerrak (erlazio logiko faltsua) | Major | Beti | → PEN-4 |
| OK-5 | Erreferentzia nahasak (izenordain aurrekaririk gabe) | Major | Beti | Markatu + azaldu |
| OK-6 | Salto logikoak | Major | Beti | → CAP-6 (iraunkorra bada) |
| OK-7 | Erredundantziak (ideia bera behin eta berriz) | Minor | Partziala | Komentatu, ez penalizatu larriki |

### 5.3. Baliabide linguistikoen hedadura (BLH)

| ID | Akatsa | Larritasuna | Zuzendu? | Ekintza |
|----|--------|-------------|----------|---------|
| LH-1 | Errepikapen lexiko altua | Media | Beti | → PEN-5, sinonimoak gomendatu |
| LH-2 | Hiztegia generikoegia (gauza, egin, ona...) | Media | Beti | → PEN-6, alternatibak proposatu |
| LH-3 | Konplexutasun sintaktiko eskasa | Media | Beti | → CAP-7 (muturrekoa bada) |
| LH-4 | Kalko lexikoak (gaztelaniatik) | Major | Beti | Markatu + euskarazko alternatiba eman |
| LH-5 | Erregistro ezegonkorra | Media | Beti | → PEN-7 |
| LH-6 | Gaztelaniazko hitza zuzenean sartuta | Major | Beti | Euskarazko baliokidea proposatu |
| LH-7 | Dialektismoak batua espero denean | Minor | Kontestuaren arabera | Batua proposatu baina ez penalizatu larriki |
| LH-8 | Egitura konplexu bat saiatu eta huts egin | — | EZ | Saiakera baloratzen da BLH-n; akatsa ZL-n neurtzen da |

### 5.4. Zuzentasun linguistikoa (ZL) — Akats kontakizunak

#### Ortografia (ZL-ORT)

| ID | Akatsa | Adibidea | Larritasuna |
|----|--------|---------|-------------|
| ZL-ORT-1 | Grafia okerra | *zagu → sagu (sibilanteak) | Minor |
| ZL-ORT-2 | Hitz-banaketa/elkarketa | *etxekoandreak → etxeko andreak | Minor |
| ZL-ORT-3 | Letra larriak | *bilbon → Bilbon | Minor |
| ZL-ORT-4 | Maileguen ortografia | *sofware → software | Minor |

#### Morfologia nominala — Deklinabidea (ZL-KAS)

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-KAS-1 | Ergatiboa falta (-k) | *Nik gustatu da → Niri gustatu zait | Major |
| ZL-KAS-2 | Datiboa (-ri) okerra | *laguna eman diot → lagunARI eman diot | Major |
| ZL-KAS-3 | Adlatiboa (-ra) falta | *eskolan joan → eskolaRA joan | Major |
| ZL-KAS-4 | Ablatiboa (-tik) nahasketa | *etxera etorri → etxeTIK etorri | Major |
| ZL-KAS-5 | Determinazioa (-a/-ak) | *gizon etorri da → gizonA etorri da | Major |
| ZL-KAS-6 | Mugagabea (-rik) falta ezezkoan | *ez dut liburu → ez dut liburuRIK | Major |
| ZL-KAS-7 | Genitiboa (-ren) | kontestua kontuan hartuta | Minor-Major |
| ZL-KAS-8 | Soziatiboa (-rekin) | zenbakia kontuan hartuta | Minor |

#### Aditz-morfologia (ZL-ADI)

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-ADI-1 | Laguntzaile-hautaketa okerra | *nik ikusi naiz → nik ikusi DUT | Critical |
| ZL-ADI-2 | Pertsona-adostasuna | *guk joan naiz → guk joan GARA | Major |
| ZL-ADI-3 | Numero-adostasuna | *umeak etorri da → umeak etorri DIRA | Major |
| ZL-ADI-4 | Aldia (tempusa) okerra | *atzo joango naiz → atzo joan NINTZEN | Major |
| ZL-ADI-5 | Aspektua (ari/-tzen/-tu/-ko) | *zer egiten duzu bihar? → zer EGINGO duzu? | Major |
| ZL-ADI-6 | Ezezkoa gaizki kokatuta | *ez ikusi dut → EZ DUT ikusi | Major |
| ZL-ADI-7 | NOR-NORI-NORK nahasketa | *ikusi diot → ikusi DUT (OZrik gabe) | Critical |

#### Sintaxia (ZL-SIN)

| ID | Akatsa | Larritasuna |
|----|--------|-------------|
| ZL-SIN-1 | Osagaien ordena anbiguoa | Minor-Major |
| ZL-SIN-2 | Mendeko perpaus gaizki eratua | Major |
| ZL-SIN-3 | Erlatibozko gaizki eratua (*gizona ikusi dudana → ikusi dudan gizona) | Major |
| ZL-SIN-4 | Osagarritasun arazoak (*hori ona da → hori ona DELA) | Major |
| ZL-SIN-5 | Esaldi osatu gabeak (mendekoa nagusirik gabe) | Major |

#### Puntuazioa (ZL-PUN)

| ID | Akatsa | Larritasuna |
|----|--------|-------------|
| ZL-PUN-1 | Punturik ez esaldien artean (run-on) | Major |
| ZL-PUN-2 | Koma subjektu eta aditz artean | Minor |
| ZL-PUN-3 | Koma falta lotura-hitz ondoren | Minor |
| ZL-PUN-4 | Komatxoen falta/soberan | Minor |

#### Erderakadak / Interferentziak (ZL-ERD)

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-ERD-1 | Kalko sintaktikoa | *baina ere → hala ere / bestalde | Major |
| ZL-ERD-2 | Gaztelaniazko hitza | *sombra → itzala / gerizpea | Major |
| ZL-ERD-3 | Hitz-ordena gaztelaniakoa (SOV haustea) | Kontestua kontuan hartuta | Minor-Major |
| ZL-ERD-4 | Esamolde-kalkoa | *ilea hartu → adarra jo | Major |
| ZL-ERD-5 | Preposizio-kalkoa (-gatik/-rentzat nahasketa) | Kontestua kontuan hartuta | Major |

---

## 6. FEEDBACK-SISTEMA / Cómo se presenta el feedback

### 6.1. Printzipio pedagogikoak

Ikerketa oinarrituta (Hattie 2021, Lipnevich 2023):

1. **Positibotik hasi BETI.** Feedback guztia zerbait on batekin hasten da — txikia bada ere. Horrela motibazioa mantentzen da.
2. **Feed-forward eman.** "Zer dago gaizki" baino garrantzitsuagoa da "nola hobetu". Irizpide bakoitzean NOLA maila igotzen den azaltzen da.
3. **Lehenetsi eragina.** Lehenik komunikazio-eragin handiena duten arazoak aipatzen dira. Off-topic bada, hori lehenik — ez puntuazio-akats bat.
4. **Akatsak multzokatu.** Ez eman 20 akatsen zerrenda laua. Multzokatu kategoriak eta patroi gisa aurkeztu (ikus 3.3).
5. **Ez saturatu.** Gehienez 2-3 hobetzeko puntu irizpide bakoitzeko. Dena aldi berean zuzentzea ezinezkoa da — hurrengo idazlanerako lehentasuna ematen da.
6. **Ebidentzia testutik.** Aipu laburrak (1-2 esaldi) ikaslearen testutik feedback-a justifikatzeko.
7. **Anti-aluzinazioa.** Zalantzarik badago, "zalantzazkoa" markatu, ez asmatu.

### 6.2. Feedback-egitura (hiru geruza)

```
GERUZA 1: LABURPEN OROKORRA (3-4 esaldi)
├── Zerbait positiboa (beti)
├── Nota globala + maila
├── Hobetzeko arlo nagusia (bat)
└── Animatzeko esaldia

GERUZA 2: IRIZPIDE BAKOITZEKO FEEDBACKA (×4)
├── Nota + maila
├── 2 indarguneak (ebidentziarekin)
├── 2 hobetzekoak (NOLA hobetu azalduz, ez soilik ZER dago gaizki)
└── Feed-forward: "Hurrengo aldian, saiatu..."

GERUZA 3: AKATS-TALDEAK (ZL irizpiderako batez ere)
├── Kategoriaren arabera multzokatuta (ikus 3.3)
├── Talde bakoitzean: kopurua + adibide bat + zuzenketa + araua
├── Larritasuna adierazita
└── "Zalantzazkoa" marka behar denean
```

### 6.3. Feedback-tonua

- **Hizkuntza:** Beti euskaraz
- **Tonua:** Positiboa, konstruktiboa, ikasleak aurrera egitera animatzen duena
- **Pertsona:** "Zuk" (errespetuzko tratamendua)
- **Debekatua:** Humiliazioa, ironia, "txarto egin duzu" gisakoak
- **Gomendatua:** "Ondo egin duzu X, eta Y hobetzeko aukera duzu Z eginez"

### 6.4. Laburpen txantiloiak

**Tarteko maila (5-6) adibidea:**
```
6.0/10 — Tarteko maila

Iritzi-artikulu ulergarri bat idatzi duzu gaiaren inguruan, zure iritzia argi
adieraziz. Egitura hobetzea da zure lehentasun nagusia: paragrafoen banaketa
eta lotura-hitzen aniztasuna landu behar dituzu. Norabide onean zaude, jarraitu!
```

**Hasiberria (3-4) adibidea:**
```
3.5/10 — Hasierako maila

Gaiaren inguruan idazten saiatu zara, eta oinarrizko ideiak badaude bertan.
Testua gehiago garatu behar duzu: arrazoiak, adibideak eta ondorioak gehitu.
Hurrengo aldian, sarrera-garapena-ondorioa egitura jarraituz saiatu. Badaukazu
oinarria, eta praktikarekin hobetuko duzu!
```

---

## 7. ZIURGABETASUN-KUDEAKETA / Gestión de incertidumbre

### 7.1. "Zalantzazkoa" protokoloa

IAk bere ebaluazioaz seguru ez dagoenean, honela jokatzen du:

| Egoera | Ekintza | Penalizazioa |
|--------|---------|--------------|
| Hitz bat ez du ezagutzen (izen propioa? neologismoa?) | "Zalantzazkoa" markatu + "Hitz hau ez dut ezagutzen; egiaztatu" | Ez penalizatu |
| Morfologia-zuzenketa bat ez du seguru | "Zalantzazkoa" markatu + bi aukera proposatu | Ez penalizatu |
| Dialektismo izan daiteke | "Dialektismoa izan daiteke; batuaz X litzateke" | Ez penalizatu (irakaslearen erabakia) |
| Akats intentzionala izan daiteke (elkarrizketa batean) | "Nahita izan daiteke kontestuan" | Ez penalizatu |
| Esaldi bat ulertezina da (ezin du parseatu) | "Esaldi hau ez dut ondo ulertzen. Berridatzi mesedez." | Penalizatu AK edo ZL-n |

**Arau nagusia:** Hobe da akats bat markatu gabe uztea, zuzena dena akats gisa markatzea baino.

### 7.2. Irakaslearen berrikusketa

IAren irteera txosten bat da, ez azken erabakia. IAk markatzen du:
- 🟢 Seguru (zuzentzeko erabaki automatikoa)
- 🟡 Zalantzazkoa (irakaslearen erabakia behar)
- 🔴 Alerta (off-topic, susmo de copia, nota oso baxua/altua — irakaslearen berrespena behar)

Irakasleak txostena azkar begiratzen du eta 🟡/🔴 kasuak erabakitzen ditu. Kasu gehienetan, IAren ebaluazioa onartuko du.

---

## 8. IRTEERA-FORMATUA / Formato de salida JSON

### 8.1. JSON egitura osoa

```json
{
  "kodea": "3A017",
  "ebaluazioa": {
    "atazaren_betetzea": {
      "nota": 7,
      "maila": "aurreratua",
      "cap_aplikatua": null,
      "iruzkina": {
        "indarguneak": ["...", "..."],
        "hobetzekoak": ["...", "..."],
        "feed_forward": "Hurrengo aldian, saiatu argudio bakoitza adibide konkretu batekin laguntzen."
      }
    },
    "antolaketa_koherentzia": {
      "nota": 7,
      "maila": "aurreratua",
      "cap_aplikatua": null,
      "iruzkina": { "indarguneak": [], "hobetzekoak": [], "feed_forward": "" }
    },
    "baliabide_linguistikoen_hedadura": {
      "nota": 5,
      "maila": "tartekoa",
      "cap_aplikatua": null,
      "iruzkina": { "indarguneak": [], "hobetzekoak": [], "feed_forward": "" }
    },
    "zuzentasun_linguistikoa": {
      "nota": 6,
      "maila": "tartekoa",
      "cap_aplikatua": null,
      "iruzkina": { "indarguneak": [], "hobetzekoak": [], "feed_forward": "" }
    }
  },
  "laburpena": {
    "batez_bestekoa": 6.25,
    "biribiltzea": 6.0,
    "heziberri_maila": "tartekoa",
    "orokorra": "Laburpen orokorra euskaraz...",
    "lehentasuna": "Hurrengo idazlanerako lehentasuna: ..."
  },
  "akats_taldeak": [
    {
      "kategoria": "Aditz laguntzailea",
      "kopurua": 3,
      "larritasuna": "major",
      "adibidea": {
        "detektatutakoa": "nik ikusi naiz",
        "zuzenketa": "nik ikusi dut",
        "azalpena": "NOR-NORK: ekintza bat egiten duzunean..."
      },
      "zalantzazkoa": false
    }
  ],
  "EP100": {
    "minor": 3,
    "major": 4,
    "critical": 0,
    "EP100_gordina": 4.0,
    "EP100_pisuduna": 6.3
  },
  "meta": {
    "segurtasun_azterketa": {
      "susmagarria": false,
      "oharrak": ""
    },
    "irakasle_berrikusketa": {
      "beharrezkoa": false,
      "arrazoiak": []
    }
  }
}
```

---

## 9. ZUZENKETA-ZIKLOA / Ciclo de corrección iterativo

### 9.1. Borrador → Feedback → Berridazketa

Sistemak borrador-ziklo bat ahalbidetzen du:

```
ZIKLOA:

1. ZIRRIBORROA idatzi (ikaslea)
      ↓
2. IAk ebaluatu + feedback eman
      ↓
3. Ikasleak feedbacka irakurri
      ↓
4. BERRIDAZKETA egin (feedbacka aplikatuz)
      ↓
5. IAk berriro ebaluatu (edo irakaslea zuzenean)
      ↓
6. AZKEN NOTA
```

**Nola funtzionatzen du praktikan:**
- Ikaslea HTMLan idazten du (lehen bertsioa)
- IAk minutu gutxitan feedback ematen du
- Ikaslea berridazten du (klasean edo etxean)
- Bigarren bertsioa da azken nota
- Irakaslea bigarren bertsioaren txostena azkar begiratzen du eta onartzen du (edo doitzen)

**Zergatik:** Ikerketak erakusten du (Hattie 2021) feedback-a berridazketa batekin konbinatzen denean, idazketa-konpetentziaren hobekuntza ASKOZ handiagoa dela feedback hutsa baino.

### 9.2. Borrador-zikloan IAren portaera

**Lehen zirriborroaren feedbacka:**
- Positiboagoa: saiakera azpimarratzen du
- Feed-forward nagusia: "Hurrengo bertsioan, lehenik X landu"
- Akats-zerrenda mugatuagoa (akats nagusiak soilik)

**Azken bertsioaren feedbacka:**
- Ebaluazio osoa: nota + deskribatzaileak + akats-talde guztiak
- Aurreko bertsioarekin konparaketa posible: "Hobekuntza: koherentzian 5etik 7ra igo zara"

---

## 10. TESTU-MOTA ESPEZIFIKOAK / Notas por tipología textual

Errubrika generikoa da tipologia guztientzat. Testu-mota bakoitzak baldintza espezifikoak ditu ataza-fitxan definitzen direnak:

| Testu-mota | AB: zer espero den | AK: egitura | BLH: erregistroa | Oharra |
|------------|-------------------|-------------|-------------------|--------|
| **Iritzi-artikulua** | Tesia + argudioak + ondorioa | Tesia→argudioak→kontrargumentua→ondorioa | Formala/akademikoa | Argudio-lokailuak |
| **Gutun formala** | Helburua + arrazoiak + eskaera | Agurra→sarrera→gorputza→eskaera→agur formala | Formala (zuka) | Agur-formulak |
| **Gutun informala** | Mezua argi komunikatu | Agurra→berria→amaiera | Informala | Ez penalizatu hika |
| **Deskribapena** | Xehetasun sentsorialak | Orokorretik zehatzera | Neutrala | Adjektiboen aniztasuna |
| **Hausnarketa** | Gogoeta pertsonala + arrazoiketa | Galdera→garapena→ondorioa | Pertsonala | Lehen pertsona |
| **Gidoia** | Pertsonaiak + elkarrizketa + ekintza | Eszenak→akotazioak→elkarrizketak | Pertsonaien arabera | Elkarrizketa naturala |
| **Narrazioa** | Istorioa kontatu | Hasiera→korapiloa→amaiera | Narraziozkoa | Aditz-denborak |
| **Laburpena** | Jatorrizko testuaren gako-ideiak | Jatorrizkoaren egitura jarraitu | Neutrala | Testu-iturriarekiko fideltasuna |

---

## 11. PROMPT-EGITURA / Estructura del prompt de sistema

```
┌─────────────────────────────────────────────────────────────┐
│ SISTEMA (fijo)                                               │
│ ├── Rola: Euskal Hizkuntza eta Literaturako irakasle aditua  │
│ ├── Enfokea: Feedbacka formatiboa, hobekuntzan zentratua     │
│ ├── Ebaluazio-sistema: ERRM B1 + Heziberri 2020             │
│ ├── Output formatua: JSON egitura zehatza                    │
│ ├── Feedback-arauak: positibotik hasi, feed-forward eman,   │
│ │   ez saturatu, multzokatu akatsak                          │
│ ├── Anti-aluzinazioa: zalantzazkoa markatu, ez asmatu        │
│ ├── Akats-errepikapen araua: lehenengo ×1, bigarren ×0.5,   │
│ │   hirugarrenetik aurrera feedback soilik                   │
│ └── Feedbackaren hizkuntza: euskara                          │
├──────────────────────────────────────────────────────────────┤
│ ERRUBRIKA (fijo — dokumentu honetako 2+3+4+5. atalak)       │
│ ├── 4 irizpideak + deskribatzaileak                          │
│ ├── Cap arauak + penalizazioak + bonifikazioak               │
│ ├── EP100 bandak                                             │
│ ├── Akats-katalogoa (IDak + larritasunak)                    │
│ └── Feedback egitura (3 geruza)                              │
├──────────────────────────────────────────────────────────────┤
│ ATAZA-FITXA (aldagarria — azterketa bakoitzean)              │
│ ├── Egitekoa (enuntziatu zehatza)                            │
│ ├── Testu-mota + erregistroa                                 │
│ ├── Maila (DBH3/DBH4)                                       │
│ ├── Hitz-kopurua (min-max)                                   │
│ ├── Eduki espezifikoak (checklist)                           │
│ ├── Ebaluazio-oharrak (irakaslearen oharrak)                 │
│ └── Zuzenketa-modua: borrador ala azken bertsioa             │
├──────────────────────────────────────────────────────────────┤
│ AINGURA-TESTUAK (aukerakoa — kalibrazioa)                    │
│ ├── Adibidea 8/10: testua + ebaluazioa                       │
│ └── Adibidea 5/10: testua + ebaluazioa                       │
├──────────────────────────────────────────────────────────────┤
│ IKASLEAREN TESTUA (aldagarria)                               │
│ └── Testua + metadatuak (kodea, hitz-kopurua, denbora)       │
└──────────────────────────────────────────────────────────────┘
```

---

## 12. KALIBRAKETA-PROZESUA / Proceso de calibración

### 12.1. Pausoak

1. **10-20 idazlan zuzendu eskuz** errubrika honekin
2. **IAk testu berdinak zuzendu**
3. **Konparatu:** notetan >1 puntuko aldea badago, doitu
4. **Doitu:** EP100 atalaseak, cap arauak, penalizazio-balioak
5. **2-3 aingura-testu sortu** kalibrazio iraunkor gisa
6. **Errepikatu** korrelazio onargarria lortu arte (helburua: ≤1 puntuko aldea kasuen %80an)

### 12.2. Talde-mailako analisia

IAk detektatzen badu talde oso batean akats-mota bat errepikatzen dela (adib. ikasleen %70ek ergatiboa ahazten du), txosten bat sortzen du irakaslearentzat:

```
TALDE-ANALISIA — 3A taldea — 2026-02-10 azterketa:

Akats ohikoenak:
1. Ergatiboa (-k) ahaztu: 18/25 ikaslek (→ Klase osoan landu behar da)
2. Lotura-hitz bakarra ("eta"): 12/25 ikaslek (→ Lotura-hitz zerrenda partekatu)
3. "Sombra" erabili "itzala" ordez: 8/25 ikaslek (→ Erderakada ohikoena)
```

Honek irakasleari aukera ematen dio hurrengo klaseetan arazo komunak lantzeko.

---

## 13. INPLEMENTAZIO-ORDENA / Orden de implementación

| Fasea | Fitxategia | Zer da | Saioa |
|-------|-----------|--------|-------|
| 0 | GitHub repo + README | Egitura + dokumentazioa | 1 saio |
| 1.1 | `errubrika.json` | Errubrika + caps + EP100 + akats-katalogoa | 1 saio |
| 1.2 | `sistema_prompt.txt` | Prompt + feedback-arauak + anti-aluzinazioa | 1 saio |
| 1.3 | `zuzendu_test.py` | Script minimoa: testua → API → JSON | 1 saio |
| 1.4 | Kalibrazioa | 10-20 testu eskuz zuzendu, IArekin konparatu, doitu | 2-3 saio |
| 2.1 | `azterketa.html` | Ikasleen interfazea: egitekoa + textarea + kontadorea + JSON irteera | 1 saio |
| 2.2 | Segurtasun-geruza | Paste/tab/pattern detekzioa HTMLan | 1 saio |
| 2.3 | `zuzendu.py` | Batch processing: karpetako JSONak → API → emaitzak | 1 saio |
| 3.1 | `emaitzak.xlsx` generatzailea | JSON emaitzak → XLSX notak + feedbacka | 1 saio |
| 3.2 | `koadernoa.xlsx` + `eguneratu.py` | Azterketa guztien notak koaderno digitalean | 1 saio |
| 4.1 | `sortzailea.html` | Irakaslearen interfazea: egitekoa konfiguratu + HTML sortu | 2 saio |
| 4.2 | Borrador-zikloa | Bi bertsio-zuzenketa HTMLan integratu | 1 saio |

**Funtsezkoa:** Fase bakoitzak zerbait funtzional sortzen du. 1.3 fasea amaitzean, dagoeneko IA bidezko zuzenketa egiten da (copiar-pegar bidez bada ere). Gainerako guztia erosotasun-geruza da.

---

*ZUZENDU v3 — Zuzenketa-sistema behin betikoa. 2026-02-09.*
