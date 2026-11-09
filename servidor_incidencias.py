"""Un servidor MCP mínimo, por stdio: una herramienta, incidencias. Lección 40 del curso.

Lee una petición por línea de stdin y escribe una respuesta por línea en stdout. Por stdout no
sale nada que no sea un mensaje del protocolo; lo que el servidor quiera contar va a stderr.
"""
import json
import sys
from pathlib import Path

VERSION = "2026-07-28"
META = "io.modelcontextprotocol/"
DATOS = json.loads(Path(__file__).with_name("incidencias.json").read_text(encoding="utf-8"))
HERRAMIENTA = {"name": "incidencias",
               "description": "Lista las incidencias del repositorio que tienen un estado, una por "
                              "línea: número, estado, fichero y título.",
               "inputSchema": {"type": "object", "required": ["estado"], "additionalProperties": False,
                               "properties": {"estado": {"type": "string",
                                                         "description": "abierta o cerrada"}}}}


def error(codigo, mensaje, **datos):
    return {"error": dict(code=codigo, message=mensaje, **({"data": datos} if datos else {}))}


def completo(**campos):
    return {"result": {"resultType": "complete", **campos,
                       "_meta": {META + "serverInfo": {"name": "incidencias", "version": "1"}}}}


def incidencias(estado):
    """(texto, es_error): las incidencias de un estado, o por qué no hay lista."""
    if estado not in ("abierta", "cerrada"):
        return "el estado es abierta o cerrada, no %r" % estado, True
    filas = ["#%d [%s] %s: %s" % (i["id"], i["estado"], i["fichero"], i["titulo"])
             for i in DATOS if i["estado"] == estado]
    return "\n".join(filas) or "no hay incidencias %s" % estado, False


def responder(metodo, params):
    """El result o el error de una petición; los tres métodos que sabe y nada más."""
    meta = params.get("_meta", {})
    if META + "protocolVersion" not in meta or META + "clientCapabilities" not in meta:
        return error(-32602, "faltan campos obligatorios en _meta")
    if meta[META + "protocolVersion"] != VERSION:
        return error(-32022, "Unsupported protocol version", supported=[VERSION],
                     requested=meta[META + "protocolVersion"])
    if metodo == "server/discover":
        return completo(supportedVersions=[VERSION], capabilities={"tools": {}}, ttlMs=0,
                        cacheScope="private")
    if metodo == "tools/list":
        return completo(tools=[HERRAMIENTA], ttlMs=0, cacheScope="private")
    if metodo == "tools/call" and params.get("name") == "incidencias":
        texto, malo = incidencias(params.get("arguments", {}).get("estado"))
        return completo(content=[{"type": "text", "text": texto}], isError=malo)
    if metodo == "tools/call":
        return error(-32602, "Unknown tool: %s" % params.get("name"))
    return error(-32601, "Method not found: " + metodo)


for linea in sys.stdin:
    mensaje = json.loads(linea)
    if "id" in mensaje:                              # una notificación no tiene id ni respuesta
        respuesta = responder(mensaje["method"], mensaje.get("params", {}))
        print(json.dumps({"jsonrpc": "2.0", "id": mensaje["id"], **respuesta},
                         separators=(",", ":")), flush=True)
