"""Lo que comparten las herramientas: el esquema de sus argumentos y qué rutas se ven."""
from pathlib import Path


def objeto(**campos):                     # un esquema: estos campos, de texto y obligatorios
    return {"type": "object", "required": list(campos), "additionalProperties": False,
            "properties": {c: {"type": "string", "description": d} for c, d in campos.items()}}


def visible(ruta):                        # ni .git ni las cachés de Python
    return not any(p.startswith(".") or p == "__pycache__" for p in ruta.parts)


def dentro(entorno, ruta):                # lección 37: la ruta, resuelta, cae en la carpeta
    raiz = Path(entorno).resolve()
    try:
        return Path(raiz, ruta).resolve().is_relative_to(raiz)
    except (OSError, ValueError):         # una ruta que el sistema no entiende no está dentro
        return False
