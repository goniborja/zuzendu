# ZUZENDU — Euskarazko idatzizko ekoizpenaren ebaluazio-sistema

## Proiektuaren laburpena

**ZUZENDU** es un ecosistema completo de evaluación de escritura en euskera para DBH 3 y DBH 4, diseñado para que una IA corrija redacciones y pruebas de escritura bajo los criterios del profesor, alineados con el Marco Común Europeo de Referencia para las Lenguas (MCER/ERRM) nivel B1 y traducidos al marco competencial Heziberri 2020.

El sistema cubre el ciclo completo: **diseñar exámenes → examinar → corregir → informar → calificar**.

---

## 1. ARKITEKTURA OROKORRA

```
ZUZENDU EKOSISTEMA

┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  SORTZAILEA  │───►│  AZTERKETA   │───►│ ZUZENTZAILEA │───►│  EMAITZAK    │───►│ KOADERNOA   │
│  (Diseñador) │    │  (Examen)    │    │ (Corrector)  │    │ (Resultados) │    │ (Cuaderno)  │
│              │    │              │    │              │    │              │    │             │
│  Irakaslea   │    │  Ikaslea     │    │  Script+IA   │    │  XLSX+JSON   │    │ XLSX global │
│  configura   │    │  idazten du  │    │  automatikoa │    │  por examen  │    │ curso entero│
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

### 1.1. Las cinco fases

| Fasea | Tresna | Sarrera (input) | Irteera (output) |
|-------|--------|-----------------|-------------------|
| **1. SORTZAILEA** | HTML (irakasle-interfazea) | Egitekoa, parametroak, ikasle-zerrenda | azterketa.html (examen generado) |
| **2. AZTERKETA** | HTML (ikasle-interfazea) | Ikaslearen testua | JSON fitxategiak (uno por alumno) |
| **3. ZUZENTZAILEA** | Python scripta + Claude API | JSONak + errubrika + prompt | Ebaluazio-JSONak |
| **4. EMAITZAK** | Python scripta | Ebaluazio-JSONak + ikasle-zerrenda | XLSX (notas + feedback por examen) |
| **5. KOADERNOA** | XLSX + Python scripta | Azterketa guztien emaitzak | Nota finala, ebaluazio-txostena |

---

## 2. EBALUAZIO-SISTEMA: ERRUBRIKA (Rúbrica)

### 2.1. Oinarria / Base teórica

- **Marco**: MCER/ERRM (Marco Común Europeo de Referencia para las Lenguas)
- **Maila**: B1 (nivel esperable para DBH 3-4)
- **Mota**: Rúbrica analítica (puntuación independiente por criterio)
- **Eskala**: 0-10, con traducción a niveles Heziberri

### 2.2. Lau irizpideak / Los cuatro criterios

Basados en las escalas cualitativas del MCER para producción escrita B1:

| # | Irizpidea | Zer ebaluatzen du | Pisua |
|---|-----------|-------------------|-------|
| 1 | **ATAZAREN BETETZEA** (Task Achievement) | Contenido, adecuación al tipo de texto, desarrollo de ideas, cumplimiento del enunciado | 25% |
| 2 | **ANTOLAKETA ETA KOHERENTZIA** (Organisation & Coherence) | Estructura del texto, párrafos, conectores, cohesión, formato del tipo textual | 25% |
| 3 | **BALIABIDE LINGUISTIKOEN HEDADURA** (Range) | Riqueza de vocabulario, variedad de estructuras, registro, capacidad expresiva | 25% |
| 4 | **ZUZENTASUNA** (Accuracy) | Corrección gramatical, léxica, ortográfica; interferencias del castellano (erderakadak) | 25% |

### 2.3. Bost lorpen-maila / Cinco niveles de logro

| Nota 0-10 | Maila | Heziberri baliokidetza |
|-----------|-------|------------------------|
| 9-10 | **Bikaintasuna** | Excelencia |
| 7-8 | **Aurreratua** | Maila aurreratua |
| 5-6 | **Tartekoa** | Tarteko maila |
| 3-4 | **Hasiberria** | Hasierako maila |
| 0-2 | **Lortu gabea** | Lortu gabea |

### 2.4. Deskribatzaileak / Descriptores detallados

#### IRIZPIDEA 1: ATAZAREN BETETZEA (25%)

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Eskatutako gai guztiak lantzen ditu eta sakonki garatzen ditu. Ideia originalak eta adibide zehatzak ematen ditu. Testu-motaren eskakizunak guztiz betetzen ditu (luzera, helburua, hartzailea). |
| 7-8 | Aurreratua | Eskatutako gai guztiak lantzen ditu eta nahiko ondo garatzen ditu. Adibideak edo xehetasunak ematen ditu gehienetan. Testu-motaren eskakizunak ia guztiz betetzen ditu. |
| 5-6 | Tartekoa | Eskatutako gaien gehienak lantzen ditu, baina batzuk gutxi garatuta daude. Xehetasun edo adibide batzuk ematen ditu. Testu-motaren oinarrizko eskakizunak betetzen ditu. |
| 3-4 | Hasiberria | Eskatutako gaien gutxi batzuk bakarrik lantzen ditu, eta ia garatu gabe. Ia ez du adibiderik ematen. Testu-motaren eskakizunak partzialki betetzen ditu. |
| 0-2 | Lortu gabea | Ez du ataza betetzen edo gaiarengandik guztiz urruntzen da. Ez du testu-motaren eskakizunik betetzen. Testua laburregia da ebaluatzeko. |

#### IRIZPIDEA 2: ANTOLAKETA ETA KOHERENTZIA (25%)

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Testuak egitura argia eta eraginkorra du (sarrera, garapena, ondorioa). Paragrafoak ondo bereizita daude eta ideia bakoitza koherenteki garatzen du. Lotura-hitz ugari eta egokiak erabiltzen ditu (hala ere, gainera, horregatik, bestalde...). Testu-motaren formatua guztiz errespetatzen du. |
| 7-8 | Aurreratua | Testuak egitura argia du. Paragrafoak ongi antolatuta daude. Lotura-hitz nahikoak eta egokiak erabiltzen ditu. Formatua ia guztiz errespetatzen du. |
| 5-6 | Tartekoa | Testuak oinarrizko egitura du, baina garapena linealegia izan daiteke. Paragraforik erabiltzen du, baina banaketa ez da beti egokia. Oinarrizko lotura-hitzak erabiltzen ditu (eta, baina, beraz). Formatua gehienetan errespetatzen du. |
| 3-4 | Hasiberria | Testuak egitura ahula du; ideiak nahasita edo ordenatu gabe agertzen dira. Paragrafoen banaketa eskasa edo existitzen ez dena. Lotura-hitz gutxi edo desegokiak. Formatuari ia ez dio jaramonik egiten. |
| 0-2 | Lortu gabea | Ez du egitura antzematekorik. Ideiak deskonektatuta agertzen dira. Ez du lotura-hitzik erabiltzen. Formatua guztiz baztertzen du. |

#### IRIZPIDEA 3: BALIABIDE LINGUISTIKOEN HEDADURA (25%)

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Hitz-altxor aberatsa eta zehatza erabiltzen du; sinonimoak eta esamolde desberdinak tartekatzen ditu errepikapena saihestuz. Perpaus-egitura ugariak erabiltzen ditu (perpaus nagusiak, mendekoak, erlatibozkoak). Erregistroa testu-motara guztiz egokitzen du. Ez du formulazio-zailtasunik hiztegia falta delako. |
| 7-8 | Aurreratua | Hitz-altxor nahikoa eta egokia erabiltzen du. Batzuetan sinonimoak edo birformulazioak erabiltzen ditu. Perpaus-egitura desberdinak erabiltzen ditu. Erregistroa gehienetan egokia da. Noizean behin formulazio-zailtasunen bat izan dezake. |
| 5-6 | Tartekoa | Oinarrizko hitz-altxorra erabiltzen du, nahikoa ataza betetzeko. Hitz batzuk errepikatzen ditu alternatiba falta delako. Perpaus sinpleak nagusi dira, baina noizean behin konplexuagoak ere erabiltzen ditu. Erregistroa gehienetan egokia bada ere, aldaketak egon daitezke. |
| 3-4 | Hasiberria | Hitz-altxor mugatua du; errepikapen ugari eta zirkumlokuzioak. Perpaus sinple eta laburrak nagusi dira ia beti. Erregistroa ez da egokia edo aldakorra da. Hiztegiaren mugek komunikazioa zailtzen dute batzuetan. |
| 0-2 | Lortu gabea | Oinarrizko hitzak bakarrik erabiltzen ditu. Hitz-altxorraren urritasunak komunikazioa eragozten du. Perpaus-egitura minimoena. |

#### IRIZPIDEA 4: ZUZENTASUNA (25%)

| Nota | Maila | Deskribatzailea |
|------|-------|-----------------|
| 9-10 | Bikaintasuna | Oinarrizko gramatika-egiturak eta ohiko egiturak oso ondo menperatzen ditu. Akats gutxi, eta horiek ez dute komunikazioa kaltetzen. Ortografia eta puntuazioa zuzenak dira. Ia ez du ama-hizkuntzaren interferentziarik (erderakadarik). |
| 7-8 | Aurreratua | Oinarrizko gramatika ondo kontrolatzen du. Akats batzuk egiten ditu, baina komunikazioa ia ez dute kaltetzen. Ortografia eta puntuazioa nahiko zuzenak dira. Noizean behineko interferentziak ama-hizkuntzatik. |
| 5-6 | Tartekoa | Ohiko egiturak nahiko ondo erabiltzen ditu, baina gai konplexuagoetan akats nabarmenak egiten ditu. Akatsak ez dute komunikazioa guztiz eragozten, baina batzuetan zailtzen dute. Ortografian akats batzuk. Ama-hizkuntzaren eragin partziala (erderakada batzuk). |
| 3-4 | Hasiberria | Oinarrizko egituretan ere akats ugariak egiten ditu. Akatsek komunikazioa maiz zailtzen dute. Ortografia eta puntuazio eskasak. Ama-hizkuntzaren eragin nabarmena (erderakada ugari: kalkoak, gaztelaniazko hitz-ordena...). |
| 0-2 | Lortu gabea | Akats sistematikoak oinarrizko egituretan. Testua ia ulertezina da akats kopuruagatik. Ortografia oso eskasa. Interferentzia sistematikoak beste hizkuntzetatik. |

### 2.5. Erderakadak / Interferencias del castellano

Las erderakadak no son un criterio separado. Se evalúan dentro de **ZUZENTASUNA** como sub-indicador progresivo, alineado con el descriptor B1 del MCER que menciona explícitamente la "influencia notable de la lengua materna". Sin embargo, en el **feedback** al alumno, las erderakadak se señalan como categoría específica de comentario para que el alumno las identifique y corrija.

### 2.6. DBH 3 vs DBH 4

Los descriptores son idénticos. Lo que cambia es la **expectativa de nivel**:
- **DBH 3**: Un 5-6 (tartekoa) es el rendimiento esperable
- **DBH 4**: Se espera un 7-8 (aurreratua) como rendimiento adecuado

Esto se gestiona en el prompt de la IA, no en la rúbrica.

---

## 3. IKASLEEN KODEAK / Sistema de códigos de alumno

Cada alumno tiene un código único que usa para identificarse en los exámenes. Formato:

```
[MAILA][TALDEA][ZENBAKIA]
Ejemplo: 3A017 → DBH3, A taldea, 17. ikaslea
```

Ventajas:
- **Pribatutasuna**: la IA corrige códigos, no nombres. Los nombres se resuelven solo en el xlsx final.
- **Akatsen prebentzioa**: datos precargados, no escritos por el alumno.
- **Iragazketa**: permite agrupar y filtrar resultados por taldea, maila, ikasturtea.

Almacenado en un fichero maestro:

```json
{
  "3A017": {
    "izena": "Ane",
    "abizena": "Etxeberria",
    "taldea": "3A",
    "maila": "DBH3"
  }
}
```

---

## 4. ATAZA-FITXA / Ficha de tarea

El egitekoa es tan importante como la rúbrica. Cada examen genera una ficha de tarea con estos campos:

| Eremua | Deskribapena | Adibidea |
|--------|-------------|----------|
| **Egitekoa** | Enunciado literal que recibe el alumno | "Idatzi iritzi-artikulu bat mugikorren erabilerari buruz ikasgelan..." |
| **Testu mota** | Tipología textual | Iritzi-artikulua / deskribapena / gutun formala / hausnarketa / gidoia / aurkezpena |
| **Maila** | Nivel educativo | DBH 3 / DBH 4 |
| **Hitz kopurua** | Extensión esperada (mín-máx) | 150-250 hitz |
| **Erregistroa** | Registro esperado | Formala (zuka) / informala / neutrala |
| **Eduki espezifikoak** | Contenidos obligatorios | "Gutxienez 2 argudio alde eta 1 kontra" |
| **Ebaluazio-oharrak** | Notas del profesor para la IA | "Gaiari buruzko debatea egin dugu klasean" |

---

## 5. DATU-FLUXUA / Flujo de datos

### 5.1. JSON de entrega del alumno (output del HTML)

```json
{
  "meta": {
    "bertsioa": "1.0",
    "data": "2026-02-08T10:32:15",
    "kodea": "3A017",
    "maila": "DBH3",
    "taldea": "3A"
  },
  "ataza": {
    "izenburua": "Iritzi-artikulua: mugikorrak ikasgelan",
    "egitekoa": "Idatzi iritzi-artikulu bat...",
    "testu_mota": "iritzi-artikulua",
    "erregistroa": "formala",
    "hitz_min": 150,
    "hitz_max": 250,
    "eduki_espezifikoak": ["Gutxienez 2 argudio alde", "Gutxienez 1 argudio kontra", "Ondorio argia"],
    "ebaluazio_oharrak": "Gaiari buruzko debatea egin dugu klasean"
  },
  "erantzuna": {
    "testua": "Gaur egun, mugikorrak gure bizitzaren parte dira...",
    "hitz_kopurua": 187,
    "denbora_minutuak": 38
  },
  "segurtasuna": {
    "itsatsi_kopurua": 0,
    "itsatsi_hitz_kopurua": 0,
    "leiho_aldaketak": 2,
    "idazketa_patroia": "normala",
    "denbora_inaktibo_segunduak": 45
  }
}
```

### 5.2. JSON de evaluación de la IA (output del corrector)

```json
{
  "kodea": "3A017",
  "ebaluazioa": {
    "atazaren_betetzea": {
      "nota": 7,
      "maila": "aurreratua",
      "iruzkina": "Eskatutako gai guztiak lantzen ditu..."
    },
    "antolaketa_koherentzia": {
      "nota": 6,
      "maila": "tartekoa",
      "iruzkina": "Sarrera, garapena eta ondorioa bereizten ditu..."
    },
    "hedadura": {
      "nota": 6,
      "maila": "tartekoa",
      "iruzkina": "Oinarrizko hiztegia egokia da gairako..."
    },
    "zuzentasuna": {
      "nota": 5,
      "maila": "tartekoa",
      "iruzkina": "NOR-NORK nahasketa 3 aldiz..."
    }
  },
  "laburpena": {
    "batez_bestekoa": 6.0,
    "heziberri_maila": "tartekoa",
    "orokorra": "Iritzi-artikuluaren oinarrizko eskakizunak betetzen dituzu..."
  },
  "segurtasun_azterketa": {
    "susmagarria": false,
    "oharrak": ""
  }
}
```

### 5.3. Prompt de la IA (estructura)

```
SISTEMA (fijo, siempre igual):
├── Rol: Euskal Hizkuntza eta Literaturako irakasle aditua
├── Ebaluazio-sistema: ERRM B1 mailako irizpideak
└── Output formatua: JSON egitura zehatza

