# ZUZENDU — ZUZENKETA-EREDU BEHIN BETIKOA
# Modelo definitivo de corrección automática para redacciones de Euskara eta Literatura (DBH 3–4)

---

## 0. DOKUMENTU HONEN HELBURUA

Este documento es la **especificación técnica completa** del motor de corrección de ZUZENDU. Contiene todo lo que necesita una IA para corregir una redacción en euskera: la rúbrica, las reglas cuantificables, el catálogo de fallos, los tipos de feedback, y ejemplos completos de salida. Es directamente aplicable en aula y directamente traducible a un prompt de sistema.

**Base teórica:** MCER/ERRM nivel B1 (Companion Volume 2020), patrón analítico 4×25% (IELTS/Cambridge), operacionalización por micro-indicadores (NAPLAN/e-rater), marco competencial Heziberri 2020.

---

## 1. EBALUAZIO-EGITURA / Estructura de evaluación

### 1.1. Eskala / Escala

| Nota 0-10 | Maila (EU) | Heziberri | Etiketa |
|-----------|------------|-----------|---------|
| 9-10 | Bikaintasuna | Bikaintasuna | ⬛⬛⬛⬛⬛ |
| 7-8 | Aurreratua | Maila aurreratua | ⬛⬛⬛⬛◻ |
| 5-6 | Tartekoa | Tarteko maila | ⬛⬛⬛◻◻ |
| 3-4 | Hasiberria | Hasierako maila | ⬛⬛◻◻◻ |
| 0-2 | Lortu gabea | Lortu gabea | ⬛◻◻◻◻ |

### 1.2. Lau irizpideak / Los cuatro criterios (4 × 25%)

| # | Irizpidea (EU) | Criterion (EN) | Zer ebaluatzen du |
|---|----------------|----------------|-------------------|
| 1 | ATAZAREN BETETZEA (AB) | Task Achievement | Contenido, cumplimiento del enunciado, desarrollo de ideas, adecuación al tipo de texto y lector |
| 2 | ANTOLAKETA ETA KOHERENTZIA (AK) | Organisation & Coherence | Estructura, párrafos, conectores, cohesión, formato del tipo textual |
| 3 | BALIABIDE LINGUISTIKOEN HEDADURA (BLH) | Linguistic Range | Variedad de vocabulario, complejidad sintáctica, registro, capacidad expresiva |
| 4 | ZUZENTASUN LINGUISTIKOA (ZL) | Linguistic Accuracy | Corrección gramatical, morfológica, ortográfica, puntuación, interferencias L1 |

**Nota final = (AB + AK + BLH + ZL) / 4**

Mismos criterios para DBH 3 y DBH 4. Lo que cambia es la expectativa (gestionada en el prompt, no en la rúbrica).

### 1.3. DBH 3 vs DBH 4: expectativas

| Maila | Espero dena (expectativa) | Interpretazioa |
|-------|---------------------------|----------------|
| DBH 3 | 5-6 (Tartekoa) es rendimiento adecuado | Un 7 en DBH3 es un buen resultado |
| DBH 4 | 7-8 (Aurreratua) es rendimiento adecuado | Un 5-6 en DBH4 indica que necesita mejorar |

---

## 2. ERRUBRIKA OSOA / Rúbrica completa con descriptores

### 2.1. IRIZPIDEA 1: ATAZAREN BETETZEA (AB) — 25%

**Qué mide:** ¿El alumno ha hecho lo que se le pedía? ¿Ha desarrollado el contenido? ¿Se adecúa al tipo de texto?

**Oinarri-deskribatzailea ERRM B1:** "Informazioa eta ideiak gai abstraktu eta zehatzen inguruan transmititu ditzake arrazoizko zehaztasunarekin."

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Eskaerako puntu guztiak lantzen ditu eta sakonki garatzen ditu. Argudio/adibide zehatzak eta egokiak ematen ditu (gutxienez bat puntu bakoitzeko). Testu-motaren baldintzak guztiz betetzen ditu: luzera, helburua, hartzailea, erregistroa. Ideia originalak edo ikuspegi pertsonala agertzen du. |
| 7-8 | Aurreratua | Eskatutako puntu guztiak lantzen ditu eta nahiko ondo garatzen ditu. Xehetasun edo adibideak ematen ditu gehienetan. Testu-motaren baldintzak ia guztiz betetzen ditu. Garatze-maila nahikoa du argudioak edo ideiak konbentzitzeko/azaltzeko. |
| 5-6 | Tartekoa | Eskatutako puntuen gehienak lantzen ditu, baina batzuk azalekoak dira edo gutxi garatuta daude. Adibide gutxi edo irregularrak. Testu-motaren oinarrizko baldintzak betetzen ditu (formatua, hartzailea), baina garapenean hutsuneak daude. |
| 3-4 | Hasiberria | Eskatutako puntu gutxi batzuk bakarrik lantzen ditu, eta ia garatu gabe. Adibiderik ia ez du ematen. Testu-motaren baldintzak partzialki betetzen ditu. Genero, helburu edo irakurlearekiko egokitzapen eskasa. |
| 0-2 | Lortu gabea | Ez du ataza betetzen: gaitik guztiz urruntzen da (off-topic), edo testua laburregia da ebaluatzeko (gutxienez hitz-kopuruaren %30 falta). Ez du testu-motaren eskakizunik betetzen. |

**Sub-adierazleak / Sub-indicadores medibles:**

| ID | Adierazlea | Nola neurtu | Detekzio-mota |
|----|-----------|-------------|---------------|
| AB-1 | Gaiarekiko garrantzia (relevancia) | Lotura semantikoa egitekoaren eta testuaren artean | Semantikoa (IA) |
| AB-2 | Eskakizunen betetzea (cobertura requisitos) | Checklist: eskatutako elementuak kontatu | Kontaketa |
| AB-3 | Garapena (desarrollo) | Baieztapenak adibide/argudio/ondorioekin lagunduak | Semantikoa (IA) |
| AB-4 | Testu-motarekiko egokitzapena (género) | Formatuaren seinaleak: agurra, izenburua, lehen pertsona... | Patroi-bilaketa |
| AB-5 | Erregistroa (registro) | Formaltasun-mailaren klasifikazioa (zuka/hika/neutro) | Semantikoa (IA) |
| AB-6 | Luzera (extensión) | Hitz-kopurua vs espero dena | Kontaketa |

### 2.2. IRIZPIDEA 2: ANTOLAKETA ETA KOHERENTZIA (AK) — 25%

**Qué mide:** ¿Está bien organizado? ¿Tiene estructura? ¿Las ideas están conectadas?

