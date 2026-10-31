import unittest

from compra import falta, ingredientes


class TestCompra(unittest.TestCase):
    def test_ingredientes(self):
        self.assertEqual(ingredientes("Gazpacho: tomates, pepino, ajo."), ["tomates", "pepino", "ajo"])

    def test_falta(self):
        self.assertEqual(falta("pan, leche, patatas", "Tortilla: huevos, patatas, cebolla."),
                         ["huevos", "cebolla"])
