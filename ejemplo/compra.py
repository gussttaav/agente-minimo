"""Lo que falta comprar para una receta."""


def ingredientes(receta):
    """«Tortilla: huevos, patatas, cebolla.» -> ["huevos", "patatas", "cebolla"]"""
    nombre, lista = receta.split(":")
    return [i.strip() for i in lista.split(",")]


def falta(lista, receta):
    """Los ingredientes de la receta que no están en la lista de la compra."""
    tengo = [i.strip() for i in lista.split(",")]
    return [i for i in ingredientes(receta) if i not in tengo]
