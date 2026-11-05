"""La compactación: cuando M se acerca a la ventana, el modelo resume los turnos viejos.

Lección 36 del curso. Se quedan tal cual el inicio de M (las dos voces y el pedido) y los
últimos turnos; los de en medio se cambian por un resumen que escribe el propio modelo. El
corte cae siempre entre dos turnos, así que ninguna llamada se separa de su observación.
"""
from entorno import HERRAMIENTAS

UMBRAL = 4096          # de 8192: 1024 de reserva y 3072 para lo que traiga el turno en curso
RECIENTES = 2          # los turnos que se quedan tal cual, contando el que está en curso
INSTRUCCION = """El harness va a quitar de M tus turnos anteriores y a dejar en su lugar lo que escribas ahora. No llames a ninguna herramienta. Escribe, en menos de 150 palabras, lo que te hace falta para seguir con el pedido:
- lo que has averiguado de cada fichero que has leído y todavía importa;
- lo que has cambiado, y las llamadas que han fallado y por qué;
- lo que te falta por hacer."""


def tokens(modelo):
    """Los tokens de M según el servidor: los de la última petición y su respuesta."""
    u = modelo.usage
    return u["input_tokens"] + u.get("cache_read_input_tokens", 0) + u["output_tokens"]


def compactar(modelo, M, umbral=UMBRAL, k=RECIENTES, herramientas=HERRAMIENTAS):
    """M, o M con los turnos viejos cambiados por un resumen. M acaba en una respuesta."""
    if tokens(modelo) <= umbral:
        return M
    p = 1 + next(i for i, (rol, _) in enumerate(M) if rol == "usuario")   # hasta el pedido
    corte = len(M) - (2 * k - 1)            # aquí empiezan los k turnos recientes
    if corte - p < 2:                       # ningún turno viejo que resumir
        return M
    r = modelo(M[:corte] + [("usuario", INSTRUCCION)], herramientas)   # las del bucle: la caché
    resumen = " ".join(b["text"] for b in r if b["type"] == "text").strip()
    if not resumen:                         # sin resumen no se quita nada
        return M
    nota = "Resumen de tus turnos anteriores, escrito por ti al compactar:\n\n" + resumen
    return M[:p] + [("usuario", nota)] + M[corte:]
