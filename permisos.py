"""El permiso, el sandbox y el ejecutar que los consulta. Lecciones 28, 29 y 37 del curso.

Un cambio respecto a las celdas del navegador: el usuario es un argumento, como el modelo.
Allí era una función global que los tests sustituían; en ficheros, quien llama dice a quién
se pregunta. Sin nadie a quien preguntar (usuario=None), preguntar cuenta como denegar.

Lección 37: el permiso mira también qué comando pide una llamada de ejecución, y antes que el
permiso va el sandbox, que nadie puede abrir: toda ruta que nombra una llamada, resuelta,
tiene que caer dentro de la carpeta de trabajo.

Lección 38: cada bucle dice qué herramientas tiene y con qué funciones; un subagente, menos.
"""
from entorno import FUNCIONES, HERRAMIENTAS, error, incumple, resultado
from herramientas import CLASES, RUTAS               # cada herramienta dice las suyas
from herramientas.comun import dentro
from herramientas.ejecutar import partes

PERMISOS = {"lectura": "permitir", "escritura": "preguntar", "ejecución": "preguntar"}
COMANDOS = ["python -m unittest", "python3 -m unittest"]   # los que corren sin preguntar


def en_la_lista(comando, comandos=COMANDOS):
    """Si el comando, cortado en palabras, es uno de los de la lista, entero."""
    try:
        return partes(comando) in [partes(c) for c in comandos]
    except ValueError:                               # una comilla sin cerrar no es ninguna
        return False


def permiso(ll, permisos=PERMISOS, comandos=COMANDOS):
    """permitir, preguntar o denegar. Mira la llamada (su herramienta y su comando), y nada más."""
    clase = CLASES.get(ll["name"])
    if clase == "ejecución" and en_la_lista(ll["input"].get("comando", ""), comandos):
        return "permitir"
    return permisos.get(clase, "denegar")


def fuera(ll, entorno):
    """La primera ruta de la llamada que cae fuera de la carpeta de trabajo, o None."""
    rutas = [ll["input"][campo] for campo in RUTAS[ll["name"]]]
    return next((r for r in rutas if not dentro(entorno, r)), None)


def ejecutar(ll, entorno, usuario=None, herramientas=HERRAMIENTAS, funciones=FUNCIONES):
    """Siempre un tool_result. El esquema, el sandbox, el permiso y, por último, la función."""
    motivo = incumple(ll, herramientas)
    if motivo is not None:
        return error(ll["id"], "no se ha ejecutado: " + motivo)
    ruta = fuera(ll, entorno)
    if ruta is not None:                             # ni se pregunta: ningún sí lo abre
        return error(ll["id"], "no se ha ejecutado: %s está fuera de la carpeta de trabajo" % ruta)
    decision = permiso(ll)
    if decision == "denegar":
        return error(ll["id"], "no se ha ejecutado: permiso denegado")
    if decision == "preguntar" and not (usuario and usuario(ll)):
        return error(ll["id"], "no se ha ejecutado: el usuario no lo ha permitido")
    try:
        contenido = funciones[ll["name"]](entorno, **ll["input"])
    except Exception as e:
        return error(ll["id"], str(e))
    return resultado(ll["id"], contenido)
