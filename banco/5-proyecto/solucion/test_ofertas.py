import unittest

from ofertas import descuento, dos_por_uno


class TestOfertas(unittest.TestCase):
    def test_dos_por_uno(self):
        self.assertEqual(dos_por_uno(120, 3), 240)
        self.assertEqual(dos_por_uno(120, 4), 240)

    def test_descuento(self):
        self.assertEqual(descuento(200, 15), 170)
