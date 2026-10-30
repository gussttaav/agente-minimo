"""Un pedido al agente, contra el modelo local, turno a turno. Lección 33 del curso.

    python correr.py "¿Qué recetas hay y cuál lleva cebolla?"
"""
import json
import sys
import time

from agente import agente
from api import ModeloAPI
from entorno import ENTORNO


def linea(b):
    """Un bloque en una línea, y si es una observación, si es un error."""
    if b["type"] == "text":
        return "texto        " + " ".join(b["text"].split())
    if b["type"] == "tool_use":
        return "llamada      %s %s" % (b["name"], json.dumps(b["input"], ensure_ascii=False))
    return ("error        " if b["is_error"] else "observación  ") + b["content"].replace("\n", " / ")


class Traza:
    """Un modelo que envuelve a otro y escribe lo que viaja. Para el bucle, es un modelo más."""
    def __init__(self, modelo):
        self.modelo, self.turno = modelo, 0

    def __call__(self, mensajes, herramientas=()):
        rol, contenido = mensajes[-1]
        if rol == "usuario" and isinstance(contenido, list):     # las observaciones de antes
            for b in contenido:
                print("  →  " + linea(b))
        self.turno, t = self.turno + 1, time.time()
        r = self.modelo(mensajes, herramientas)
        u = self.modelo.usage
        print("turno %d  %.0f s  %d tokens de entrada" % (self.turno, time.time() - t,
              u["input_tokens"] + u.get("cache_read_input_tokens", 0)))
        for b in r:
            print("  ←  " + linea(b))
        return r


entorno = dict(ENTORNO)
motivo, texto, M = agente(Traza(ModeloAPI()), sys.argv[1], entorno)
print(motivo, "·", "%d mensajes en M" % len(M))
for ruta in sorted(entorno):
    if entorno[ruta] != ENTORNO.get(ruta):
        print("cambia", ruta, "->", entorno[ruta])
