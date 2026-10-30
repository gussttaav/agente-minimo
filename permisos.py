"""El permiso y el ejecutar que lo consulta. Lecciones 28 y 29 del curso.

Un cambio respecto a las celdas del navegador: el usuario es un argumento, como el modelo.
Allí era una función global que los tests sustituían; en ficheros, quien llama dice a quién
se pregunta. Sin nadie a quien preguntar (usuario=None), preguntar cuenta como denegar.
"""
from entorno import FUNCIONES, error, incumple, resultado

CLASES = {"leer": "lectura", "listar": "lectura", "buscar": "lectura", "escribir": "escritura"}
PERMISOS = {"lectura": "permitir", "escritura": "preguntar", "ejecución": "preguntar"}


def permiso(ll, permisos=PERMISOS):
    """permitir, preguntar o denegar. Mira la herramienta de la llamada, y nada más."""
    return permisos.get(CLASES.get(ll["name"]), "denegar")


def ejecutar(ll, entorno, usuario=None):
    """Siempre un tool_result. El esquema, después el permiso, después la función."""
    motivo = incumple(ll)
    if motivo is not None:
        return error(ll["id"], "no se ha ejecutado: " + motivo)
    decision = permiso(ll)
    if decision == "denegar":
        return error(ll["id"], "no se ha ejecutado: permiso denegado")
    if decision == "preguntar" and not (usuario and usuario(ll)):
        return error(ll["id"], "no se ha ejecutado: el usuario no lo ha permitido")
    try:
        contenido = FUNCIONES[ll["name"]](entorno, **ll["input"])
    except Exception as e:
        return error(ll["id"], str(e))
    return resultado(ll["id"], contenido)
