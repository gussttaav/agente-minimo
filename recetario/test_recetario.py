import unittest

from recetario import cargar, con, ingredientes, leer_recetario, sin

TEXTO = """# Un recetario pequeño.

# Primeros
Gazpacho: Tomates, pepino, ajo, aceite.

# Segundos
Tortilla: Huevos, patatas, cebolla, aceite.
Huevos rotos: huevos, patatas, jamón, aceite.
"""


class TestRecetario(unittest.TestCase):
    def test_sin_punto_ni_espacios(self):
        self.assertEqual(ingredientes("Flan: huevos, leche , azúcar."), ["huevos", "leche", "azúcar"])

    def test_en_minusculas(self):
        self.assertEqual(ingredientes("Gazpacho: Tomates, pepino, ajo."), ["tomates", "pepino", "ajo"])

    def test_lee_las_recetas_en_orden(self):
        self.assertEqual(list(leer_recetario(TEXTO)), ["Gazpacho", "Tortilla", "Huevos rotos"])

    def test_el_fichero_de_verdad(self):
        recetario = cargar()
        self.assertEqual(len(recetario), 40)
        self.assertEqual(recetario["Tortilla"], ["huevos", "patatas", "cebolla", "aceite", "sal"])

    def test_con_y_sin(self):
        recetario = leer_recetario(TEXTO)
        self.assertEqual(con(recetario, "Huevos"), ["Tortilla", "Huevos rotos"])
        self.assertEqual(sin(recetario, ["jamón"]), ["Gazpacho", "Tortilla"])
