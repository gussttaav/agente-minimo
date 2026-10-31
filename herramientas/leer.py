"""leer(ruta): un fichero entero, o lo que hay en una carpeta. Lección 34 del curso."""
from pathlib import Path

from herramientas.comun import objeto, visible

CLASE = "lectura"
HERRAMIENTA = {"name": "leer", "description": "Devuelve el contenido entero de un fichero. "
               "Si ruta es una carpeta, lo que hay dentro, una ruta por línea; las carpetas "
               "acaban en /. La carpeta de trabajo es .",
               "input_schema": objeto(ruta="la ruta del fichero o de la carpeta")}


def leer(entorno, ruta):
    p = Path(entorno, ruta)
    if p.is_dir():
        hijos = (h.relative_to(entorno) for h in sorted(p.iterdir()))
        return "\n".join(h.as_posix() + ("/" if Path(entorno, h).is_dir() else "")
                         for h in hijos if visible(h))
    if not p.is_file():
        raise FileNotFoundError("no existe el fichero %r" % ruta)
    return p.read_text(encoding="utf-8")
