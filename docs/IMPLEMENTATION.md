# ZUZENDU v3 — Plan de implementación

## Visión general

El proyecto se implementa en 4 fases incrementales. Cada fase produce algo funcional: a partir de la Fase 1.3 ya se pueden corregir textos (aunque sea con copiar-pegar). Las fases posteriores añaden interfaz, automatización y comodidad.

---

## Fase 0: Scaffold (esta fase)

| Tarea | Fichero | Estado |
|-------|---------|--------|
| Crear estructura de carpetas | `config/`, `src/`, `tests/`, etc. | Hecho |
| README + documentación base | `README.md`, `docs/` | Hecho |
| Configuración del entorno | `.env.example`, `requirements.txt`, `.gitignore` | Hecho |

---

## Fase 1: Motor de corrección

### 1.1. Rúbrica en JSON — COMPLETADA

**Fichero:** `config/errubrika.json`

Traducir la especificación de `ZUZENDU_v3_sistema.md` (secciones 2-5) a un JSON estructurado:
- 4 criterios con descriptores por banda (0-2, 3-4, 5-6, 7-8, 9-10)
- Caps (CAP-1 a CAP-8) con condiciones y notas máximas
- Penalizaciones (PEN-1 a PEN-7) con valores y acumulación máxima
- Bonificaciones (BON-1 a BON-4)
- Bandas EP100
- Catálogo de 60 errores tipificados con IDs, severidad y acciones
- Tipologías textuales y niveles de conectores

### 1.2. Prompt de sistema — COMPLETADA

**Fichero:** `config/sistema_prompt.txt`

Prompt que recibe el LLM con:
- Rol y enfoque formativo
- Referencia a `errubrika.json` y `config/gramatika/*.tsv` (inyectados en el mensaje)
- Reglas de feedback (positivo primero, feed-forward, no saturar, agrupar errores)
- Protocolo anti-alucinación ("zalantzazkoa") y señales de alerta para el profesor
- Regla de penalización decreciente por repetición
- Formato de salida JSON esperado
- Ejemplo few-shot completo (DBH4-015, 138 hitz, con errores y JSON de salida)
- Idioma del feedback: euskera

### 1.3. Script de test mínimo — COMPLETADA

**Fichero:** `src/zuzendu_test.py`

Script que junta toda la configuración, llama a la API de Anthropic y guarda el JSON:
- System prompt: `config/sistema_prompt.txt`
- User message con XML tags: `<errubrika>` + `<gramatika_fitxategia>` x11 + `<ataza_metadatuak>` + `<ikaslearen_testua>`
- CLI: `--kodea`, `--maila`, `--mota`, `--hitzak`, `--modua`, `--stdin`
- Sin argumentos usa texto few-shot hardcodeado (DBH4-015)
- Salida rich: panel nota, tabla criterios, EP100, akats-taldeak, lehentasuna
- Validación de claves JSON; raw response guardado si falla
- Resultado en `data/emaitzak/{kodea}_{timestamp}.json`

### 1.4. Calibración

**Carpeta:** `tests/testu_kalibrazioa/`

- Corregir 10-20 textos a mano con la rúbrica
- Corregir los mismos con la IA
- Comparar: objetivo ≤1 punto de diferencia en ≥80% de los casos
- Ajustar umbrales EP100, caps y penalizaciones según resultados
- Crear 2-3 textos ancla (uno ~8/10 y otro ~5/10) para calibración permanente

---

## Fase 2: Interfaz de examen + procesamiento batch

### 2.1. Interfaz del alumno

**Fichero:** `templates/azterketa.html`

HTML autocontenido con:
- Enunciado del ejercicio
- Textarea con contador de palabras en tiempo real
- Temporizador (configurable)
- Botón de entrega → genera JSON con metadatos (código alumno, texto, palabras, tiempo)

### 2.2. Capa de seguridad

Detección de comportamiento sospechoso en el HTML:
- Paste detection (pegado desde fuera)
- Tab/alt-tab detection (cambio de ventana)
- Patrones de escritura (velocidad, borrado masivo)
- Registro de eventos en el JSON de salida

### 2.3. Procesamiento batch

**Fichero:** `src/zuzendu.py`

Script principal que:
- Lee todos los JSON de `data/ikasle_testuak/`
- Envía cada texto a la API con la ficha de tarea correspondiente
- Guarda resultados en `data/emaitzak/`
- Gestión de rate limits y reintentos

---

## Fase 3: Reporting

### 3.1. Generador de Excel

**Fichero:** `src/emaitzak_xlsx.py`

Convierte JSON de resultados → XLSX con:
- Hoja de notas (alumno, nota por criterio, nota final, nivel Heziberri)
- Hoja de feedback (feedback completo por alumno)
- Hoja de errores (errores agrupados por tipo y frecuencia)

### 3.2. Cuaderno digital

**Ficheros:** `src/koadernoa.py`

Acumula las notas de todas las evaluaciones en un cuaderno digital XLSX:
- Una fila por alumno, una columna por evaluación
- Medias por criterio a lo largo del tiempo
- Evolución del alumno visible

---

## Fase 4: Herramientas del profesor

### 4.1. Generador de exámenes

**Fichero:** `templates/sortzailea.html`

Interfaz para que el profesor configure:
- Tipo de texto y registro
- Nivel (DBH3/DBH4)
- Enunciado y requisitos
- Rango de palabras
- Genera el HTML de examen automáticamente

### 4.2. Ciclo borrador-reescritura

Integrar en el flujo HTML:
- Primera entrega → feedback formativo (más suave, feed-forward)
- Segunda entrega → evaluación completa con nota final
- Comparación entre versiones ("Has mejorado de 5 a 7 en coherencia")

---

## Prioridades

```
COMPLETADO  Fase 1.1 + 1.2 + 1.3  →  Motor funcional (copiar-pegar)
URGENTE     Fase 1.4               →  Calibración (fiabilidad)
ÚTIL        Fase 2.1 + 2.3        →  Interfaz + batch (eficiencia)
MEJORA      Fase 3 + 4            →  Reporting + herramientas
```

---

*Referencia completa: [ZUZENDU_v3_sistema.md](ZUZENDU_v3_sistema.md)*
