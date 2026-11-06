# El ticket de la compra: una línea por artículo y el total.
from cuentas import importe


def euros(centimos):
    # 215 -> '2,15'
    return '%d,%02d' % divmod(centimos, 100)


def ticket(articulos):
    # [('pan', 120), ('leche', 95)] -> 'pan 1,20 / leche 0,95 / total 2,15'
    lineas = ['%s %s' % (nombre, euros(precio)) for nombre, precio in articulos]
    total = importe([precio for _, precio in articulos])
    return ' / '.join(lineas + ['total ' + euros(total)])
