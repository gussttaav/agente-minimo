import unittest

from unidades import a_gramos, a_kilos


class TestUnidades(unittest.TestCase):
    def test_a_gramos(self):
        self.assertEqual(a_gramos(2, 'cucharada'), 30)

    def test_unidad_desconocida(self):
        with self.assertRaises(ValueError):
            a_gramos(1, 'pizca')

    def test_a_kilos(self):
        self.assertEqual(a_kilos(1500), 1.5)