**Oinarri-deskribatzailea ERRM B1:** "Elementu laburren segida bat lotu dezake sekuentzia konektatu lineal batean."

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Egitura argia eta eraginkorra (sarrera-garapena-ondorioa). Paragrafoak ondo bereizita eta ideia bakoitza koherenteki garatua. Lotura-hitz ugari eta egokiak (hala ere, gainera, horregatik, bestalde, horretaz gain...). Erreferentzia-sistema argia (pronominalak, elipsia). Testu-motaren formatua guztiz errespetatua. |
| 7-8 | Aurreratua | Egitura argia du. Paragrafoak ongi antolatuta daude, ideia nagusi bat paragrafo bakoitzean. Lotura-hitz nahikoak eta egokiak, batzuk konplexuak. Akats txikiak koheretzian baina ez dira oztopo. Formatua ia guztiz egokia. |
| 5-6 | Tartekoa | Oinarrizko egitura badu (sarrera-garapena-ondorioa antzematen dira), baina garapena linealegia edo saltoduna izan daiteke. Paragrafoak erabiltzen ditu baina banaketa ez da beti egokia. Oinarrizko lotura-hitzak nagusi dira (eta, baina, beraz, gero). Koherentzia orokorrean mantendu badu ere, saltoren bat edo ilunguneren bat egon daiteke. |
| 3-4 | Hasiberria | Egitura ahula; ideiak nahasita edo ordenatu gabe agertzen dira. Paragrafoen banaketa eskasa edo ez-existitzea. Lotura-hitz gutxi eta oinarrizkoak, edo desegokiak. Salto logiko nabarmenak. Formatuari ia ez dio jaramonik egiten. |
| 0-2 | Lortu gabea | Egiturarik ez da antzematen. Ideiak deskonektatuta agertzen dira, kohesiorik ia ez. Paragraforik ez. Lotura-hitzik ez. |

**Sub-adierazleak:**

| ID | Adierazlea | Nola neurtu | Detekzio-mota |
|----|-----------|-------------|---------------|
| AK-1 | Makro-egitura (estructura global) | Sarrera/garapena/ondorioa identifikatu | Patroi-bilaketa |
| AK-2 | Paragrafoak (párrafos) | Kopurua, batez besteko luzera, gai-batasuna | Kontaketa + IA |
| AK-3 | Lotura-hitzak: kopurua eta aniztasuna (conectores) | Kontatu eta sailkatu (kausa, kontraste, gehiketa...) | Kontaketa |
| AK-4 | Lotura-hitzak: zuzentasuna (uso correcto) | Erlazio logikoa egiaztatu | Semantikoa (IA) |
| AK-5 | Erreferentzia-koherentzia (referencias) | Izenordainak, elipsia, anaforak | Semantikoa (IA) |
| AK-6 | Salto logikoak (saltos) | Gai-aldaketak trantsiziorik gabe | Semantikoa (IA) |

### 2.3. IRIZPIDEA 3: BALIABIDE LINGUISTIKOEN HEDADURA (BLH) — 25%

**Qué mide:** ¿Tiene recursos para expresarse? ¿Vocabulario variado? ¿Estructuras complejas?

**Oinarri-deskribatzailea ERRM B1:** "Hiztegia nahikoa du, zirkumlokuzioekin; mugapen lexikoek errepikapena eragiten dute."

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Hitz-altxor aberatsa eta zehatza; sinonimoak eta esamolde desberdinak tartekatzen ditu errepikapena saihestuz. Perpaus-egitura ugari eta konplexuak erabiltzen ditu (mendekoak, erlatibozkoak, kausazkoak, kontzesiboak). Erregistroa guztiz egokia eta koherentea testu osoan. Ez du formulazio-zailtasunik. Noizean behin esapide idiomatikoak edo esamolde bereziak erabiltzen ditu. |
| 7-8 | Aurreratua | Hitz-altxor nahikoa eta egokia. Batzuetan sinonimoak edo birformulazioak erabiltzen ditu. Perpaus-egitura desberdinak erabiltzen ditu, nahiz eta sinpleagoak nagusi. Erregistroa gehienetan egokia da. Noizean behin formulazio-zailtasun txikiren bat izan dezake. |
| 5-6 | Tartekoa | Oinarrizko hitz-altxorra erabiltzen du, nahikoa ataza betetzeko. Hitz batzuk errepikatzen ditu alternatiba falta delako. Perpaus sinpleak nagusi dira, baina noizean behin konplexuagoak ere erabiltzen ditu. Erregistroa gehienetan egokia bada ere, gorabehera batzuk egon daitezke. |
| 3-4 | Hasiberria | Hitz-altxor mugatua; errepikapen ugari. Perpaus sinple eta laburrak nagusi dira ia beti. Erregistroa ez da egokia edo oso aldakorra da. Hiztegiaren mugek komunikazioa zailtzen dute batzuetan. Kalko lexikoak ager daitezke. |
| 0-2 | Lortu gabea | Oinarrizko hitzak bakarrik. Hitz-altxorraren urritasunak komunikazioa eragozten du. Perpaus-egitura minimoa. |

**Sub-adierazleak:**

| ID | Adierazlea | Nola neurtu | Detekzio-mota |
|----|-----------|-------------|---------------|
| BLH-1 | Aniztasun lexikoa (diversidad léxica) | Type-token ratioa (lemmen arabera); errepikapen-tasa | Kontaketa |
| BLH-2 | Zehaztasun lexikoa (precisión léxica) | "Hitz generikoen" proportzioa (gauza, egin, ona, hori...) vs espezifikoak | Kontaketa + IA |
| BLH-3 | Konplexutasun sintaktikoa (complejidad) | Batez besteko esaldi-luzera + mendeko perpausak 100 hitzeko | Kontaketa |
| BLH-4 | Kalko linguistikoak (calcos estructurales) | Interferentzia-patroi ezagunak (zerrenda heuristikoa) | Patroi-bilaketa |
| BLH-5 | Erregistroa (registro) | Formal/informal nahasketa-detekzioa | Semantikoa (IA) |
| BLH-6 | Esamoldeak eta kolokazio egokiak (fraseología) | Esamolde idiomatikoen presentzia | Semantikoa (IA) |

### 2.4. IRIZPIDEA 4: ZUZENTASUN LINGUISTIKOA (ZL) — 25%

**Qué mide:** ¿Escribe correctamente? ¿Gramática, ortografía, puntuación?

