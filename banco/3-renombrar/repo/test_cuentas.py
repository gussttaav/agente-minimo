import unittest

from cuentas import por_persona, suma_precios
from ticket import ticket


class TestCuentas(unittest.TestCase):
    def test_suma_precios(self):
        self.assertEqual(suma_precios([120, 95]), 215)

    def test_por_persona(self):
        self.assertEqual(por_persona([120, 95], 2), 108)

    def test_ticket(self):
        self.assertEqual(ticket([('pan', 120), ('leche', 95)]), 'pan 1,20 / leche 0,95 / total 2,15')
