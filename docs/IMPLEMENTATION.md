# ZUZENDU v3 — Plan de implementación

## Visión general

El proyecto se implementa en 4 fases incrementales. Cada fase produce algo funcional: a partir de la Fase 1.3 ya se pueden corregir textos. Las fases posteriores añaden interfaz, automatización, detección IA avanzada y reporting.

---

## Fase 0: Scaffold — COMPLETADA

| Tarea | Fichero | Estado |
|-------|---------|--------|
| Crear estructura de carpetas | `config/`, `src/`, `tests/`, etc. | ✅ |
| README + documentación base | `README.md`, `docs/` | ✅ |
| Configuración del entorno | `.env.example`, `requirements.txt`, `.gitignore` | ✅ |

---

## Fase 1: Motor de corrección — COMPLETADA

### 1.1. Rúbrica en JSON — ✅
**Fichero:** `config/errubrika.json`

### 1.2. Prompt de sistema — ✅
**Fichero:** `config/sistema_prompt.txt`

### 1.3. Script de test mínimo — ✅
**Fichero:** `src/zuzendu_test.py` + `src/zuzendu.py` (pipeline batch)

### 1.4. Calibración — ✅
- KAL-001 a KAL-004: 95% celdas ≤1 punto
- 6 parches aplicados al prompt
- EP100 post-procesado en Python (`src/ep100.py`)
- Validación académica (Uria 2009, Arrieta 2010, Maritxalar 1999)

### 1.5. IA Detección v1 — ✅
**Fichero:** `src/ia_detekzioa.py`
- API call separada, antes de evaluación
- S1-S7 (perfección, vocabulario, estructura, tono, longitud, patrones, uniformidad)
- Umbrales: BAXUA (0-7), ERTAINA (8-13), ALTUA (14-21)
- Bug corregido: Python calcula suma S1-S7, no confía en el modelo

### 1.6. Organización por grupos — ✅
- Estructura `idazlanak/[TALDEA]/[AKTIBITATEA]/`
- Resultados en `emaitzak/[TALDEA]/[AKTIBITATEA]/`
- Pipeline automático: `python src/zuzendu.py "idazlanak/DBH4B/..." --mota narrazioa`

---

## Fase 2: Interfaz de escritura + IA detección avanzada

> **Principio rector (deep research, 2026-02-09):**
> No se detecta "IA sí/no", sino la probabilidad de desajuste entre el texto y el trabajo cognitivo esperable del alumno. La detección puramente automática del texto es vulnerable y no debe ser la base de decisiones. Lo que funciona es la **triangulación**: texto + proceso + contexto + resistencia.

### 2.1. HTML idazketa-tresna (interfaz del alumno)

**Fichero:** `templates/idazketa.html`

HTML autocontenido donde el alumno escribe sus textos. Funcionalidades:

**Básicas:**
- Textarea con contador de palabras en tiempo real
- Enunciado del ejercicio visible
- Identificación con email del centro
- Botón "Entregatu" → genera fichero con texto + metadatos

**Guardado entre sesiones (clave):**
- Autoguardado en localStorage cada 10 segundos (mensaje "Gordeta ✓")
- Si cambian de dispositivo: botón "📋 Kopiatu kodea" / "📥 Jarraitu hemen"
- Al entregar: descarga fichero .zuzendu (JSON con texto + metadatos)

**Captura de metadatos (Dominio 1 — Proceso/procedencia):**
- Tiempo total de escritura por sesión
- Número de sesiones con timestamps
- Eventos de pegar (paste): cuántos, cuántas palabras, contenido
- Ritmo de escritura: velocidad entre teclas, variabilidad
- Borrados: frecuencia y patrones
- Pausas de pensamiento (>5 segundos)
- Palabras al inicio vs al final de cada sesión (crecimiento progresivo)