**Oinarri-deskribatzailea ERRM B1:** "Komunikazioa arrazoizko zehaztasunarekin; kontrol orokorrean ona, ama-hizkuntzaren eragin nabarmenarekin; akatsek ez dute ulermena eragozten."

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Akats ortografiko/puntuazio oso gutxi (EP100 ≤ 1 minor, 0 major). Morfologia nominala eta aditz-morfologia ondo kontrolatuta. Kasuen erabilera zuzena. NOR-NORI-NORK sistema zuzen erabiltzen du. Ia ez du ama-hizkuntzaren interferentziarik. |
| 7-8 | Aurreratua | Akats batzuk (EP100 ≤ 3 minor, ≤ 1 major noizean behin) baina ez dute ulermena oztopatzen. Oinarrizko gramatika ondo kontrolatzen du. Ortografia eta puntuazioa nahiko zuzenak. Noizean behineko interferentziak ama-hizkuntzatik. |
| 5-6 | Tartekoa | Akats errepikatuak (EP100 4-6 nahasketa) batez ere kasu-marketan, aditz-adostasunean eta puntuazioan. Testua ulergarria da baina akatsek irakurketa zailtzen dute batzuetan. Ama-hizkuntzaren eragin partziala (erderakada batzuk). |
| 3-4 | Hasiberria | Akats ugari eta sistematikoak (EP100 > 6 edo major-ak maiz). Oinarrizko egituretan ere akatsak. Ulermena tarteka zailtzen da. Ortografia eta puntuazio eskasak. Ama-hizkuntzaren eragin nabarmena (erderakada ugari: kalkoak, gaztelaniazko hitz-ordena...). |
| 0-2 | Lortu gabea | Akats larriak eta oso ugari. Testua ia ulertezina akats kopuruagatik. Interferentzia sistematikoak. |

**Sub-adierazleak:**

| ID | Adierazlea | Nola neurtu | Detekzio-mota |
|----|-----------|-------------|---------------|
| ZL-1 | Ortografia (ortografía) | Grafien erroreak, hitz-banaketa, letra larriak | Kontaketa |
| ZL-2 | Morfologia nominala (declinación) | Kasu-markak (-k, -ri, -ren, -ra, -tik, -rekin...), determinazioa (-a/-ak), zenbakia | Patroi-bilaketa + IA |
| ZL-3 | Aditz-morfologia (conjugación) | Laguntzaile-hautaketa, NOR-NORI-NORK adostasuna, denbora/modua, ezezkoa | Patroi-bilaketa + IA |
| ZL-4 | Sintaxia (sintaxis) | Osagaien ordena, mendeko perpausen formazioa, erlatibozkoak, osagarritasuna | Semantikoa (IA) |
| ZL-5 | Puntuazioa (puntuación) | Komak, puntuak, bi puntuak, komatxoak | Kontaketa + IA |
| ZL-6 | Erderakadak / L1 interferentziak | Kalko sintaktikoak, mailegu desegokiak, gaztelaniazko egitura-kalkoak | Patroi-bilaketa + IA |

---

## 3. ARAU KUANTIFIKAGARRIAK / Reglas cuantificables

### 3.1. Muga-arauak / Reglas "cap" (topes máximos)

Estas reglas anulan la puntuación libre y establecen un máximo cuando se detecta una condición grave. Son binarias y tienen prioridad sobre la evaluación cualitativa.

| ID | Araua | Irizpidea | Cap (gehienezko nota) | Baldintza |
|----|-------|-----------|-----------------------|-----------|
| CAP-1 | Off-topic | AB | **2/10** | Testua gaiarekiko garrantzi semantiko oso baxua du |
| CAP-2 | Eskakizunen %50+ falta | AB | **4/10** | Eskatutako puntuen erdia edo gehiago falta dira |
| CAP-3 | Luzera insuficientea (<70% min) | AB | **4/10** | Hitz-kopurua < gutxieneko %70 |
| CAP-4 | Generoa ez da errespetatzen | AB | **6/10** | Testu-mota okerra (gutun ordez artikulua, etab.) |
| CAP-5 | Egiturarik ez | AK | **4/10** | Sarrera/garapena/ondoriotik 2 falta dira |
| CAP-6 | Inkoherentzia iraunkorra | AK | **6/10** | Salto logiko sistematikoak testu osoan |
| CAP-7 | Perpaus sinpleak soilik | BLH | **6/10** | Ia mendeko perpausik ez testu osoan |
| CAP-8 | Testua ia ulertezina | ZL | **2/10** | Akatsek testua ulertezin egiten dute |

**Lehentasun-ordena:** CAP arauak deskribatzaileen aurretik aplikatzen dira. Adibidez: testu bat off-topic bada, AB irizpidean 2/10 izango du, nahiz eta garatuta egon.

### 3.2. EP100: Akats-dentsitatea / Densidad de errores (para ZL)

EP100 = (akats kopurua × 100) / hitz kopurua

**Akats-sailkapena / Clasificación de errores:**

| Larritasuna | Deskribapena | Adibideak | Pisua EP100n |
|-------------|-------------|-----------|--------------|
| **Minor** | Akats txikia, komunikazioa ez du kaltetzen | Letra larri falta, koma bat falta, typo nabaria | ×1 |
| **Major** | Akats nabarmena, ulermena zailtzen du | Kasu-marka okerra, NOR-NORK nahasketa, aditz okerra | ×2 |
| **Critical** | Akats larria, esaldia ulertezin egiten du | Esaldia zentzurik gabe, aditza guztiz okerra, hitz-ordena ulertezina | ×3 |

**EP100 pisuduna = (minor×1 + major×2 + critical×3) × 100 / hitz kopurua**

| Banda | EP100 pisuduna (orientagarria) | Nota-tartea |
|-------|-------------------------------|-------------|
| Bikaintasuna | ≤ 2 | 9-10 |
| Aurreratua | 3-5 | 7-8 |
| Tartekoa | 6-10 | 5-6 |
| Hasiberria | 11-18 | 3-4 |
| Lortu gabea | > 18 | 0-2 |

**OHARRA:** EP100 orientagarria da, ez erabakigarria. IAk deskribatzaileak eta EP100 biak erabiltzen ditu nota jartzeko. EP100 bakarrik ez da nahikoa.

### 3.3. Penalizazio-sistema / Sistema de penalizaciones (AB, AK, BLH)

AB, AK eta BLH irizpideetan, cap arauak ez badira aplikatzen, IAk deskribatzaileen arabera nota jartzen du eta penalizazio txikiak aplika ditzake:

| ID | Penalizazioa | Irizpidea | Balioa | Gehienezko metatze |
|----|-------------|-----------|--------|---------------------|
| PEN-1 | Eskakizun bat garatu gabe | AB | -0.5 | -2.0 |
| PEN-2 | Paragrafo bakarra | AK | -0.5 | -0.5 |
| PEN-3 | Paragrafo batean gai-apurketa | AK | -0.2 | -1.0 |
| PEN-4 | Lotura-hitz okerra (erlazio logiko faltsua) | AK | -0.5 | -1.5 |
| PEN-5 | Errepikapen lexiko nabarmena (sostenida) | BLH | -0.5 | -1.5 |
| PEN-6 | Hitz generikoen gehiegizko erabilera | BLH | -0.3 | -1.0 |
| PEN-7 | Erregistro-nahasketa | BLH | -0.5 | -1.0 |

**OHARRA:** Penalizazioak deskribatzaileak jarritako notaren barruan aplikatzen dira, ez gehigarri gisa. Adibidez, deskribatzaileen arabera 7 bada eta PEN-2 aplikatzen bada, emaitza 6.5 izango da, ez 6.5 ken beste penalizazio guztiak.

