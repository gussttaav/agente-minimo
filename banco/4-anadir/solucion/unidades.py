# Las cantidades de las recetas, pasadas a gramos.

GRAMOS = {'g': 1, 'kg': 1000, 'cucharada': 15, 'taza': 240}


def a_gramos(cantidad, unidad):
    # (2, 'cucharada') -> 30
    if unidad not in GRAMOS:
        raise ValueError('unidad desconocida: %s' % unidad)
    return cantidad * GRAMOS[unidad]


def a_kilos(gramos):
    # 1500 -> 1.5
    return gramos / 1000
