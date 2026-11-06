import unittest

from tiempos import minutos, total


class TestTiempos(unittest.TestCase):
    def test_minutos(self):
        self.assertEqual(minutos('1:30'), 90)

    def test_total(self):
        self.assertEqual(total(['0:20', '1:30']), 110)
