"""El agente: el inicio y el bucle. Lecciones 31, 35, 36, 38 y 40 del curso.

El inicio de M tiene dos voces. El prompt de sistema es la del harness: qué es el agente y
qué reglas sigue en cualquier repositorio. El fichero de proyecto, AGENTE.md, es la del
repositorio: cómo se trabaja en éste. Se lee una vez, al empezar.
"""
from pathlib import Path

from bucle import bucle
from cliente_mcp import con_servidor
from entorno import FUNCIONES, HERRAMIENTAS
from subagente import REGLA, con_delegar

SISTEMA = """Eres un agente de programación. Trabajas en un repositorio, la carpeta de trabajo (.), y sólo sabes de él lo que te devuelven tus herramientas.

- Escribe en español, aunque el código esté en inglés.
- No expliques lo que vas a hacer: haz la llamada.
- Lee un fichero antes de editarlo, y copia antiguo de esa lectura tal cual, con sus comillas.
- Si una llamada vuelve con un error, no la repitas igual: cambia lo que el error dice.
- Un fichero sólo cambia si llamas a editar o a escribir, y los tests sólo corren si llamas a ejecutar. No digas que has hecho nada que no esté en una llamada tuya.
- Cuando los tests pasen, termina con una frase que diga qué has cambiado."""

PROYECTO = "AGENTE.md"


def inicio(pedido, entorno=None, sistema=SISTEMA):
    """M al empezar: el prompt de sistema, el fichero de proyecto si lo hay, y el pedido."""
    M = [("sistema", sistema)]
    if entorno is not None and Path(entorno, PROYECTO).is_file():
        proyecto = Path(entorno, PROYECTO).read_text(encoding="utf-8")
        M.append(("sistema", "El fichero de proyecto, %s:\n\n%s" % (PROYECTO, proyecto)))
    return M + [("usuario", pedido)]


def agente(modelo, pedido, entorno, tope=10, usuario=None, compactar=None, delegar=None, servidor=None):
    """Un pedido, hasta que el modelo no pida nada o se acabe el tope: (motivo, texto, M).

    Lección 38: con delegar, el modelo de los subagentes, el agente tiene una herramienta más,
    y su prompt de sistema, una regla que dice para qué. Lección 40: con servidor, un ServidorMCP,
    tiene además las que el servidor anuncia.
    """
    herramientas, funciones, sistema = HERRAMIENTAS, FUNCIONES, SISTEMA
    if delegar is not None:
        herramientas, funciones = con_delegar(delegar)
        sistema = SISTEMA + "\n" + REGLA
    if servidor is not None:
        herramientas, funciones = con_servidor(servidor, herramientas, funciones)
    return bucle(modelo, inicio(pedido, entorno, sistema), entorno, tope, usuario, compactar,
                 herramientas, funciones)
