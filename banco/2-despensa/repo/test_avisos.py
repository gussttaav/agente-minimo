import unittest
from datetime import date

from avisos import avisos
from despensa import leer_despensa

DESPENSA = '''
# nombre; cantidad; caduca
arroz; 2; 2026-12-31
leche; 1; 2026-11-07
yogur; 4; 2026-11-03
huevos; 6; 2026-11-05
'''
HOY = date(2026, 11, 5)


class TestAvisos(unittest.TestCase):
    def test_avisos(self):
        self.assertEqual(avisos(leer_despensa(DESPENSA), HOY),
                         ['tirar: yogur (caducó hace 2 días)', 'comer hoy: huevos',
                          'comer pronto: leche (quedan 2 días)'])
