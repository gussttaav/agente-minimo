"""delegar(encargo): otro bucle, que lee por el agente y le devuelve su texto final. Lección 38.

Lo que lee el modelo y lo que lee el permiso están aquí, como en las demás herramientas. La
función no: necesita un modelo, y una herramienta sólo recibe la carpeta. La escribe
subagente.py, y agente.py se la da al bucle junto con las otras cinco.
"""
from herramientas.comun import objeto

CLASE = "lectura"                    # el subagente sólo tiene herramientas de lectura
RUTAS = []                           # el encargo no es una ruta
HERRAMIENTA = {"name": "delegar", "description": "Encarga a un subagente una pregunta sobre el "
               "repositorio que exige leer o buscar en varios ficheros. El subagente sólo lee, "
               "con su propia conversación, y te devuelve su respuesta en pocas líneas: lo que "
               "él lea no ocupa la tuya. No ve esta conversación, así que escribe el encargo "
               "entero: qué quieres saber y dónde buscarlo.",
               "input_schema": objeto(encargo="la pregunta, completa, que el subagente contesta")}
