# El evaluador de la prueba: lo que tiene que hacer el código, con casos que el agente no ha visto.
import unittest
from pathlib import Path

from unidades import a_kilos


class Evaluador(unittest.TestCase):
    def test_a_kilos(self):
        self.assertEqual(a_kilos(1500), 1.5)
        self.assertEqual(a_kilos(250), 0.25)

    def test_tiene_su_test(self):
        self.assertIn('a_kilos', Path('test_unidades.py').read_text(encoding='utf-8'))
