import unittest

from precios import precio, total


class TestPrecios(unittest.TestCase):
    def test_precio(self):
        self.assertEqual(precio('pan 1,20'), 1.2)

    def test_total(self):
        self.assertEqual(total('pan 1,20; leche 0,95; huevos 2,10'), 4.25)
