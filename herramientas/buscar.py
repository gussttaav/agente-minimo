"""buscar(patron, ruta): las líneas que lo contienen, sin distinguir mayúsculas. Lección 34."""
from pathlib import Path

from herramientas.comun import objeto, visible

CLASE = "lectura"
HERRAMIENTA = {"name": "buscar", "description": "Las líneas que contienen patron, sin "
               "distinguir mayúsculas, en el fichero ruta o en todos los de la carpeta ruta, "
               "cada una como ruta:número: línea.",
               "input_schema": objeto(patron="el texto que buscar",
                                      ruta="un fichero o una carpeta; . es la de trabajo")}


def buscar(entorno, patron, ruta):
    p = Path(entorno, ruta)
    if not p.exists():
        raise FileNotFoundError("no existe %r" % ruta)
    ficheros = [p] if p.is_file() else sorted(f for f in p.rglob("*") if f.is_file())
    lineas = []
    for f in (f for f in ficheros if visible(f.relative_to(entorno))):
        try:
            texto = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:                   # un fichero binario no tiene líneas
            continue
        for n, linea in enumerate(texto.split("\n"), 1):
            if patron.lower() in linea.lower():
                lineas.append("%s:%d: %s" % (f.relative_to(entorno).as_posix(), n, linea))
    return "\n".join(lineas) or "ninguna línea contiene %r en %s" % (patron, ruta)
