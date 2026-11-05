"""El subagente: el mismo bucle, con una M nueva, que contesta un encargo. Lección 38 del curso.

M empieza con el prompt de sistema del subagente y el encargo, y nada más: ni el pedido, ni el
fichero de proyecto, ni lo que el agente principal haya leído. Sus herramientas son las de
lectura, y sus llamadas pasan por el mismo ejecutar, con el sandbox. Al agente principal sólo
le vuelve el texto final; la M del subagente se tira.
"""
from bucle import bucle
from entorno import FUNCIONES, HERRAMIENTAS
from herramientas import CLASES, delegar

REGLA = ("- Para averiguar dónde está o qué hace algo del repositorio, encárgaselo a un "
         "subagente con delegar, y lee tú sólo el fichero que vayas a editar.")  # al prompt de sistema
LECTURAS = [h for h in HERRAMIENTAS if CLASES[h["name"]] == "lectura"]    # leer y buscar
TOPE = 6
SISTEMA = """Eres un subagente. Otro agente te ha hecho un encargo sobre un repositorio, la carpeta de trabajo (.), y sólo verá el texto con el que termines. Puedes leer y buscar; no puedes cambiar nada.

- Escribe en español.
- No expliques lo que vas a hacer: haz la llamada.
- buscar dice dónde está algo, no qué hace: antes de contestar qué hace una función, lee el fichero donde está.
- Cuando sepas la respuesta, termina con ella, en menos de 100 palabras: los ficheros y las funciones por su nombre, y las líneas que importen copiadas tal cual.
- Si no la encuentras, dilo, y di qué has mirado."""


def subagente(modelo, encargo, entorno, tope=TOPE):
    """El texto final de otro bucle, que empieza de cero con el encargo y sólo puede leer."""
    motivo, texto, _ = bucle(modelo, [("sistema", SISTEMA), ("usuario", encargo)], entorno, tope,
                             herramientas=LECTURAS)
    if motivo == "tope":
        raise RuntimeError("el subagente ha llegado a su tope de %d turnos sin contestar" % tope)
    return texto


def con_delegar(modelo):
    """Las herramientas del agente principal y sus funciones: las cinco y delegar."""
    def f(entorno, encargo):
        return subagente(modelo, encargo, entorno)
    return HERRAMIENTAS + [delegar.HERRAMIENTA], dict(FUNCIONES, delegar=f)
