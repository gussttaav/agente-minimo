# El evaluador de la prueba: lo que tiene que hacer el código, con casos que el agente no ha visto.
import unittest

from tiempos import minutos, total


class Evaluador(unittest.TestCase):
    def test_minutos(self):
        self.assertEqual(minutos('2:05'), 125)
        self.assertEqual(minutos('0:45'), 45)

    def test_total(self):
        self.assertEqual(total(['1:00', '0:15', '0:05']), 80)