Estos metadatos se guardan en un JSON oculto dentro del fichero .zuzendu:
```json
{
  "testua": "Bart eta bere lagunak...",
  "sesioak": [
    {"data": "2026-02-10 17:30", "iraupena_min": 25, "hitz_hasiera": 0, "hitz_amaiera": 180, "paste_events": 0, "borratuak": 45},
    {"data": "2026-02-10 21:15", "iraupena_min": 40, "hitz_hasiera": 180, "hitz_amaiera": 450, "paste_events": 0, "borratuak": 78}
  ],
  "paste_log": [],
  "tekleo_erritmoa": {"batez_bestekoa_ms": 180, "desbideratzea": 85}
}
```

### 2.2. IA detekzio v2 — 5 domeinu sistema

**Base teórica:** Deep research (2026-02-09) — triangulación de evidencia heterogénea.

**Fichero:** `src/ia_detekzioa_v2.py`

5 dominios con evidencia acumulada:

#### Dominio 1: Proceso/procedencia (metadatuak)
**Fuente de datos:** HTML idazketa-tresna (fichero .zuzendu)
- Tiempo de escritura vs longitud del texto (3 min para 800 palabras = sospechoso)
- Eventos de pegar (un paste de 500 palabras = copiado)
- Ritmo irregular (natural) vs constante (copiado tecleando)
- Borrados frecuentes (natural) vs casi ninguno (pegado)
- Sesiones múltiples (natural) vs sesión única muy corta (sospechoso)

#### Dominio 2: Consistencia textual intra-documento
**Fuente de datos:** Texto del alumno (API call)
- Cambios de estilo dentro del texto (segmentos con densidad léxica diferente)
- Registro que fluctúa (normal en alumno) vs estable (IA)
- Calidad uniforme hasieratik bukaeraraino (IA) vs degradación por cansancio (natural)

#### Dominio 3: Perfil longitudinal del alumno
**Fuente de datos:** Correcciones anteriores almacenadas
- Comparar errores típicos: si siempre confunde s/z y ahora no → sospechoso
- Comparar nivel de vocabulario, longitud de frases, complejidad sintáctica
- Salto brusco de notas sin explicación (4,5,4 → 9 = sospechoso)
- A partir del 3er texto: línea base fiable

**Implementación:** `src/ikasle_profila.py`
- Almacenar perfil por alumno tras cada corrección
- Errores frecuentes, vocabulario medio, longitud de frases, nota media
- Comparar texto nuevo vs perfil acumulado

#### Dominio 4: Cognitivo-didáctico
**Fuente de datos:** Texto del alumno (API call)
- ¿Hay errores plausibles para su nivel? (la IA no comete errores de ikasle)
- ¿Hay anclaje al aula? (referencias a clase, experiencias personales)
- ¿Responde a la tarea o a su comprensión de la tarea? (IA = perfecto, alumno = parcial)
- Incongruencia cognitiva: conclusiones sin proceso previo visible

#### Dominio 5: Pruebas de resistencia (minidefensa)
**Fuente de datos:** Generadas automáticamente por ZUZENDU
- 6-10 preguntas personalizadas sobre el texto del alumno
- "Zergatik aukeratu zenuen hitz hau?"
- "Azaldu 3. paragrafoan zer esan nahi zenuen"
- "Zein iturri erabili zenuen ideia hau lortzeko?"
- Se aplican a TODOS los textos (parte normal del proceso, no solo sospechosos)
- El profesor las usa en clase para minidefensa oral (5-10 min)

**Output v2:**
```json
{
  "domeinuak": {
    "prozesua": {"ebidentzia": "...", "probabilitatea": "baxua/ertaina/altua"},
    "koherentzia_testual": {"ebidentzia": "...", "probabilitatea": "..."},
    "profil_longitudinala": {"ebidentzia": "...", "probabilitatea": "..."},
    "kognitibo_didaktikoa": {"ebidentzia": "...", "probabilitatea": "..."},
    "erresistentzia": {"galderak": ["...", "..."], "oharrak": "..."}
  },
  "estimazio_orokorra": "baxua/ertaina/altua",
  "faltsu_positiboen_arriskuak": ["..."],
  "irakaslearentzako_gomendioa": "..."
}
```

### 2.3. Erreferentzia-paragrafoa (klase-barnean)

