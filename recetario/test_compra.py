import unittest

from compra import compra, lista_de_la_compra, menu, veces
from recetario import leer_recetario

TEXTO = """Salmorejo: tomates, pan, aceite, ajo, sal.
Tortilla: huevos, patatas, cebolla, aceite, sal.
Huevos rotos: huevos, patatas, jamón, aceite, sal.
Flan: huevos, leche, azúcar, vainilla."""


class TestCompra(unittest.TestCase):
    def setUp(self):
        self.recetario = leer_recetario(TEXTO)

    def test_cada_ingrediente_una_vez(self):
        self.assertEqual(compra(self.recetario, ["Tortilla", "Huevos rotos"], "patatas, sal"),
                         ["huevos", "cebolla", "aceite", "jamón"])

    def test_lo_que_hay_en_casa(self):
        self.assertEqual(compra(self.recetario, ["Salmorejo"], "Tomates, ajo, aceite, sal"), ["pan"])

    def test_veces(self):
        self.assertEqual(veces(self.recetario, ["Tortilla", "Huevos rotos", "Flan"])[:3],
                         [("huevos", 3), ("aceite", 2), ("patatas", 2)])

    def test_una_receta_que_no_esta(self):
        with self.assertRaises(KeyError):
            menu(self.recetario, ["Tortila"])

    def test_lista_de_la_compra(self):
        self.assertEqual(lista_de_la_compra(self.recetario, ["Salmorejo"], "tomates, ajo, aceite"),
                         "- pan\n- sal")
