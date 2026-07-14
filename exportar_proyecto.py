from pathlib import Path

# ==========================================================
# CONFIGURACION
# ==========================================================

# Carpeta donde está este script
PROYECTO = Path(__file__).parent

# Archivo de salida
SALIDA = PROYECTO / "codigo_completo.txt"

# ==========================================================
# CARPETAS A IGNORAR
# ==========================================================

EXCLUIR_CARPETAS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".tox",
    ".nox",
    ".vscode",
    ".idea",
    "node_modules",
    "dist",
    "build",
    "env",
    "ENV",
    "venv",
    "htmlcov",
    ".coverage",
}

# ==========================================================
# ARCHIVOS A IGNORAR
# ==========================================================

EXCLUIR_ARCHIVOS = {
    "exportar_proyecto.py",
    "codigo_completo.txt",
    ".DS_Store",
}

# ==========================================================
# EXTENSIONES A EXPORTAR
# ==========================================================

EXTENSIONES_PERMITIDAS = {
    ".py",
    ".sql",
    ".json",
    ".txt",
    ".md",
    ".html",
    ".css",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
}

# ==========================================================
# EXTENSIONES A IGNORAR
# ==========================================================

EXTENSIONES_EXCLUIDAS = {
    ".db",
    ".sqlite",
    ".sqlite3",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".bmp",
    ".ico",
    ".svg",
    ".pdf",
    ".zip",
    ".rar",
    ".7z",
    ".exe",
    ".dll",
    ".so",
    ".pyc",
    ".pyo",
    ".log",
    ".mp3",
    ".mp4",
    ".avi",
    ".mov",
    ".wav",
    ".ttf",
    ".otf",
    ".woff",
    ".woff2",
}

# ==========================================================
# FUNCION PARA SABER SI SE EXPORTA
# ==========================================================

def exportar_archivo(archivo):

    if archivo.is_dir():
        return False

    # Ignorar carpetas
    if any(parte in EXCLUIR_CARPETAS for parte in archivo.parts):
        return False

    # Ignorar archivos específicos
    if archivo.name in EXCLUIR_ARCHIVOS:
        return False

    # Ignorar TODOS los archivos ocultos
    if archivo.name.startswith("."):
        return False

    # Ignorar extensiones
    if archivo.suffix.lower() in EXTENSIONES_EXCLUIDAS:
        return False

    # Solo exportar extensiones permitidas
    return archivo.suffix.lower() in EXTENSIONES_PERMITIDAS

# ==========================================================
# EXPORTACION
# ==========================================================

archivos_exportados = 0
lineas_exportadas = 0

with open(SALIDA, "w", encoding="utf-8") as salida:

    salida.write("=" * 100 + "\n")
    salida.write("EXPORTACION DEL PROYECTO\n")
    salida.write("=" * 100 + "\n\n")

    for archivo in sorted(PROYECTO.rglob("*")):

        if not exportar_archivo(archivo):
            continue

        ruta = archivo.relative_to(PROYECTO)

        salida.write("=" * 100 + "\n")
        salida.write(f"ARCHIVO: {ruta}\n")
        salida.write("=" * 100 + "\n\n")

        try:
            with open(archivo, "r", encoding="utf-8") as f:

                contenido = f.read()

                salida.write(contenido)
                salida.write("\n\n")

                archivos_exportados += 1
                lineas_exportadas += contenido.count("\n") + 1

        except UnicodeDecodeError:
            salida.write("[Archivo no compatible con UTF-8]\n\n")

        except Exception as e:
            salida.write(f"[ERROR]: {e}\n\n")

print()
print("=" * 60)
print("EXPORTACION COMPLETADA")
print("=" * 60)
print(f"Proyecto : {PROYECTO}")
print(f"Salida    : {SALIDA}")
print(f"Archivos  : {archivos_exportados}")
print(f"Lineas    : {lineas_exportadas}")
print("=" * 60)