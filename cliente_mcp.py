"""Un cliente MCP mínimo, por stdio: lanza un servidor y le habla. Lección 40 del curso.

El servidor es un subproceso. El cliente le escribe una petición por línea y lee una respuesta
por línea, una a una: no hay sesión, y cada petición lleva en _meta la versión del protocolo.
"""
import json
import queue
import subprocess
import threading

from entorno import TIPOS

VERSION = "2026-07-28"
META = "io.modelcontextprotocol/"
LIMITE = 30                                          # segundos que espera cada respuesta


class ServidorMCP:
    """Un servidor MCP como subproceso, ya descubierto: habla nuestra versión y ofrece herramientas."""
    def __init__(self, *comando, traza=False):
        self.proceso = subprocess.Popen(comando, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                        text=True, encoding="utf-8")
        self.lineas, self.n, self.traza = queue.Queue(), 0, traza
        self.hilo = threading.Thread(target=self.leer, daemon=True)
        self.hilo.start()
        r = self.pedir("server/discover")
        if VERSION not in r["supportedVersions"] or "tools" not in r["capabilities"]:
            self.cerrar()
            raise RuntimeError("el servidor MCP no habla %s o no ofrece herramientas" % VERSION)

    def leer(self):
        for linea in self.proceso.stdout:
            self.lineas.put(linea)
        self.lineas.put(None)                        # el servidor ha cerrado su salida

    def pedir(self, metodo, **params):
        """Una petición y su respuesta: el result, o una excepción con el mensaje del error."""
        self.n += 1
        meta = {META + "protocolVersion": VERSION, META + "clientCapabilities": {},
                META + "clientInfo": {"name": "agente-minimo", "version": "1"}}
        peticion = json.dumps({"jsonrpc": "2.0", "id": self.n, "method": metodo,
                               "params": {"_meta": meta, **params}}, separators=(",", ":"))
        if self.traza:
            print("→", peticion)
        try:
            self.proceso.stdin.write(peticion + "\n")
            self.proceso.stdin.flush()
        except OSError:
            raise RuntimeError("el servidor MCP se ha cerrado")
        while True:
            try:
                linea = self.lineas.get(timeout=LIMITE)
            except queue.Empty:
                raise TimeoutError("el servidor MCP no ha contestado en %d s" % LIMITE)
            if linea is None:
                raise RuntimeError("el servidor MCP se ha cerrado")
            if self.traza:
                print("←", linea.rstrip("\n"))
            r = json.loads(linea)
            if r.get("id") == self.n:                # una respuesta tardía de otra petición se salta
                break
        if "error" in r:
            raise RuntimeError("%s (%d)" % (r["error"]["message"], r["error"]["code"]))
        return r["result"]

    def herramientas(self):
        """Las herramientas que anuncia el servidor, tal como las anuncia."""
        r = self.pedir("tools/list")
        if r.get("nextCursor"):
            raise RuntimeError("el servidor pagina su lista de herramientas, y este cliente no")
        return r["tools"]

    def llamar(self, nombre, argumentos):
        """El texto de la llamada, o una excepción con el texto del servidor si dice que ha fallado."""
        r = self.pedir("tools/call", name=nombre, arguments=argumentos)
        if r.get("resultType", "complete") != "complete":
            raise RuntimeError("el servidor pide más datos, y este cliente no sabe darlos")
        texto = "\n".join(c["text"] for c in r["content"] if c["type"] == "text")
        if r.get("isError"):
            raise RuntimeError(texto)
        return texto

    def cerrar(self):
        self.proceso.stdin.close()                   # el servidor sale al ver el final de su entrada
        try:
            self.proceso.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.proceso.kill()
        self.hilo.join()                             # sin salida que leer, el hilo acaba
        self.proceso.stdout.close()


def herramienta(t):
    """La herramienta de un servidor, en la forma de las nuestras; None si no sabemos comprobarla."""
    esquema = t["inputSchema"]
    campos = esquema.get("properties", {})
    if esquema.get("type") != "object" or any(c.get("type") not in TIPOS for c in campos.values()):
        return None
    return {"name": t["name"], "description": t.get("description", ""),
            "input_schema": {"type": "object", "required": esquema.get("required", []),
                             "properties": campos, "additionalProperties": False}}


def con_servidor(servidor, herramientas, funciones):
    """Las herramientas del agente y sus funciones, más las que ofrece el servidor."""
    ajenas = [h for h in map(herramienta, servidor.herramientas()) if h]
    chocan = {h["name"] for h in herramientas} & {h["name"] for h in ajenas}
    if chocan:
        raise ValueError("el servidor ofrece herramientas que el agente ya tiene: %s"
                         % ", ".join(sorted(chocan)))

    def funcion(nombre):
        return lambda entorno, **argumentos: servidor.llamar(nombre, argumentos)
    return herramientas + ajenas, dict(funciones, **{h["name"]: funcion(h["name"]) for h in ajenas})
