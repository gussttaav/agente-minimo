"""El mini-benchmark: cada prueba de banco/, unas cuantas veces, y su tasa de acierto. Lección 39.

    python medir.py 3

Una prueba es una carpeta de banco/: repo/, el repositorio que recibe el agente; pedido.txt, lo
que se le pide; y evaluador.py, unos tests que el agente no ve. El agente trabaja sobre una copia
de repo/, y al terminar, como termine, el evaluador mira esa copia: no lee su texto final.
"""
import math
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from agente import agente
from api import ModeloAPI
from compactar import INSTRUCCION, compactar
from herramientas import CLASES

BANCO = Path(__file__).parent / "banco"
LIMITE = 60                          # segundos para cada orden del evaluador


def evaluar(prueba, entorno):
    """1 si pasan los tests de la copia, como los ha dejado el agente, y los del evaluador; si no, 0."""
    shutil.copy(prueba / "evaluador.py", entorno)        # llega después: el agente no lo ha visto
    for argumentos in (["-m", "unittest"], ["-m", "unittest", "evaluador"]):
        try:
            r = subprocess.run([sys.executable, *argumentos], cwd=entorno, capture_output=True,
                               timeout=LIMITE)
        except subprocess.TimeoutExpired:
            return 0
        if r.returncode != 0:
            return 0
    return 1


def usuario(ll):
    """Nadie mira: sí a las escrituras, que el sandbox deja en la copia; no a otros comandos."""
    return CLASES[ll["name"]] == "escritura"


class Cuenta:
    """Un modelo que envuelve a otro y cuenta sus turnos, sus compactaciones y su petición mayor."""
    def __init__(self, modelo):
        self.modelo, self.turnos, self.compactaciones, self.pico = modelo, 0, 0, 0

    def __call__(self, mensajes, herramientas=()):
        if mensajes[-1][1] == INSTRUCCION:
            self.compactaciones += 1
        else:
            self.turnos += 1
        r = self.modelo(mensajes, herramientas)
        self.usage = u = self.modelo.usage                # compactar mira aquí
        self.pico = max(self.pico, u["input_tokens"] + u.get("cache_read_input_tokens", 0))
        return r


def intento(prueba):
    """Un intento de una prueba, en una copia que se tira: (acierto, motivo, modelo, segundos)."""
    pedido = (prueba / "pedido.txt").read_text(encoding="utf-8").strip()
    modelo, t = Cuenta(ModeloAPI()), time.time()
    with tempfile.TemporaryDirectory() as entorno:
        shutil.copytree(prueba / "repo", entorno, dirs_exist_ok=True)
        try:
            motivo, _, _ = agente(modelo, pedido, entorno, usuario=usuario, compactar=compactar,
                                  delegar=Cuenta(ModeloAPI()))
        except Exception as e:                   # un 400, un límite de tiempo: el intento acaba
            motivo = "excepción (%s)" % str(e)[:60]
        return evaluar(prueba, entorno), motivo, modelo, time.time() - t


def wilson(k, n):
    """El intervalo de Wilson al 95 % de k aciertos en n, el de la lección 23."""
    a, c = k / n, 1.96 ** 2 / n
    centro, r = (a + c / 2) / (1 + c), 1.96 * math.sqrt(a * (1 - a) / n + c / (4 * n)) / (1 + c)
    return centro - r, centro + r


if __name__ == "__main__":
    repeticiones = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    pruebas = sorted(p for p in BANCO.iterdir() if p.is_dir())
    aciertos = {p.name: [] for p in pruebas}
    falsos = 0                                   # el agente acaba en fin y el evaluador dice 0
    for vez in range(1, repeticiones + 1):
        for p in pruebas:
            a, motivo, m, s = intento(p)
            aciertos[p.name].append(a)
            falsos += motivo == "fin" and not a
            print("%-12s %d  %-7s  %-9s %2d turnos  %d resúmenes  %4d tokens  %4.0f s"
                  % (p.name, vez, "acierta" if a else "falla", motivo, m.turnos, m.compactaciones,
                     m.pico, s), flush=True)
    for nombre, a in aciertos.items():
        print("%-12s %d de %d" % (nombre, sum(a), len(a)))
    k, n = sum(map(sum, aciertos.values())), repeticiones * len(pruebas)
    print("aciertos: %d de %d = %.3f, Wilson [%.3f, %.3f]" % (k, n, k / n, *wilson(k, n)))
    print("acaban diciendo que han terminado y fallan: %d" % falsos)