### 3.4. Bonifikazioak / Bonificaciones (opcional)

| ID | Bonifikazioa | Irizpidea | Balioa | Baldintza |
|----|-------------|-----------|--------|-----------|
| BON-1 | Esamolde idiomatikoak | BLH | +0.3 | Kolokazio edo esamolde natural eta egokiak erabiltzen ditu |
| BON-2 | Ikuspegi originala | AB | +0.3 | Ideia edo planteamendu bereziki originala |
| BON-3 | Kohesio-baliabide aurreratuak | AK | +0.3 | Anafora, elipsi edo erreferentzia-baliabide konplexuak egoki erabiltzen ditu |

Bonifikazioak ez dute 10/10 gainditu behar.

---

## 4. AKATS-KATALOGOA / Catálogo de fallos tipificados

### 4.1. Atazaren betetzea (AB) — Fallos de contenido

| ID | Akatsa (EU) | Fallo (ES) | Detekzio-bidea | Larritasuna |
|----|------------|-----------|----------------|-------------|
| TB-1 | Gaitik urrun | Off-topic | Lotura semantiko baxua egitekoarekin | Critical → CAP-1 |
| TB-2 | Eskakizun-falta | Requisitos incumplidos | Checklist: eskatutako elementuak kontatu | Major → CAP-2 |
| TB-3 | Garapen eskasa | Desarrollo insuficiente | Baieztapenak laguntza gabe | Media → PEN-1 |
| TB-4 | Generoa ez du errespetatzen | Género no respetado | Formato-seinaleak falta | Major → CAP-4 |
| TB-5 | Erregistro desegokia | Registro inadecuado | Formaltasun-marka desegokiak | Media → PEN-7 |
| TB-6 | Testua laburregia | Texto insuficiente | Hitz-kopurua < %70 | Major → CAP-3 |

### 4.2. Antolaketa eta koherentzia (AK) — Fallos de organización

| ID | Akatsa (EU) | Fallo (ES) | Detekzio-bidea | Larritasuna |
|----|------------|-----------|----------------|-------------|
| OK-1 | Egiturarik ez | Sin estructura | Sarrera/garapena/ondorioa falta | Major → CAP-5 |
| OK-2 | Paragrafo-banaketa eskasa | Mala paragrafación | Paragrafo bakarra edo luzeegia | Media → PEN-2, PEN-3 |
| OK-3 | Lotura-hitz eskasak | Conectores pobres/repetitivos | Kontaketa + aniztasuna | Media |
| OK-4 | Lotura-hitz okerrak | Conectores mal usados | Erlazio logiko faltsua | Major → PEN-4 |
| OK-5 | Erreferentzia nahasak | Referencias ambiguas | Izenordainak aurrekaririk gabe | Major |
| OK-6 | Salto logikoak | Saltos lógicos | Gai-aldaketa trantsiziorik gabe | Major → CAP-6 |

### 4.3. Baliabide linguistikoen hedadura (BLH) — Fallos de riqueza

| ID | Akatsa (EU) | Fallo (ES) | Detekzio-bidea | Larritasuna |
|----|------------|-----------|----------------|-------------|
| LH-1 | Errepikapen lexiko altua | Repetición léxica alta | Type-token ratioa | Media → PEN-5 |
| LH-2 | Hiztegia generikoegia | Léxico genérico | gauza, egin, ona, hori... proportzioa | Media → PEN-6 |
| LH-3 | Konplexutasun sintaktiko eskasa | Poca variedad sintáctica | Perpaus sinpleak soilik | Media → CAP-7 |
| LH-4 | Egitura-kalkoak | Calcos estructurales | Interferentzia-patroi zerrenda | Media-Major |
| LH-5 | Erregistro ezegonkorra | Registro inestable | Formal + informal nahasketa | Media → PEN-7 |
| LH-6 | Esamolderik ez | Sin fraseología | Kolokazio/esamolde naturalik ez | Minor → BON-1 |

### 4.4. Zuzentasun linguistikoa (ZL) — Errores contables

#### 4.4.1. Ortografia

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-ORT-1 | Grafia okerra | *gaurko → gaueroko* (?) Kontestuaren arabera | Minor-Major |
| ZL-ORT-2 | Hitz-banaketa/elkarketa | *alde batetik → aldetik* (?) / *etxekoandreak → etxeko andreak* | Minor |
| ZL-ORT-3 | Letra larriak | *bilbon → Bilbon*, *astelehena → astelehena* (ondo) | Minor |
| ZL-ORT-4 | Maileguen ortografia | *futbola → futbola* (ondo) / *sofware → software* | Minor |

#### 4.4.2. Morfologia nominala (deklinabidea)

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-KAS-1 | Absolutiboa (-Ø/-a) vs ergatiboa (-k) | *nik gustatu da → niri gustatu zait* | Major |
| ZL-KAS-2 | Datiboa (-ri) | *nire lagunari eman diot → ✓* / *nire laguna eman diot → ✗* | Major |
| ZL-KAS-3 | Genitiboa (-ren) | *Mikelena → Mikelen* (possesiboa) | Minor-Major |
| ZL-KAS-4 | Adlatiboa (-ra) | *eskolan joan → eskolara joan* | Major |
| ZL-KAS-5 | Ablatiboa (-tik) | *etxera etorri → etxetik etorri* (kontestua) | Major |
| ZL-KAS-6 | Soziatiboa (-rekin) | *nire lagunekin → ✓* / *nire lagunarekin → ✓* (zenbakia) | Minor |
| ZL-KAS-7 | Determinazioa (-a/-ak) | *gizon bat etorri da → ✓* / *gizon etorri da → ✗* | Major |
| ZL-KAS-8 | Mugagabea vs mugatua | *ez dut liburu → ez dut libururik* | Major |

#### 4.4.3. Aditz-morfologia

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-ADI-1 | Laguntzaile-hautaketa (NOR vs NOR-NORK vs NOR-NORI-NORK) | *nik ikusi naiz → nik ikusi dut* | Critical |
| ZL-ADI-2 | Pertsona-adostasuna | *guk joan gara → ✓* / *guk joan naiz → ✗* | Major |
| ZL-ADI-3 | Numero-adostasuna | *umeak etorri da → umeak etorri dira* | Major |
| ZL-ADI-4 | Aldia (tempusa) | *atzo joango naiz → atzo joan nintzen* | Major |
| ZL-ADI-5 | Modua (subjuntiboa, ahalezkoa...) | *nahi dut joatea → joan nahi dut* / *nahi dut joan dadin* | Minor-Major |
| ZL-ADI-6 | Ezezkoa | *ez dut ikusi → ✓* / *ez ikusi dut → ✗* | Major |
| ZL-ADI-7 | Aditz-perifrasia | *hasi da egiten → hasi da egiten* (ondo) / *hasi da egitera → ✗ (kontestua)* | Minor-Major |

