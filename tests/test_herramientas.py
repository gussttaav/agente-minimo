"""Los contratos de editar y escribir, y ejecutar con un comando que falla. Lección 34."""
import sys
import tempfile
import unittest
from pathlib import Path

from herramientas.editar import editar
from herramientas.ejecutar import ejecutar
from herramientas.escribir import escribir

CODIGO = "x = 1\ny = 1\n"


class TestHerramientas(unittest.TestCase):
    def setUp(self):
        self.entorno = self.enterContext(tempfile.TemporaryDirectory())
        self.fichero = Path(self.entorno, "a.py")
        self.fichero.write_text(CODIGO, encoding="utf-8")

    def test_editar_una_vez(self):
        r = editar(self.entorno, "a.py", "y = 1", "y = 2")
        self.assertEqual(r, "editado a.py en la línea 2")
        self.assertEqual(self.fichero.read_text(encoding="utf-8"), "x = 1\ny = 2\n")

    def test_editar_ninguna_o_dos_veces(self):
        for antiguo in ("z = 1", "= 1", ""):
            with self.assertRaises(ValueError):
                editar(self.entorno, "a.py", antiguo, "= 2")
            self.assertEqual(self.fichero.read_text(encoding="utf-8"), CODIGO)

    def test_escribir_no_pisa_un_fichero(self):
        with self.assertRaises(FileExistsError):
            escribir(self.entorno, "a.py", "")
        self.assertEqual(self.fichero.read_text(encoding="utf-8"), CODIGO)

    def test_ejecutar_un_comando_que_falla(self):
        r = ejecutar(self.entorno, '"%s" -c "import sys; sys.exit(3)"' % sys.executable)
        self.assertTrue(r.startswith("código de salida 3\n"))


if __name__ == "__main__":
    unittest.main()
