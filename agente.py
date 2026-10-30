"""El agente: el inicio y el bucle. Lección 31 del curso."""
from bucle import bucle

SISTEMA = "Trabajas con los ficheros del usuario mediante tus herramientas."


def inicio(pedido):
    return [("sistema", SISTEMA), ("usuario", pedido)]


def agente(modelo, pedido, entorno, tope=10, usuario=None):
    """Un pedido, hasta que el modelo no pida nada o se acabe el tope: (motivo, texto, M)."""
    return bucle(modelo, inicio(pedido), entorno, tope, usuario)
