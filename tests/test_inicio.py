"""El inicio de M, con y sin fichero de proyecto, y cómo llega al protocolo. Lección 35."""
import tempfile
import unittest
from pathlib import Path

import api
from agente import PROYECTO, SISTEMA, inicio


class TestInicio(unittest.TestCase):
    def test_sin_fichero_de_proyecto(self):
        with tempfile.TemporaryDirectory() as entorno:
            self.assertEqual(inicio("Hola.", entorno), [("sistema", SISTEMA), ("usuario", "Hola.")])

    def test_con_fichero_de_proyecto(self):
        with tempfile.TemporaryDirectory() as entorno:
            Path(entorno, PROYECTO).write_text("Los tests: python -m unittest.", encoding="utf-8")
            M = inicio("Hola.", entorno)
        self.assertEqual([rol for rol, _ in M], ["sistema", "sistema", "usuario"])
        self.assertTrue(M[1][1].endswith("Los tests: python -m unittest."))
        p = api.peticion("local", 1024, M, [])        # las dos voces, en el campo system
        self.assertEqual(p["system"], SISTEMA + "\n\n" + M[1][1])
        self.assertEqual(p["messages"], [{"role": "user", "content": "Hola."}])


if __name__ == "__main__":
    unittest.main()
