"""El bucle del agente. Lección 27 del curso, sin tocar salvo por el usuario y la compactación.

Lección 38: las herramientas son un argumento, porque un subagente corre este mismo bucle con
menos herramientas, y el agente principal con una más.
"""
from entorno import FUNCIONES, HERRAMIENTAS
from permisos import ejecutar


def bucle(modelo, inicio, entorno, tope, usuario=None, compactar=None,
          herramientas=HERRAMIENTAS, funciones=FUNCIONES):
    """Hasta que el modelo no pida nada, o el tope: (motivo, texto, M)."""
    M = list(inicio)
    for turno in range(tope):
        r = modelo(M, herramientas)
        M.append(("asistente", r))
        llamadas = [b for b in r if b["type"] == "tool_use"]
        if not llamadas:
            return "fin", " ".join(b["text"] for b in r if b["type"] == "text"), M
        if compactar is not None:                    # lección 36: antes de las observaciones
            M = compactar(modelo, M, herramientas=herramientas)
        M.append(("usuario", [ejecutar(ll, entorno, usuario, herramientas, funciones)
                               for ll in llamadas]))
    return "tope", None, M
