"""editar(ruta, antiguo, nuevo): un cambio en un sitio, o ninguno. Lección 34 del curso."""
from pathlib import Path

from herramientas.comun import objeto

CLASE = "escritura"
HERRAMIENTA = {"name": "editar", "description": "Cambia en el fichero ruta el texto antiguo "
               "por nuevo. antiguo tiene que aparecer en el fichero exactamente una vez, "
               "copiado tal cual, con sus espacios y sus saltos de línea; si no, no cambia "
               "nada y dice por qué.",
               "input_schema": objeto(ruta="la ruta del fichero", antiguo="el texto que cambiar",
                                      nuevo="el texto que lo sustituye")}


def editar(entorno, ruta, antiguo, nuevo):
    p = Path(entorno, ruta)
    if not p.is_file():
        raise FileNotFoundError("no existe el fichero %r" % ruta)
    texto = p.read_text(encoding="utf-8")
    veces = texto.count(antiguo) if antiguo else 0     # "" aparecería en todas partes
    if veces == 0:
        raise ValueError("antiguo no aparece en %s: cópialo tal cual del fichero. "
                         "No se ha cambiado nada" % ruta)
    if veces > 1:
        raise ValueError("antiguo aparece %d veces en %s: añade líneas de alrededor para que "
                         "sea único. No se ha cambiado nada" % (veces, ruta))
    p.write_text(texto.replace(antiguo, nuevo), encoding="utf-8")
    return "editado %s en la línea %d" % (ruta, texto[:texto.index(antiguo)].count("\n") + 1)