#### 4.4.4. Sintaxia

| ID | Akatsa | Adibidea | Larritasuna |
|----|--------|---------|-------------|
| ZL-SIN-1 | Osagaien ordena | SOV ordena ez errespetatzea (nabarmena bada) | Minor-Major |
| ZL-SIN-2 | Mendeko perpaus gaizki eratua | *...delako ikusi dut → ...delako, ikusi dut* | Major |
| ZL-SIN-3 | Erlatibozko gaizki eratua | *gizona ikusi dudana → ikusi dudan gizona* | Major |
| ZL-SIN-4 | Osagarritasun arazoak | *pentsatzen dut hori ona da → pentsatzen dut hori ona dela* | Major |

#### 4.4.5. Puntuazioa

| ID | Akatsa | Adibidea | Larritasuna |
|----|--------|---------|-------------|
| ZL-PUN-1 | Punturik ez esaldien artean | Esaldi luzea geldiunerik gabe | Major |
| ZL-PUN-2 | Koma deserosoa | Koma subjektu eta aditz artean | Minor |
| ZL-PUN-3 | Bi puntuen erabilera okerra | | Minor |
| ZL-PUN-4 | Komatxoen falta/soberan | | Minor |

#### 4.4.6. Erderakadak / Interferentziak

| ID | Akatsa | Adibidea (gaizki → ondo) | Larritasuna |
|----|--------|--------------------------|-------------|
| ZL-ERD-1 | Kalko sintaktikoa | *horren garrantzitsua da ezen → hain garrantzitsua da, non...* | Major |
| ZL-ERD-2 | Mailegu desegokia | *entonces → orduan/beraz* | Minor-Major |
| ZL-ERD-3 | Hitz-ordena gaztelaniakoa | *liburu interesgarri bat → liburu interesgarri bat* (baina: *interesgarria den liburu bat*) | Minor-Major |
| ZL-ERD-4 | Preposizio-kalkoa | *-gatik, -rentzat, -buruz* erabilera desegokiak | Major |
| ZL-ERD-5 | Mugatzaile-arazoak | *Bilbo hiria → Bilbo hiria* (baina: *el Bilbao / la ciudad de Bilbao → Bilbo*) | Minor |

---

## 5. FEEDBACK MOTAK / Tipos de feedback al alumno

### 5.1. Feedback-egitura / Estructura del feedback

La IA genera tres niveles de feedback por cada evaluación:

```
FEEDBACK EGITURA:

1. LABURPEN OROKORRA (Resumen global)
   └── 3-4 esaldi: nota globala + maila + inpresio orokorra

2. IRIZPIDE BAKOITZEKO FEEDBACKA (Feedback por criterio × 4)
   ├── Nota + maila
   ├── 2 indarguneak ("zer egin du ondo")
   ├── 2 hobetzeko proposamenak ("zer hobetu behar du")
   └── Ebidentzia: testuaren aipu laburrak (1-2 esaldi)

3. AKATS-ZERRENDA (Lista de errores — solo para ZL)
   ├── Kategoria (ortografia / kasuak / aditza / puntuazioa / erderakada)
   ├── Detektatutakoa → proposatutako zuzenketa
   ├── Larritasuna (minor / major / critical)
   └── "Zalantzazkoa" marka (anti-aluzinazioa)
```

### 5.2. Hizkuntza eta tonua / Lengua y tono del feedback

- **Hizkuntza:** Feedbacka beti **euskaraz**
- **Tonua:** Positiboa eta konstruktiboa, zuzentzailea baina ez humiliagarria
- **Pertsona:** "Zuk" (errespetuzko tratamendua)
- **Formatua:** Esaldi laburrak, zuzenak, adibide konkretuak testuaren bertatik

### 5.3. Feedback-txantiloiak / Plantillas de feedback

#### 5.3.1. Laburpen orokorra — txantiloia

```
[NOTA]/10 — [MAILA]

[Inpresio positibo orokor bat]. [Hobetzeko arlo nagusia]. [Animatzeko esaldi bat].
```

**Adibidea (tartekoa):**
```
6.0/10 — Tarteko maila

Iritzi-artikulu ulergarri bat idatzi duzu gaiaren inguruan, argudio batzuk garatuz.
Egitura hobetu beharko zenuke, batez ere paragrafoen banaketa eta lotura-hitzen
aniztasuna. Jarraitu lanean, norabide onean zaude!
```

**Adibidea (aurreratua):**
```
7.5/10 — Maila aurreratua

Iritzi-artikulu ondo egituratua eta arrazoitua idatzi duzu. Zure argudioak garatu
eta adibideekin lagundu dituzu. Zuzentasunean akats batzuk zuzendu behar dituzu,
batez ere kasu-marketan. Lan bikaina!
```

**Adibidea (hasiberria):**
```
3.5/10 — Hasierako maila

Gaiaren inguruan idazten saiatu zara, baina ideiak gehiago garatu behar dituzu eta
testuak egitura argiagoa behar du. Hurrengo aldian, saiatu sarrera, garapena eta
ondorio bat bereizten. Badaukazu oinarria hobetzeko!
```

#### 5.3.2. Irizpide-feedbacka — txantiloia

```
[IRIZPIDEA] ([NOTA]/10 — [MAILA]):

✓ Indargunea 1: [Zerbait zehatza ondo egin duena, testuaren adibidearekin]
✓ Indargunea 2: [Beste zerbait]

△ Hobetu: [Proposamen konkretu bat, posible bada adibidearekin]
△ Hobetu: [Beste proposamen bat]
```

**Adibide osoa (Zuzentasun linguistikoa, tartekoa):**

```
ZUZENTASUN LINGUISTIKOA (5/10 — Tarteko maila):

✓ Aditz-denborak ondo hautatzen dituzu: lehenaldia eta orainaldian ondo bereizten
  dituzu testu osoan.
✓ Ortografia orokorrean nahiko egokia da; akats gutxi egiten dituzu idazkera arruntean.

△ Hobetu: NOR-NORK sistema. 3 aldiz nahasi duzu: "nik gustatu da" idatzi beharrean
  "niri gustatu zait" erabili behar da (NOR-NORI: gustatu + nori). Antzeko akatsa
  2. paragrafoan: "guk ikusi gara" → "guk ikusi dugu" (NOR-NORK).
△ Hobetu: Kasu-markak adlatiboan. "Eskolara" (nora) eta "eskolan" (non) ondo bereizten
  dituzu gehienetan, baina "etxe joan" idatzi duzu; zuzena: "etxeRA joan".

Erderakada bat antzeman da: "es que hori horrela da" → saiatu "hori horrela
delako da" erabiltzen (kausa-egitura euskaraz).
```

#### 5.3.3. Akats-zerrenda — txantiloia

