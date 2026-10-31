"""ejecutar(comando): un programa, con su código de salida y lo que escribe. Lección 34."""
import subprocess

from herramientas.comun import objeto

CLASE = "ejecución"
LIMITE = 30                                          # segundos
HERRAMIENTA = {"name": "ejecutar", "description": "Ejecuta un comando de la terminal en la "
               "carpeta de trabajo y devuelve su código de salida, su stdout y su stderr. "
               "Se detiene a los %d segundos." % LIMITE,
               "input_schema": objeto(comando="el comando, como lo escribirías en la terminal")}


def ejecutar(entorno, comando):
    try:
        r = subprocess.run(comando, shell=True, cwd=entorno, capture_output=True,
                           encoding="utf-8", errors="replace", timeout=LIMITE)
    except subprocess.TimeoutExpired:
        raise TimeoutError("no ha terminado en %d s y se ha detenido" % LIMITE)
    return "código de salida %d\n--- stdout\n%s--- stderr\n%s" % (r.returncode, r.stdout, r.stderr)
