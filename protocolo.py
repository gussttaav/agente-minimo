"""Un turno a mano: el protocolo de mensajes, sin harness. Lección 32 del curso."""
import json
import os
import urllib.request

from entorno import HERRAMIENTAS

URL = os.environ.get("ANTHROPIC_BASE_URL", "http://localhost:11434") + "/v1/messages"


def enviar(peticion):
    """Manda una petición al servidor y devuelve lo que contesta, ya leído del JSON."""
    datos = json.dumps(peticion).encode("utf-8")
    req = urllib.request.Request(URL, data=datos, headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=300) as r:
        return json.load(r)


peticion = {
    "model": "local",
    "max_tokens": 1024,
    "thinking": {"type": "disabled"},
    "system": "Trabajas con los ficheros del usuario mediante tus herramientas.",
    "messages": [{"role": "user", "content": "¿Qué hay en lista.txt?"}],
    "tools": HERRAMIENTAS,
}
r = enviar(peticion)
print(json.dumps(r, ensure_ascii=False, indent=2))

llamadas = [b for b in r["content"] if b["type"] == "tool_use"]
if llamadas:                              # el modelo ha pedido algo, y nadie lo ha ejecutado
    observaciones = []
    for ll in llamadas:                   # el harness eres tú: escribe lo que contestaría
        contenido = input("\n%s %s -> " % (ll["name"], json.dumps(ll["input"], ensure_ascii=False)))
        observaciones.append({"type": "tool_result", "tool_use_id": ll["id"], "content": contenido})
    peticion["messages"] += [{"role": "assistant", "content": r["content"]},
                             {"role": "user", "content": observaciones}]
    r = enviar(peticion)
    print(json.dumps(r, ensure_ascii=False, indent=2))
