"""Una conversación con un servidor MCP, sin modelo y sin harness: lo que viaja. Lección 40.

    python mcp_a_mano.py python servidor_incidencias.py
"""
import sys

from cliente_mcp import ServidorMCP

servidor = ServidorMCP(*sys.argv[1:], traza=True)    # descubrir también es una petición
servidor.herramientas()
for estado in ("abierta", "pendiente"):
    try:
        servidor.llamar("incidencias", {"estado": estado})
    except RuntimeError as e:
        print("error:", e)
servidor.cerrar()
