"""El modelo guionizado: modelo(mensajes, herramientas) -> respuesta, sacada de un guion.

Lección 18 del curso. Es la implementación de `modelo` sobre la que corren los tests: no
entiende el prompt, no sortea y no decide nada.
"""


class ModeloGuionizado:
    """modelo(mensajes, herramientas) -> respuesta, sacada de un guion escrito de antemano."""
    def __init__(self, guion):
        self.guion = guion                  # [(mensajes que espera, respuesta que da), ...]
        self.turno = 0                      # el puntero: la entrada del guion que toca

    def __call__(self, mensajes, herramientas=()):
        if self.turno == len(self.guion):
            raise RuntimeError("el guion se acabó en el turno %d" % self.turno)
        espera, respuesta = self.guion[self.turno]
        if mensajes != espera:
            i = next(i for i in range(len(mensajes) + 1) if mensajes[i:i + 1] != espera[i:i + 1])
            raise ValueError("turno %d: el mensaje %d no es el del guion" % (self.turno, i))
        self.turno += 1
        return respuesta


def guion_de(inicio, respuestas, vistos):
    """El guion de una conversación: en cada turno, los mensajes que el modelo espera."""
    guion, M = [], list(inicio)
    for r, v in zip(respuestas, vistos):
        guion, M = guion + [(M, r)], M + [("asistente", r), ("usuario", v)]
    return guion