**Kontzeptua:** Ikasleek klase-barnean (zuen aurrean, gailurik gabe) paragrafo bat idazten dute gai jakin bati buruz. Paragrafo hau erreferentzia gisa gordetzen da.

**Helburua:** Errore-patroi pertsonalak identifikatu (sibilanteak, ergatiboa, kasu-markak...) eta etxean idatzitako testuekin alderatu.

**Galdera-mota egokia:** "Kontatu labur zer egin zenuten atzo goizean, norekin egon zineten, eta zergatik gustatu zitzaizuen edo ez." → Obliga: pasado, ergativo, dativo, kausal... dena paragrafo natural batean.

**Gordetzea:** `data/profilak/[TALDEA]/[IKASLEA]/erreferentzia.txt`

### 2.4. Prompt garbiketa

**Fichero:** `config/sistema_prompt.txt`

- **Kendu** "0. IA DETEKZIOA" atala → modeloak ignoratzen zuen eta orain `ia_detekzioa.py`-n dago
- **Berrikusi** ebaluazio-promptaren egitura: deep research-ek esaten du ebidentzia kognitibo-didaktikoa (ikaslearen pentsamendu-prozesua, klaserekiko lotura) ere ebaluazioan kontuan hartu behar dela, ez bakarrik IA detekzioan
- **Gehitu** minidefentsa galderak sortzeko argibidea: modeloak ebaluazioarekin batera 3-5 galdera pertsonalizatu proposatu behar ditu irakaslearentzat

### 2.5. Procesamiento batch mejorado

**Fichero:** `src/zuzendu.py` (ya existe, ampliar)
- Integrar .zuzendu ficheros (HTML-tik) además de .docx/.txt
- Metadatos de escritura automáticamente incorporados a IA detekzioa v2
- Gestión de rate limits y reintentos

---

## Fase 3: Reporting

### 3.1. Generador de Excel
**Fichero:** `src/emaitzak_xlsx.py`
- Hoja de notas (alumno, nota por criterio, nota final, nivel Heziberri)
- Hoja de feedback (feedback completo por alumno)
- Hoja de errores (errores agrupados por tipo y frecuencia)

### 3.2. Cuaderno digital
**Fichero:** `src/koadernoa.py`
- Una fila por alumno, una columna por evaluación
- Medias por criterio a lo largo del tiempo
- Evolución del alumno visible
- Alimenta el perfil longitudinal (Dominio 3)

---

## Fase 4: Herramientas del profesor

### 4.1. Generador de ejercicios
**Fichero:** `templates/sortzailea.html`
- Tipo de texto, nivel, enunciado, requisitos, rango de palabras
- Genera el HTML de escritura automáticamente

### 4.2. Ciclo borrador-reescritura
- Primera entrega → feedback formativo (más suave, feed-forward)
- Segunda entrega → evaluación completa con nota final
- Comparación entre versiones ("5 → 7 koherentzian!")

---

## Prioridades

```
COMPLETADO    Fase 0 + 1             →  Motor funcional + IA detekzioa v1
EN CURSO      Fase 1 (taldeak)       →  Prozesatu 4A, 3A, 3B
PRIORITARIO   Fase 2.1 + 2.2 + 2.4   →  HTML tresna + IA detekzioa v2 + prompt garbiketa
ÚTIL          Fase 2.3 + 2.5         →  Erreferentzia + batch hobetua
MEJORA        Fase 3 + 4             →  Reporting + herramientas
```

---

## Kostu estimazioa

- Zuzenketa deia: ~$0.10/ikasle (Sonnet, ~4K input + 3K output)
- IA detekzio deia: ~$0.01/ikasle (~2K input, ~200 output)
- Hilean: ~70 ikasle × $0.11 = ~$8/hilean
- Urtean: 9 hile × aktibitate bat/hilean = ~$70/urtean

---

*Erreferentzia osoa: [ZUZENDU_v3_sistema.md](ZUZENDU_v3_sistema.md)*
*Deep research IA detekzioa: [docs/referencias/ia_detekzioa_deep_research.md](docs/referencias/ia_detekzioa_deep_research.md)*
