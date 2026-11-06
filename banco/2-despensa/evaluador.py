# El evaluador de la prueba: lo que tiene que hacer el código, con casos que el agente no ha visto.
import unittest
from datetime import date

from avisos import avisos
from despensa import leer_despensa
from fechas import dias_hasta

HOY = date(2026, 3, 10)


class Evaluador(unittest.TestCase):
    def test_dias_hasta(self):
        self.assertEqual(dias_hasta(date(2026, 3, 14), HOY), 4)
        self.assertEqual(dias_hasta(date(2026, 3, 7), HOY), -3)

    def test_avisos(self):
        despensa = leer_despensa('queso; 1; 2026-03-12\npan; 1; 2026-03-07\natún; 3; 2027-05-01')
        self.assertEqual(avisos(despensa, HOY),
                         ['tirar: pan (caducó hace 3 días)', 'comer pronto: queso (quedan 2 días)'])
