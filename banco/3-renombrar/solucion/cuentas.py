# Las cuentas de la compra, en céntimos: 120 es 1,20 euros.


def importe(precios):
    # [120, 95] -> 215
    return sum(precios)


def por_persona(precios, personas):
    # Lo que paga cada uno, redondeado hacia arriba al céntimo: [120, 95] entre 2 -> 108
    return -(-importe(precios) // personas)
