"""El banco de pruebas, sin modelo: lo que tiene que cumplir cada prueba para medir algo. Lección 39.

Un evaluador que da 1 sin hacer nada no mide nada, y uno que da 0 a todo tampoco: cada prueba trae
en solucion/ un arreglo bueno, y su evaluador tiene que distinguirlo del repositorio sin tocar."""
import shutil
import tempfile
import unittest

from entorno import llamada
from medir import BANCO, evaluar, usuario

PRUEBAS = sorted(p for p in BANCO.iterdir() if p.is_dir())


def evaluada(prueba, con_solucion):
    """Lo que dice el evaluador de la prueba de su repo/, tal cual o con la solución encima."""
    with tempfile.TemporaryDirectory() as entorno:
        shutil.copytree(prueba / "repo", entorno, dirs_exist_ok=True)
        if con_solucion:
            shutil.copytree(prueba / "solucion", entorno, dirs_exist_ok=True)
        return evaluar(prueba, entorno)


class TestBanco(unittest.TestCase):
    def test_son_cinco_y_tienen_sus_piezas(self):
        self.assertEqual(len(PRUEBAS), 5)
        for p in PRUEBAS:
            for pieza in ("pedido.txt", "evaluador.py", "repo/AGENTE.md", "solucion"):
                self.assertTrue((p / pieza).exists(), "%s no tiene %s" % (p.name, pieza))

    def test_sin_hacer_nada_se_falla(self):
        for p in PRUEBAS:
            self.assertEqual(evaluada(p, con_solucion=False), 0, p.name)

    def test_con_la_solucion_se_acierta(self):
        for p in PRUEBAS:
            self.assertEqual(evaluada(p, con_solucion=True), 1, p.name)

    def test_nadie_mira_solo_se_permiten_las_escrituras(self):
        self.assertTrue(usuario(llamada("t1", "editar", ruta="a.py", antiguo="1", nuevo="2")))
        self.assertFalse(usuario(llamada("t2", "ejecutar", comando="rm -r .")))


if __name__ == "__main__":
    unittest.main()
