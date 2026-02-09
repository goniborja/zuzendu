# ZUZENDU v3 — Pasos para arrancar

## 1. Crear el repo en GitHub

Ve a https://github.com/new y crea:
- **Nombre:** `zuzendu`
- **Visibilidad:** Private (tiene datos de rúbrica, no hace falta público)
- **NO** inicialices con README (lo tenemos ya)

## 2. Inicializar en local

Abre la terminal y ejecuta esto (adapta la ruta si quieres otra ubicación):

```bash
# Crear la carpeta del proyecto
mkdir -p ~/proyectos/zuzendu
cd ~/proyectos/zuzendu

# Inicializar git
git init
git branch -M main
```

## 3. Crear la estructura

```bash
# Carpetas
mkdir -p config src tests/testu_kalibrazioa scripts templates docs
mkdir -p data/azterketa_fitxak data/ikasle_testuak data/emaitzak

# .gitkeep para que git trackee las carpetas vacías
touch data/azterketa_fitxak/.gitkeep
touch data/ikasle_testuak/.gitkeep
touch data/emaitzak/.gitkeep
touch tests/testu_kalibrazioa/.gitkeep
```

## 4. Copiar los archivos del scaffold

Los archivos que he generado (README.md, .gitignore, .env.example, requirements.txt, docs/*) los descargas y los colocas en la raíz del proyecto. O si usas Claude Desktop, simplemente pídele que los cree directamente.

La estructura final debe ser:
```
zuzendu/
├── .gitignore
├── .env.example
├── README.md
├── requirements.txt
├── config/
├── src/
├── tests/testu_kalibrazioa/
├── scripts/
├── templates/
├── data/{azterketa_fitxak,ikasle_testuak,emaitzak}/
└── docs/
    ├── ZUZENDU_v3_sistema.md
    └── IMPLEMENTATION.md
```

## 5. Configurar entorno Python

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar API key
cp .env.example .env
# Edita .env y pon tu API key real de Anthropic
```

## 6. Primer commit y push

```bash
git add .
git commit -m "feat: scaffold inicial ZUZENDU v3 - estructura + documentación"
git remote add origin https://github.com/goniborja/zuzendu.git
git push -u origin main
```

## 7. Siguiente paso: Fase 1.1

Con Claude Desktop, pídele:
> "Vamos a implementar la Fase 1.1: crear errubrika.json. 
> Tienes la especificación en docs/ZUZENDU_v3_sistema.md"

Él leerá el doc y generará el JSON completo.

---

**Flujo de trabajo recomendado con Claude Desktop:**
1. Siempre trabaja en una rama por fase: `git checkout -b fase/1.1-errubrika`
2. Implementa con Claude Desktop
3. Testea
4. Merge a main: `git checkout main && git merge fase/1.1-errubrika`
5. Siguiente fase