```
AKATS-ZERRENDA:

# | Kategoria | Detektatutakoa | Zuzenketa proposatua | Larritasuna | Oharra
1 | ZL-KAS-4 | "eskolan joan" | "eskolara joan" | Major |
2 | ZL-ADI-1 | "nik gustatu da" | "niri gustatu zait" | Critical |
3 | ZL-ADI-2 | "guk ikusi gara" | "guk ikusi dugu" | Major |
4 | ZL-ERD-2 | "entonces" | "orduan" / "beraz" | Minor |
5 | ZL-PUN-1 | 3. esaldia (punturik gabe) | Puntua jarri | Minor |
6 | ZL-KAS-2 | "lagunari kontatu diot" | ✓ (zuzena da) | — | Zalantzazkoa
```

**OHARRA:** Azken errenkadan "Zalantzazkoa" agertzen da. IAri eskatzen zaio bere zuzenketaz seguru ez dagoenean horrela markatzea, asmatu beharrean. Hau anti-aluzinazioa da.

---

## 6. IRTEERA-ADIBIDE OSOAK / Ejemplos completos de salida de la IA

### 6.1. Adibidea 1: Iritzi-artikulua, DBH 3, tarteko maila

**Egitekoa:** "Idatzi iritzi-artikulu bat mugikorren erabilerari buruz ikasgelan. Gutxienez bi argudio alde eta bat kontra eman behar dituzu. 150-250 hitz. Erregistro formala."

**Ikaslearen testua (simulatua, 175 hitz):**

*"Gaur egun mugikorra oso garrantzitsua da gure bizitzan. Nik uste dut mugikorrak ikasgelan erabili behar direla.
Alde batetik, mugikorrak informazioa bilatzeko oso onak dira. Adibidez, klasean zerbait ez dakigunean, mugikorrarekin bilatu dezakegu eta azkarrago ikasten dugu. Gainera, aplikazio batzuk daude ikasten laguntzen dutenak.
Baina ere egia da mugikorrak distraitu egiten dutela. Batzuetan ikasleak jolasean edo sare sozialetan egoten dira irakaslea azaltzen ari denean.
Beraz, nik uste dut mugikorrak erabili behar dira baina arau batzuekin. Irakasleak esan behar du noiz erabili eta noiz ez. Horrela, guztiontzat hobea izango da.
Ondorioz, mugikorrak tresna onak dira ikasteko baina kontrolarekin erabili behar dira ikasgelan."*

**IA-ren irteera / Salida completa de la IA:**

```json
{
  "kodea": "3A017",
  "ebaluazioa": {
    "atazaren_betetzea": {
      "nota": 7,
      "maila": "aurreratua",
      "iruzkina": {
        "indarguneak": [
          "Eskatutako hiru argudioak lantzen dituzu: bi alde (informazio-bilaketa eta aplikazioak) eta bat kontra (distrakzioa).",
          "Erregistro formala mantentzen duzu testu osoan eta iritzi-artikuluaren formatua errespetatzen duzu."
        ],
        "hobetzekoak": [
          "Argudioak gehiago garatu: 'aplikazio batzuk daude ikasten laguntzen dutenak' — zeintzuk? Adibide konkretu bat eman (Kahoot, Quizlet...) hobeto konbentzitzeko.",
          "Kontrako argudioa azalegiegia da. 'Batzuetan ikasleak jolasean egoten dira' gehiago azal dezakezu: zenbat denbora galtzen dute? Zer eragin du notetan?"
        ]
      }
    },
    "antolaketa_koherentzia": {
      "nota": 7,
      "maila": "aurreratua",
      "iruzkina": {
        "indarguneak": [
          "Sarrera, garapena eta ondorio argia ditu. Egitura logikoa eta jarraitzeko erraza da.",
          "Paragrafoen banaketa egokia da: paragrafo bakoitzak ideia nagusi bat lantzen du."
        ],
        "hobetzekoak": [
          "Lotura-hitzetan aniztasun gehiago: 'alde batetik... gainera... baina... beraz... ondorioz' erabiltzen dituzu, eta ondo daude, baina 'hala ere', 'horretaz gain', 'bestalde' bezalakoak ere txertatu ditzakezu.",
          "'Baina ere egia da' → 'hala ere' edo 'bestalde' naturalagoak dira euskaraz. 'Baina ere' gaztelaniazko 'pero también'-ren kalkoa da."
        ]
      }
    },
    "baliabide_linguistikoen_hedadura": {
      "nota": 5,
      "maila": "tartekoa",
      "iruzkina": {
        "indarguneak": [
          "Oinarrizko hitz-altxorra egokia da gairako: 'mugikorra', 'informazioa', 'aplikazioa', 'sare sozialak', 'tresna'.",
          "Mendeko perpaus batzuk erabiltzen dituzu: '...ez dakigunean', '...laguntzen dutenak', '...azaltzen ari denean'."
        ],
        "hobetzekoak": [
          "'Nik uste dut' 3 aldiz agertzen da. Saiatu 'nire ustez', 'nire iritziz', 'nire aburuz' ere erabiltzen errepikapena saihesteko.",
          "Hitz generikoak nagusi dira: 'onak dira', 'oso garrantzitsua', 'hobea izango da'. Zehaztasun gehiago: 'baliagarriak dira', 'funtsezko tresna bihurtu dira', 'eraginkorragoa izango da'."
        ]
      }
    },
    "zuzentasun_linguistikoa": {
      "nota": 6,
      "maila": "tartekoa",
      "iruzkina": {
        "indarguneak": [
          "Aditz-denborak ondo hautatzen dituzu (orainaldi orokorra artikulu baterako).",
          "Kasu-marka gehienak ondo erabiltzen dituzu: '-an', '-ekin', '-tzeko'."
        ],
        "hobetzekoak": [
          "'Baina ere egia da' — 'ere' kokapena: zuzena 'baina egia ere bada' edo 'hala ere, egia da' litzateke. Gaztelaniazko 'pero también' kalkotzat har daiteke.",
          "'Mugikorrak distraitu egiten dutela' — 'distraitu' gaztelaniazko mailegatik dator; 'arreta galdu', 'arreta desbideratu' edo 'jo eta ke ibili' naturalagoak dira."
        ]
      }
    }
  },
  "laburpena": {
    "batez_bestekoa": 6.25,
    "biribiltzea": 6.0,
    "heziberri_maila": "tartekoa",
    "orokorra": "Iritzi-artikulu ulergarri eta ondo egituratua idatzi duzu. Argudioak landu dituzu baina gehiago garatu behar dituzu adibide konkretuagoekin. Hitz-altxorra zabaldu eta errepikapena saihestu behar duzu. Norabide onean zaude!"
  },
  "akats_zerrenda": [
    {
      "zenbakia": 1,
      "kategoria": "ZL-ERD-1",
      "detektatutakoa": "baina ere egia da",
      "zuzenketa": "hala ere, egia da / bestalde, egia da",
      "larritasuna": "minor",
      "zalantzazkoa": false
    },
    {
      "zenbakia": 2,
      "kategoria": "ZL-ERD-2",
      "detektatutakoa": "distraitu egiten dutela",
      "zuzenketa": "arreta galarazten / arreta desbideratzen dutela",
      "larritasuna": "minor",
      "zalantzazkoa": true
    },
    {
      "zenbakia": 3,
      "kategoria": "ZL-PUN-2",
      "detektatutakoa": "Beraz, nik uste dut mugikorrak erabili behar dira baina arau batzuekin.",
      "zuzenketa": "...erabili behar dira, baina arau batzuekin.",
      "larritasuna": "minor",
      "zalantzazkoa": false
    }
  ],
  "EP100": {
    "minor": 3,
    "major": 0,
    "critical": 0,
    "EP100_gordina": 1.71,
    "EP100_pisuduna": 1.71
  },
  "segurtasun_azterketa": {
    "susmagarria": false,
    "oharrak": "Idazketa-patroia normala, maila koherentea ikaslearen profila kontuan hartuta."
  }
}
```

