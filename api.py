"""modelo(mensajes, herramientas) -> respuesta, sobre la API de mensajes. Lección 33 del curso.

El adaptador: traduce M al protocolo, manda la petición con urllib y devuelve la respuesta
tal como llega. Ninguna biblioteca del proveedor.
"""
import json
import os
import urllib.error
import urllib.request

URL = os.environ.get("ANTHROPIC_BASE_URL", "http://localhost:11434") + "/v1/messages"
CLAVE = os.environ.get("ANTHROPIC_API_KEY")       # el servidor local no la pide
ROLES = {"usuario": "user", "asistente": "assistant"}


def peticion(nombre, max_tokens, mensajes, herramientas):
    """M en el protocolo: el prompt de sistema, a su campo; los demás, con el rol en inglés."""
    p = {"model": nombre, "max_tokens": max_tokens, "thinking": {"type": "disabled"},
         "system": "\n\n".join(c for rol, c in mensajes if rol == "sistema"),
         "messages": [{"role": ROLES[rol], "content": c} for rol, c in mensajes if rol != "sistema"]}
    if herramientas:
        p["tools"] = list(herramientas)
    return p


def enviar(p):
    """Un POST con la petición; lo que contesta el servidor, leído del JSON."""
    cabeceras = {"content-type": "application/json"}
    if CLAVE:
        cabeceras.update({"x-api-key": CLAVE, "anthropic-version": "2023-06-01"})
    req = urllib.request.Request(URL, data=json.dumps(p).encode("utf-8"), headers=cabeceras)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:              # un 400, un 404: el servidor dice por qué
        raise RuntimeError("el servidor contesta %d: %s" % (e.code, e.read().decode("utf-8")))


class ModeloAPI:
    """modelo(mensajes, herramientas) -> respuesta, de un modelo que sirve otro programa."""
    def __init__(self, nombre="local", max_tokens=1024):
        self.nombre, self.max_tokens = nombre, max_tokens
        self.usage = None                             # el de la última petición, para quien mire

    def __call__(self, mensajes, herramientas=()):
        r = enviar(peticion(self.nombre, self.max_tokens, mensajes, herramientas))
        self.usage = r["usage"]
        if r["stop_reason"] == "max_tokens":          # una respuesta cortada no se devuelve
            raise RuntimeError("la respuesta no cabe en max_tokens=%d" % self.max_tokens)
        return r["content"]