ERRUBRIKA (fija):
├── 1. Atazaren betetzea [5 maila × deskribatzaileak]
├── 2. Antolaketa eta koherentzia [5 maila × deskribatzaileak]
├── 3. Baliabide linguistikoen hedadura [5 maila × deskribatzaileak]
└── 4. Zuzentasuna [5 maila × deskribatzaileak]

ATAZA-FITXA (variable por examen):
├── Egitekoa, testu mota, maila, erregistroa...
└── Eduki espezifikoak, ebaluazio-oharrak

AINGURA-TESTUAK (opcional, calibración):
├── Adibidea: 8/10 nota → [testua + ebaluazioa]
└── Adibidea: 5/10 nota → [testua + ebaluazioa]

IKASLEAREN TESTUA (variable por alumno):
└── [Testua]
```

Los **aingura-testuak** (textos ancla) son opcionales pero muy recomendables: 2-3 textos corregidos a mano por el profesor que calibran el criterio de la IA. Multiplican la precisión de la corrección.

---

## 6. SEGURTASUNA / Anti-copia

Filosofía: **registrar, no bloquear**. El HTML captura eventos sospechosos y los incluye en el JSON de entrega. El profesor decide qué hacer con esa información.

| Neurria | Zer erregistratzen du |
|---------|-----------------------|
| **Itsatsi detekzioa** (Paste detection) | Ctrl+V eventos: cuántas veces, cuánto texto pegado |
| **Leiho aldaketak** (Tab switching) | Cuántas veces sale de la pestaña del examen y por cuánto tiempo |
| **Idazketa patroia** (Writing pattern) | Si el texto aparece de golpe (vs. escritura progresiva normal) |
| **Denbora inaktiboa** (Inactive time) | Tiempo sin escribir (puede indicar que está en otra ventana) |
| **IA detekzioa** (por el corrector) | Si un alumno de nivel bajo entrega texto de nivel alto, flag automático |

Además: **disuasión psicológica**. Al entrar en el examen, aviso visible: "Zure jarduera guztia erregistratzen da."

---

## 7. KOADERNO DIGITALA / Cuaderno de notas global

### 7.1. Kontzeptua

Un XLSX maestro que acumula las notas de TODOS los exámenes y pruebas del curso. Cada vez que se corrige un examen nuevo, los resultados se vuelcan automáticamente (o manualmente) en este cuaderno. Al final de la evaluación, calcula la nota final ponderada.

### 7.2. Egitura / Estructura

**Pestaña por evaluación (1. ebaluazioa, 2. ebaluazioa, 3. ebaluazioa):**

| Kodea | Izena | 1. azterketa (iritzi-art.) | 2. azterketa (gutuna) | 3. azterketa (deskrib.) | ... | Ebaluazio nota |
|-------|-------|------|------|------|-----|---------|
| 3A017 | Ane Etxeberria | 6.0 | 7.5 | 5.5 | ... | 6.3 |
| 3A018 | Mikel Aguirre | 4.5 | 5.0 | 6.0 | ... | 5.2 |

**Pestaña resumen global (Laburpena):**

| Kodea | Izena | 1. ebaluazioa | 2. ebaluazioa | 3. ebaluazioa | Azken nota |
|-------|-------|-------|-------|-------|------|
| 3A017 | Ane Etxeberria | 6.3 | 7.1 | ... | ... |

**Pestaña de detalle por examen (opcional):**

Desglose por criterio (Atazaren betetzea, Antolaketa, Hedadura, Zuzentasuna) + feedback completo para cada alumno en cada examen. Útil para tutorías y reuniones con familias.

### 7.3. Funtzionalitate osagarriak / Funcionalidades extra

- **Ponderación configurable**: cada examen puede tener un peso diferente en la nota de evaluación
- **Estadísticas por criterio**: media del grupo en cada criterio → detectar carencias colectivas
- **Evolución individual**: gráfico de progresión de cada alumno a lo largo del curso
- **Alertas**: flag automático para alumnos cuya nota cae por debajo de un umbral

---

## 8. GITHUB REPO EGITURA / Estructura del repositorio

```
zuzendu/
├── README.md
├── LICENSE
│
├── config/                         ← KONFIGURAZIOA (una vez)
│   ├── errubrika.json              ← rúbrica MCER B1 completa
│   ├── sistema_prompt.txt          ← prompt fijo para la IA correctora
│   └── ikasleak/                   ← listas de alumnos
│       ├── 2025-26_DBH3A.json
│       ├── 2025-26_DBH3B.json
│       └── 2025-26_DBH4A.json
│
├── sortzailea/                     ← DISEÑADOR DE EXÁMENES
│   ├── sortzailea.html             ← interfaz del profesor (+ IA para generar egitekoak)
│   └── txantiloiak/                ← plantillas de tipos de texto
│       ├── iritzi_artikulua.json
│       ├── gutun_formala.json
│       ├── gutun_informala.json
│       ├── deskribapena.json
│       ├── hausnarketa.json
│       ├── aurkezpena.json
│       └── gidoia.json
│
├── azterketak/                     ← EXÁMENES GENERADOS
│   ├── 2026-02-10_iritzi/          ← carpeta por examen
│   │   ├── azterketa.html          ← HTML que abren los alumnos
│   │   ├── ataza_config.json       ← configuración de la tarea
│   │   └── entregas/               ← JSON de entregas
│   │       ├── 3A017.json
│   │       └── ...
│   └── ...
│
├── zuzentzailea/                   ← CORRECTOR
│   ├── zuzendu.py                  ← script principal (batch processing)
│   ├── requirements.txt
│   └── aingurak/                   ← textos ancla de calibración (opcional)
│       └── iritzi_artikulua/
│           ├── maila_8.json
│           └── maila_5.json
│
├── emaitzak/                       ← RESULTADOS POR EXAMEN
│   └── 2026-02-10_iritzi/
│       ├── emaitzak.xlsx
│       └── ebaluazio_jsonak/
│           ├── 3A017_eb.json
│           └── ...
│
└── koadernoa/                      ← CUADERNO DIGITAL GLOBAL
    ├── koadernoa.xlsx              ← cuaderno maestro con todas las notas
    ├── eguneratu.py                ← script para volcar resultados al cuaderno
    └── txostenak/                  ← informes generados
        ├── 3A_txostena.xlsx        ← informe por grupo
        └── banakakoak/             ← informes individuales (para familias)
