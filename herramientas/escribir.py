"""escribir(ruta, contenido): un fichero nuevo, nunca uno que ya existe. Lecciones 26 y 34."""
from pathlib import Path

from herramientas.comun import objeto

CLASE = "escritura"
HERRAMIENTA = {"name": "escribir", "description": "Crea un fichero nuevo con este contenido. "
               "Si el fichero ya existe, no lo toca: para cambiar un fichero que existe, usa "
               "editar.",
               "input_schema": objeto(ruta="la ruta del fichero nuevo",
                                      contenido="su contenido, entero")}


def escribir(entorno, ruta, contenido):
    p = Path(entorno, ruta)
    if p.exists():
        raise FileExistsError("ya existe %r: para cambiarlo, usa editar. No se ha escrito nada"
                              % ruta)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(contenido, encoding="utf-8")
    return "escritos %d caracteres en %s" % (len(contenido), ruta)
