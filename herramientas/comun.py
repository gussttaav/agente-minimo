"""Lo que comparten las herramientas: el esquema de sus argumentos y qué rutas se ven."""


def objeto(**campos):                     # un esquema: estos campos, de texto y obligatorios
    return {"type": "object", "required": list(campos), "additionalProperties": False,
            "properties": {c: {"type": "string", "description": d} for c, d in campos.items()}}


def visible(ruta):                        # ni .git ni las cachés de Python
    return not any(p.startswith(".") or p == "__pycache__" for p in ruta.parts)
