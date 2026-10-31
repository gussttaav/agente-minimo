"""Un pedido al agente, sobre una copia de una carpeta, contra el modelo local, turno a turno.

Lecciones 33 y 34 del curso.

    python correr.py ejemplo "Los tests fallan: ejecuta python -m unittest y arregla compra.py."
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path

from agente import agente
from api import ModeloAPI
from herramientas.comun import visible


def linea(b):
    """Un bloque en una línea, y si es una observación, si es un error."""
    if b["type"] == "text":
        return "texto        " + " ".join(b["text"].split())
    if b["type"] == "tool_use":
        return "llamada      %s %s" % (b["name"], json.dumps(b["input"], ensure_ascii=False))
    return (("error        " if b["is_error"] else "observación  ")
            + b["content"].rstrip("\n").replace("\n", "\n" + " " * 18))


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


def usuario(ll):
    """Tú, en la terminal: cada escritura y cada comando, antes de que corran."""
    return input("  ?  ¿permites %s? [s/N] " % linea(ll)[13:]).strip().lower() == "s"


carpeta, pedido = sys.argv[1], sys.argv[2]
entorno = tempfile.mkdtemp()                        # una copia: la carpeta no se toca
shutil.copytree(carpeta, entorno, dirs_exist_ok=True)
motivo, texto, M = agente(Traza(ModeloAPI()), pedido, entorno, usuario=usuario)
print(motivo, "·", "%d mensajes en M" % len(M), "· la copia está en", entorno)
for f in sorted(Path(entorno).rglob("*")):
    ruta = f.relative_to(entorno)
    antes = Path(carpeta, ruta)
    igual = antes.is_file() and antes.read_bytes() == f.read_bytes()
    if f.is_file() and visible(ruta) and not igual:
        print("cambia", ruta.as_posix())
