# Las ofertas del súper. Los precios, en céntimos.


def dos_por_uno(precio, unidades):
    # Se paga una de cada dos: (120, 3) -> 240
    return precio * (unidades - unidades // 2)


def descuento(precio, por_ciento):
    # (200, 15) -> 170
    return round(precio * (100 - por_ciento) / 100)
