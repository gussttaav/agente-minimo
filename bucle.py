"""El bucle del agente. Lección 27 del curso, sin tocar salvo por el usuario."""
from entorno import HERRAMIENTAS
from permisos import ejecutar


def bucle(modelo, inicio, entorno, tope, usuario=None):
    """Hasta que el modelo no pida nada, o el tope: (motivo, texto, M)."""
    M = list(inicio)
    for turno in range(tope):
        r = modelo(M, HERRAMIENTAS)
        M.append(("asistente", r))
        llamadas = [b for b in r if b["type"] == "tool_use"]
        if not llamadas:
            return "fin", " ".join(b["text"] for b in r if b["type"] == "text"), M
        M.append(("usuario", [ejecutar(ll, entorno, usuario) for ll in llamadas]))
    return "tope", None, M
