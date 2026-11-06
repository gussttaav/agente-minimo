import unittest

from cuentas import por_persona, importe
from ticket import ticket


class TestCuentas(unittest.TestCase):
    def test_importe(self):
        self.assertEqual(importe([120, 95]), 215)

    def test_por_persona(self):
        self.assertEqual(por_persona([120, 95], 2), 108)

    def test_ticket(self):
        self.assertEqual(ticket([('pan', 120), ('leche', 95)]), 'pan 1,20 / leche 0,95 / total 2,15')
