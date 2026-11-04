"""Lo que ocupa en la ventana cada pieza fija de M, en cada turno. Lección 35 del curso.

    python coste.py ejemplo
"""
import sys

from agente import inicio
from api import enviar, peticion
from entorno import HERRAMIENTAS

VENTANA = 8192                                       # la del Modelfile


def tokens(mensajes, herramientas=()):
    """Los tokens de entrada de una petición con estos mensajes, sin esperar respuesta."""
    u = enviar(peticion("local", 1, mensajes, herramientas))["usage"]
    return u["input_tokens"] + u.get("cache_read_input_tokens", 0)


sistema, *proyecto, pedido = inicio("Hola.", sys.argv[1])
piezas = [("el pedido", [pedido], ()), ("+ las herramientas", [pedido], HERRAMIENTAS),
          ("+ el prompt de sistema", [sistema, pedido], HERRAMIENTAS),
          ("+ el fichero de proyecto", [sistema, *proyecto, pedido], HERRAMIENTAS)]
antes = 0
for nombre, M, h in piezas:
    n = tokens(M, h)
    print("%-26s %5d tokens  (%+d)  %4.1f %% de la ventana" % (nombre, n, n - antes, 100 * n / VENTANA))
    antes = n