```

---

## 9. ONLINE / OFFLINE

### Proposamena: sistema hibridoa

- **AZTERKETA (examen)**: funciona offline (JavaScript puro, sin dependencias externas). Si cae el WiFi, el examen no se interrumpe.
- **ENTREGA**: si hay WiFi → el JSON se envía a un servidor local (el portátil del profesor con un servidor Python básico). Si no hay WiFi → el alumno descarga el JSON y lo entrega manualmente.
- **ZUZENTZAILEA (corrección)**: requiere conexión (necesita la API de Claude). Se ejecuta desde el ordenador del profesor.
- **VENTAJA offline para anti-copia**: sin WiFi, los alumnos no pueden acceder a ChatGPT ni a Google. Es la medida anti-copia más efectiva.

---

## 10. POSIBLES AMPLIACIONES / Jarduerak eta integrazioak

El modelo ZUZENDU (diseñar → examinar → corregir → informar) puede extenderse a otras actividades evaluables con escritura:

### 10.1. Integración directa (misma rúbrica, mismo flujo)

| Jarduera | Nola integratzen da |
|----------|---------------------|
| **Idazlan libreak** (redacciones libres) | Mismo flujo exacto. Solo cambia la ataza-fitxa. |
| **Laburpenak** (resúmenes) | Mismo flujo. Se añade el texto fuente al JSON para que la IA verifique fidelidad al original. |
| **Irakurketa-txostenak** (informes de lectura) | Mismo flujo. El egitekoa especifica el libro/texto leído. |
| **Egunkariak / Blogak** (diarios/blogs) | Evaluación periódica de entradas. Se acumulan en el koadernoa como notas parciales. |
| **Azterketak galdera irekiekin** (exámenes con preguntas abiertas) | El HTML presenta múltiples preguntas. Cada una genera su propio bloque en el JSON. La IA corrige pregunta por pregunta. |

### 10.2. Integración con adaptación (misma infraestructura, rúbrica diferente)

| Jarduera | Zer aldatzen da |
|----------|-----------------|
| **Ahozko aurkezpenak** (presentaciones orales) | Rúbrica diferente (añade criterios de pronunciación, fluidez, lenguaje no verbal). Input: transcripción o audio. La IA puede evaluar transcripciones. |
| **Eztabaidak** (debates) | Rúbrica con criterios argumentativos. Input: transcripción del debate o notas del profesor. |
| **Talde-lanak** (trabajos en grupo) | Mismo flujo pero con evaluación individual + grupal. Se puede añadir co-evaluación entre alumnos. |

### 10.3. Herramientas complementarias que podrían integrarse

| Tresna | Helburua |
|--------|----------|
| **Autoebaluazio-errubrika ikaslearentzat** | HTML donde el alumno se autoevalúa con la misma rúbrica ANTES de entregar. Fomenta la reflexión metacognitiva. Se registra en el JSON y la IA puede comparar la autoevaluación con su evaluación. |
| **Koebaluazioa** (evaluación entre pares) | Los alumnos evalúan el texto de un compañero (anonimizado por código) usando una versión simplificada de la rúbrica. Genera datos interesantes sobre percepción de calidad. |
| **Akats-bankua** (banco de errores) | La IA acumula los errores más frecuentes de cada alumno a lo largo del curso. Genera ejercicios personalizados de refuerzo. |
| **Hitz-altxor pertsonala** (vocabulario personal) | La IA detecta el vocabulario que cada alumno usa (y no usa) y sugiere léxico nuevo personalizado. |
| **Bilakaera-txostena** (informe de evolución) | Al final del curso, informe automático por alumno mostrando progresión en cada criterio, errores recurrentes superados, y áreas de mejora pendientes. Útil para reuniones con familias. |

### 10.4. Integración con el diseñador de exámenes existente

El **sortzailea** (diseñador) puede integrar el generador de exámenes por IA que ya existe:
- La IA genera egitekoak adaptados al tema, nivel y tipología textual
- El profesor revisa, ajusta y aprueba
- El sortzailea genera el HTML del examen con todo embebido
- Flujo: IA propone → profesor valida → HTML generado → alumnos escriben → IA corrige

---

## 11. HURRENGO PAUSOAK / Próximos pasos

### Lehentasun handikoak (prioridad alta)
1. **Errubrika findu**: Revisar los descriptores con casos reales de alumnos
2. **HTML azterketa prototipoa**: Construir el examen funcional con contador de palabras, códigos de alumno y registro de seguridad
3. **zuzendu.py**: Script de corrección que lea JSONs y llame a la API de Claude
4. **Prompt optimizazioa**: Iterar el prompt con textos reales hasta que la IA clave las notas

### Lehentasun ertaina (prioridad media)
5. **Sortzailea**: Integrar el diseñador de exámenes existente
6. **Koadernoa**: Crear el cuaderno digital con volcado automático
7. **Aingura-testuak**: Corregir 2-3 textos a mano como calibración

### Lehentasun baxua (prioridad baja, pero de alto impacto)
8. **Autoebaluazioa**: HTML para que los alumnos se autoevalúen
9. **Akats-bankua**: Sistema de errores acumulados por alumno
10. **Bilakaera-txostena**: Informes de evolución automáticos

---

## 12. PRINTZIPIO GIDATZAILEAK / Principios de diseño

1. **Irakaslearen irizpidea nagusi**: La IA aplica TU criterio, no el suyo. La rúbrica y los textos ancla definen el estándar.
2. **Erdi-automatikoa**: La IA propone, el profesor dispone. Siempre hay un punto de revisión humana.
3. **Estandar irekietan oinarritua**: MCER B1 como base, Heziberri como traducción institucional. Defendible ante inspección.
4. **Sinplea eta erabilgarria**: Si es más trabajo que corregir a mano, ha fallado. Tiene que ahorrar tiempo REAL.
5. **Pribatutasuna**: Los datos de alumnos nunca salen del control del profesor. La IA recibe códigos, no nombres.
6. **Offline-first**: El examen funciona sin internet. La corrección requiere conexión, pero es asíncrona.

---

*Dokumentu hau diseinuaren laburpena da. ZUZENDU proiektuaren hasierako fasea. 2026-02-08.*
