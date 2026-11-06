import unittest
from datetime import date

from despensa import articulo, cantidad, gastar, leer_despensa


class TestDespensa(unittest.TestCase):
    def test_articulo(self):
        self.assertEqual(articulo('arroz; 2; 2026-11-20'),
                         {'nombre': 'arroz', 'cantidad': 2, 'caduca': date(2026, 11, 20)})

    def test_cantidad(self):
        despensa = leer_despensa('arroz; 2; 2026-11-20\narroz; 1; 2027-01-10\nsal; 1; 2030-01-01')
        self.assertEqual(cantidad(despensa, 'arroz'), 3)

    def test_gastar_empieza_por_lo_que_caduca_antes(self):
        despensa = leer_despensa('arroz; 2; 2027-01-10\narroz; 1; 2026-11-20')
        self.assertEqual(gastar(despensa, 'arroz', 2),
                         [{'nombre': 'arroz', 'cantidad': 1, 'caduca': date(2027, 1, 10)}])