### 6.2. Adibidea 2: Gutun formala, DBH 4, hasiberria

**Egitekoa:** "Idatzi gutun formal bat zure udaletxeari zuhaitz gehiago landatzeko eskatuz. Arrazoiak eman. 150-200 hitz. Zuka."

**Ikaslearen testua (simulatua, 95 hitz):**

*"Kaixo,
Nik nahi dut zuhaitzak parkean jarri. Parkean ez dago zuhaitzik eta udaran bero handia egiten du. Gainera zuhaitzak onak dira airearentzat.
Nire lagunak eta biok parkera joaten gara egunero baina ez dago sombra eta ez daukagu leku onik esertzeko.
Eskerrik asko.
Agur"*

**IA-ren irteera:**

```json
{
  "kodea": "4B008",
  "ebaluazioa": {
    "atazaren_betetzea": {
      "nota": 3,
      "maila": "hasiberria",
      "cap_aplikatua": "CAP-3",
      "cap_arrazoia": "Testua 95 hitz: eskatutako 150 hitzetatik %63 soilik (< %70 muga).",
      "iruzkina": {
        "indarguneak": [
          "Gaia lantzen du: zuhaitzak landatzea eskatzen du udaletxeari.",
          "Bi arrazoi ematen ditu: beroa udaran eta airea."
        ],
        "hobetzekoak": [
          "Testua laburregia da (95 hitz, 150 eskatuta). Arrazoiak gehiago garatu behar dituzu: zenbat zuhaitz? Non zehazki? Zer motatako zuhaitzak?",
          "Gutun formal batek helburu argiagoa behar du: zer eskatzen duzun zehazki, eta zer egin dezakeen udaletxeak. Proposamen konkretu bat gehitu."
        ]
      }
    },
    "antolaketa_koherentzia": {
      "nota": 4,
      "maila": "hasiberria",
      "iruzkina": {
        "indarguneak": [
          "Gutunaren oinarrizko formatua badu: agurra hasieran eta amaieran.",
          "'Gainera' lotura-hitza erabiltzen du bigarren argudioa sartzeko."
        ],
        "hobetzekoak": [
          "Gutun formalak sarrera-formula behar du: 'Udal agintari agurgarria' edo 'Jaun/Andre agurgarria'. 'Kaixo' informalegia da gutun formal baterako.",
          "Gorputzean paragrafoak bereizi: lehenengo paragrafoan zergatik idazten duzun azaldu, bigarrenean arrazoiak, hirugarrenean eskaera formala."
        ]
      }
    },
    "baliabide_linguistikoen_hedadura": {
      "nota": 3,
      "maila": "hasiberria",
      "iruzkina": {
        "indarguneak": [
          "Oinarrizko hitz-altxorra du gaia lantzeko: 'zuhaitzak', 'parkea', 'airea'.",
          "Perpaus bat mendekoa da: 'esertzeko'."
        ],
        "hobetzekoak": [
          "Hitz-altxorra oso mugatua da. 'Onak dira' ordez saiatu: 'onuragarriak dira', 'lagungarriak dira', 'ezinbestekoak dira'. 'Parkean' 3 aldiz agertzen da; erabili 'gune horretan', 'espazio berdean'.",
          "Erregistroa ez da formala: 'nik nahi dut' → 'eskatu nahiko nizuke' edo 'proposatu nahi dut'. Gutun formal batean 'zuka' idatzi behar da."
        ]
      }
    },
    "zuzentasun_linguistikoa": {
      "nota": 4,
      "maila": "hasiberria",
      "iruzkina": {
        "indarguneak": [
          "Oinarrizko perpaus-egiturak zuzen idazten ditu: 'Parkean ez dago zuhaitzik'.",
          "Ezezkoa ondo jartzen du: 'ez dago', 'ez daukagu'."
        ],
        "hobetzekoak": [
          "'sombra' → gaztelaniazko hitza da; euskaraz 'itzala' edo 'gerizpea' erabili.",
          "'Nire lagunak eta biok' → 'nire laguna eta biok' (bi pertsona badira) edo 'nire lagunak eta ni'. Zenbakia zehaztu behar da."
        ]
      }
    }
  },
  "laburpena": {
    "batez_bestekoa": 3.5,
    "biribiltzea": 3.5,
    "heziberri_maila": "hasiberria",
    "orokorra": "Gaia lantzen saiatu zara, baina testua laburregia da eta gutun formalaren eskakizunak hobeto bete behar dituzu. Hurrengo aldian, luzatu testua arrazoiak garatuz, erregistro formala erabili (zuka), eta gutunaren egitura formala jarraitu. Oinarria badaukazu!"
  },
  "akats_zerrenda": [
    {
      "zenbakia": 1,
      "kategoria": "ZL-ERD-2",
      "detektatutakoa": "sombra",
      "zuzenketa": "itzala / gerizpea",
      "larritasuna": "major",
      "zalantzazkoa": false
    },
    {
      "zenbakia": 2,
      "kategoria": "ZL-KAS-7",
      "detektatutakoa": "airearentzat",
      "zuzenketa": "airearentzat (zuzena, baina kontestuan 'airearen kalitaterako' hobea)",
      "larritasuna": "minor",
      "zalantzazkoa": true
    },
    {
      "zenbakia": 3,
      "kategoria": "ZL-PUN-1",
      "detektatutakoa": "Gainera zuhaitzak onak dira",
      "zuzenketa": "Gainera, zuhaitzak onak dira",
      "larritasuna": "minor",
      "zalantzazkoa": false
    },
    {
      "zenbakia": 4,
      "kategoria": "TB-5",
      "detektatutakoa": "Kaixo (gutun formalean)",
      "zuzenketa": "'Jaun/Andre agurgarria' edo 'Udal agintari agurgarria'",
      "larritasuna": "major",
      "zalantzazkoa": false
    }
  ],
  "EP100": {
    "minor": 2,
    "major": 2,
    "critical": 0,
    "EP100_gordina": 4.21,
    "EP100_pisuduna": 6.32
  },
  "segurtasun_azterketa": {
    "susmagarria": false,
    "oharrak": ""
  }
}
```

