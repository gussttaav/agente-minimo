# El total de una lista de la compra, con los precios escritos como aquí: 1,20.


def precio(articulo):
    # 'pan 1,20' -> 1.2
    return float(articulo.split()[-1])


def total(lista):
    # 'pan 1,20; leche 0,95' -> 2.15
    return round(sum(precio(a) for a in lista.split(';')), 2)
