"""Los bloques del protocolo, el esquema de cada llamada y los ficheros de los tests.

Lecciones 26 y 28 del curso. Hasta la lección 34, también el entorno: un diccionario en
memoria con cuatro herramientas. Ahora el entorno es una carpeta de tu disco, las herramientas
están en herramientas/, y el diccionario es lo que los tests escriben en una carpeta temporal.
"""
import json

from herramientas import FUNCIONES, HERRAMIENTAS     # bucle y permisos las importan de aquí

ENTORNO = {"lista.txt": "pan, leche, patatas",
           "notas.txt": "El sábado vienen cuatro a cenar.",
           "recetas/gazpacho.txt": "Gazpacho: tomates, pepino, pimiento, ajo.",
           "recetas/tortilla.txt": "Tortilla: huevos, patatas, cebolla."}


def texto(t):
    return {"type": "text", "text": t}
def llamada(id, nombre, **argumentos):
    return {"type": "tool_use", "id": id, "name": nombre, "input": argumentos}
def resultado(id, contenido):
    return {"type": "tool_result", "tool_use_id": id, "content": contenido, "is_error": False}
def error(id, contenido):
    return {"type": "tool_result", "tool_use_id": id, "content": contenido, "is_error": True}

def muestra(b):                                      # un bloque, en una línea
    if b["type"] == "text":
        return "text         " + b["text"]
    if b["type"] == "tool_use":
        return "tool_use     %s %s %s" % (b["id"], b["name"], json.dumps(b["input"], ensure_ascii=False))
    return "tool_result  %s %s" % (b["tool_use_id"], b["content"].replace("\n", " / "))


TIPOS = {"string": str, "integer": int, "boolean": bool}

def incumple(b):
    """Por qué no se puede ejecutar la llamada b, o None si cumple su esquema."""
    h = next((h for h in HERRAMIENTAS if h["name"] == b["name"]), None)
    if h is None:
        return "no hay ninguna herramienta %r" % b["name"]
    esquema, argumentos = h["input_schema"], b["input"]
    if not isinstance(argumentos, dict):
        return "input no es un objeto"
    for campo in esquema["required"]:
        if campo not in argumentos:
            return "falta el campo %r" % campo
    for campo, valor in argumentos.items():
        if campo not in esquema["properties"]:
            return "sobra el campo %r" % campo
        tipo = esquema["properties"][campo]["type"]
        if type(valor) is not TIPOS[tipo]:
            return "el campo %r no es de tipo %s" % (campo, tipo)
    return None