---

## 7. ANTI-ALUZINAZIOA / Medidas contra alucinaciones de la IA

### 7.1. Arau zehatza IArentzat

La IA DEBE seguir estas reglas para evitar correcciones incorrectas:

1. **"Zalantzazkoa" marka:** Si la IA no está segura de una corrección (especialmente en morfología verbal vasca, que es compleja), debe marcarlo como `"zalantzazkoa": true` en la lista de errores.

2. **Ez asmatu:** La IA no debe inventar reglas gramaticales del euskera. Si no está segura de una forma verbal o una declinación, debe indicar la duda en vez de proponer una corrección potencialmente incorrecta.

3. **Kontestua kontuan hartu:** Muchas formas en euskera son correctas en un contexto e incorrectas en otro. La IA debe considerar el contexto completo de la oración.

4. **Positibo faltsuak minimizatu:** Es preferible no señalar un error real que señalar algo correcto como error. Los falsos positivos destruyen la confianza del alumno en el sistema.

5. **Dialektoak:** No penalizar formas dialectales legítimas. El euskera batua es la referencia, pero formas como "egin dau" (bizkaieraz) en vez de "egin du" no son necesariamente errores en todos los contextos educativos. El profesor puede especificar esto en la ataza-fitxa.

### 7.2. Kalibraketa-prozesua / Proceso de calibración

Para que el sistema funcione con precisión:

1. Corregir a mano 10-20 redacciones reales con esta rúbrica
2. Pasar las mismas redacciones por la IA
3. Comparar: ¿las notas difieren en más de 1 punto? ¿Los errores señalados coinciden?
4. Ajustar: umbrales de EP100, caps, penalizaciones
5. Crear 2-3 "textos ancla" (aingura-testuak) como calibración permanente del prompt
6. Repetir hasta que la correlación sea aceptable (objetivo: ≤ 1 punto de diferencia en el 80% de los casos)

---

## 8. TESTU-MOTA ZEHATZEN OHARRAK / Notas por tipología textual

La rúbrica es genérica para todas las tipologías, pero cada tipo de texto tiene requisitos específicos que se activan a través de la ataza-fitxa. Aquí van las claves:

| Testu-mota | AB: zer espero den | AK: egitura espezifikoa | BLH: erregistroa | ZL: arreta berezia |
|------------|-------------------|------------------------|-------------------|---------------------|
| **Iritzi-artikulua** | Tesia + argudioak (alde/kontra) + ondorioa | Tesia → argudioak → kontrargumentua → ondorioa | Formala / akademikoa | Argudio-lokailuak: "hala ere", "bestalde"... |
| **Gutun formala** | Helburua + arrazoiak + eskaera | Agurra → sarrera → gorputza → eskaera → agur formala | Formala (zuka) | Agur-formulak, eskaera-egiturak |
| **Gutun informala** | Mezua argi komunikatu | Agurra → berria → amaiera | Informala | Tonu naturala, ez penalizatu hika |
| **Deskribapena** | Xehetasun sentsorialak | Orokorretik zehatzera / espazial-ordena | Neutrala | Adjektiboen aniztasuna |
| **Hausnarketa** | Gogoeta pertsonala + arrazoiketa | Hasierako galdera → garapena → ondorioa | Pertsonala | Lehen pertsona, iritzi-adierazleak |
| **Gidoia** | Pertsonaiak + elkarrizketa + ekintza | Eszenak → akotazioak → elkarrizketak | Pertsonaien arabera | Elkarrizketa naturala, akotazio-formatua |
| **Narrazioa** | Istorioa kontatu | Hasiera → korapiloa → amaiera | Narraziozkoa | Aditz-denborak (lehenaldia) |

---

## 9. PROMPT-EGITURA / Estructura del prompt de sistema

El prompt final para la IA se construye así:

```
┌─────────────────────────────────────────────────────────┐
│ SISTEMA (fijo — beti berdina)                           │
│ ├── Rola: Euskal Hizkuntza eta Literaturako irakaslea   │
│ ├── Ebaluazio-sistema: ERRM B1 + Heziberri 2020        │
│ ├── Output formatua: JSON (egitura zehatza)             │
│ ├── Anti-aluzinazioa: zalantzazkoa markatu, ez asmatu   │
│ └── Feedbackaren hizkuntza: euskara                     │
├─────────────────────────────────────────────────────────┤
│ ERRUBRIKA (fijo — dokumentu honetako 2. atala)          │
│ ├── 4 irizpideak + deskribatzaileak                     │
│ ├── Cap arauak (3. atala)                               │
│ ├── EP100 bandak                                        │
│ └── Penalizazioak eta bonifikazioak                     │
├─────────────────────────────────────────────────────────┤
│ ATAZA-FITXA (aldagarria — azterketa bakoitzean)         │
│ ├── Egitekoa (enuntziatu zehatza)                       │
│ ├── Testu-mota + erregistroa                            │
│ ├── Maila (DBH3/DBH4)                                  │
│ ├── Hitz-kopurua (min-max)                              │
│ ├── Eduki espezifikoak (checklist)                      │
│ └── Ebaluazio-oharrak (irakaslearen oharrak)            │
├─────────────────────────────────────────────────────────┤
│ AINGURA-TESTUAK (aukerakoa — kalibrazioa)               │
│ ├── Adibidea 8/10: testua + ebaluazioa                  │
│ └── Adibidea 5/10: testua + ebaluazioa                  │
├─────────────────────────────────────────────────────────┤
│ IKASLEAREN TESTUA (aldagarria — ikasle bakoitzean)      │
│ └── Testua + metadatuak (kodea, hitz-kopurua, denbora)  │
└─────────────────────────────────────────────────────────┘
```

---

## 10. INPLEMENTAZIO-ORDENA / Orden de implementación

Este documento se traduce al código en este orden:

| Lehentasuna | Fitxategia | Zer da | Dokumentu honetan |
|-------------|-----------|--------|-------------------|
| 1 | `errubrika.json` | Rúbrica + caps + EP100 + catálogo de fallos | Atalak 2, 3, 4 |
| 2 | `sistema_prompt.txt` | Prompt de sistema con rol, reglas, formato output | Atala 9 |
| 3 | `zuzendu_test.py` | Script mínimo: texto → API → JSON evaluación | Atala 6 (ejemplos) |
| 4 | Calibración con textos reales | Corregir 10-20 textos a mano, comparar con IA | Atala 7.2 |
| 5 | `aingurak/` | Textos ancla de calibración permanente | Atala 9 |
| 6 | Feedback display / XLSX | Formatear el JSON de salida para uso en aula | Atala 5 |

---

*ZUZENDU — Zuzenketa-eredu behin betikoa. v1.0. 2026-02-09.*
