"""ejecutar(comando): un programa, con su código de salida y lo que escribe. Lecciones 34 y 37.

Desde la lección 37, sin shell: partes() corta el comando en palabras, la primera es el
programa y las demás sus argumentos, y eso es lo que corre. El permiso corta con la misma
función, así que lo que compara con su lista es lo que se ejecuta.
"""
import shlex
import subprocess

from herramientas.comun import objeto

CLASE = "ejecución"
RUTAS = []                           # lección 37: el comando no es una ruta
LIMITE = 30                                          # segundos
HERRAMIENTA = {"name": "ejecutar", "description": "Ejecuta un programa en la carpeta de trabajo "
               "y devuelve su código de salida, su stdout y su stderr. Sin shell: ni tuberías, "
               "ni redirecciones, ni ; ni &&. Se detiene a los %d segundos." % LIMITE,
               "input_schema": objeto(comando="el programa y sus argumentos, separados por espacios")}


def partes(comando):
    """'python -m unittest' -> ['python', '-m', 'unittest'], con las comillas de la terminal."""
    return shlex.split(comando)            # un ValueError si una comilla no se cierra


def ejecutar(entorno, comando):
    p = partes(comando)
    if not p:
        raise ValueError("el comando está vacío")
    try:
        r = subprocess.run(p, cwd=entorno, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=LIMITE)
    except FileNotFoundError:
        raise FileNotFoundError("no existe el programa %r" % p[0])
    except subprocess.TimeoutExpired:
        raise TimeoutError("no ha terminado en %d s y se ha detenido" % LIMITE)
    return "código de salida %d\n--- stdout\n%s--- stderr\n%s" % (r.returncode, r.stdout, r.stderr)
