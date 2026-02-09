# ZUZENDU v3

Sistema de corrección automática para escritura en euskera — Euskara eta Literatura (DBH 3-4).

## Zer da?

ZUZENDU es un motor de corrección híbrido (LLM + rúbrica analítica) que evalúa textos escritos por alumnado de DBH 3-4 según el MCER B1 y Heziberri 2020. No es un juez que pone nota: es un corrector formativo que aplica la rúbrica del profesor, señala errores con pedagogía, y orienta al alumno sobre **cómo mejorar**.

### Características principales

- **Rúbrica analítica 4x25%:** Atazaren Betetzea (AB), Antolaketa eta Koherentzia (AK), Baliabide Linguistikoen Hedadura (BLH), Zuzentasun Linguistikoa (ZL)
- **Catálogo de errores tipificados** con severidad (minor/major/critical) y penalización decreciente por repetición
- **EP100 ponderado** para medir densidad de errores normalizada por longitud
- **Feedback formativo en euskera** en 3 capas: resumen, criterio por criterio, y agrupación de errores
- **Ciclo borrador-feedback-reescritura** para maximizar el aprendizaje
- **Gestión de incertidumbre:** marcaje "zalantzazkoa" para evitar falsos positivos
- **Salida JSON estructurada** para integración con Excel y reporting

## Egitura / Estructura

```
zuzendu/
├── config/                  # Configuración del sistema
│   └── gramatika/           # Tablas de gramática euskera (TSV)
├── src/                     # Código fuente
├── tests/                   # Tests y textos de calibración
│   └── testu_kalibrazioa/   # Textos corregidos a mano para calibrar
├── scripts/                 # Scripts auxiliares
├── templates/               # Plantillas HTML (exámenes, generador)
├── data/
│   ├── azterketa_fitxak/    # Fichas de examen (enunciados)
│   ├── ikasle_testuak/      # Textos de alumnos (input)
│   └── emaitzak/            # Resultados de corrección (output)
└── docs/                    # Documentación
    ├── ZUZENDU_v3_sistema.md    # Especificación técnica completa
    ├── IMPLEMENTATION.md        # Plan de implementación por fases
    └── referentzia/             # Documentos de referencia y diseño
```

## Instalación

### Requisitos previos

- Python 3.10+
- Cuenta de API en Anthropic (Claude)

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/goniborja/zuzendu.git
cd zuzendu

# 2. Crear y activar entorno virtual
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Editar .env con tu API key de Anthropic
```

## Uso

> En desarrollo. Ver [docs/IMPLEMENTATION.md](docs/IMPLEMENTATION.md) para el plan de implementación por fases.

## Documentación

- **[ZUZENDU_v3_sistema.md](docs/ZUZENDU_v3_sistema.md)** — Especificación técnica completa: rúbrica, catálogo de errores, feedback, formato JSON
- **[IMPLEMENTATION.md](docs/IMPLEMENTATION.md)** — Plan de implementación por fases

## Licencia

Proyecto privado. Uso interno.
