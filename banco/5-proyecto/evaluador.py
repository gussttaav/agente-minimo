# El evaluador de la prueba: lo que tiene que hacer el código, con casos que el agente no ha visto.
import unittest
from pathlib import Path

from ofertas import descuento


class Evaluador(unittest.TestCase):
    def test_descuento(self):
        self.assertEqual(descuento(200, 15), 170)
        self.assertEqual(descuento(349, 15), 297)        # 296.65: al céntimo más cercano
        self.assertIs(type(descuento(199, 10)), int)     # céntimos, nunca un float

    def test_tiene_su_test(self):
        self.assertIn('descuento', Path('test_ofertas.py').read_text(encoding='utf-8'))
