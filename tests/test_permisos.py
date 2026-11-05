"""El sandbox, la lista de comandos y el comando sin shell. Lección 37 del curso."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

from entorno import llamada
from herramientas.ejecutar import ejecutar as correr
from permisos import ejecutar, permiso


class TestPermisos(unittest.TestCase):
    def setUp(self):
        self.entorno = self.enterContext(tempfile.TemporaryDirectory())
        self.preguntas = []

    def usuario(self, ll):                # dice que sí a todo, y apunta qué se le pregunta
        self.preguntas.append(ll["id"])
        return True

    def test_una_ruta_fuera_no_se_ejecuta_ni_se_pregunta(self):
        fuera = str(Path(self.entorno).parent / "otro.txt")
        for ll in (llamada("t1", "leer", ruta="../otro.txt"), llamada("t2", "leer", ruta=fuera),
                   llamada("t3", "escribir", ruta="a/../../otro.txt", contenido="x")):
            r = ejecutar(ll, self.entorno, self.usuario)
            self.assertTrue(r["is_error"])
            self.assertTrue(r["content"].endswith("está fuera de la carpeta de trabajo"))
        self.assertEqual(self.preguntas, [])

    def test_un_enlace_que_sale_de_la_carpeta(self):
        try:
            os.symlink(Path(self.entorno).parent, Path(self.entorno, "enlace"))
        except OSError:                   # Windows pide permisos para crear enlaces
            self.skipTest("este sistema no deja crear enlaces simbólicos")
        r = ejecutar(llamada("t1", "leer", ruta="enlace/otro.txt"), self.entorno, self.usuario)
        self.assertTrue(r["content"].endswith("está fuera de la carpeta de trabajo"))

    def test_la_lista_de_comandos_enteros_y_nada_mas(self):
        def decide(comando):
            return permiso(llamada("t1", "ejecutar", comando=comando))
        self.assertEqual(decide("python -m unittest"), "permitir")
        self.assertEqual(decide("python  -m 'unittest'"), "permitir")
        for comando in ("python -m unittest; rm -r .", "python -m unittest -v", "sh instalar.sh"):
            self.assertEqual(decide(comando), "preguntar")

    def test_un_comando_fuera_de_la_lista_sin_usuario(self):
        r = ejecutar(llamada("t1", "ejecutar", comando="sh instalar.sh"), self.entorno)
        self.assertEqual(r["content"], "no se ha ejecutado: el usuario no lo ha permitido")

    def test_sin_shell_un_punto_y_coma_es_un_argumento(self):
        r = correr(self.entorno, '"%s" -c "import sys; print(sys.argv[1:])" ; echo hola' % sys.executable)
        self.assertIn("[';', 'echo', 'hola']", r)


if __name__ == "__main__":
    unittest.main()
