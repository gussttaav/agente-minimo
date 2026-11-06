# La despensa de casa: qué hay, cuánto y hasta cuándo se puede comer.
#
# Cada línea de la despensa es un artículo: nombre; cantidad; fecha de caducidad, con la
# fecha como en el calendario, año-mes-día. Una línea vacía o que empieza por # no es un
# artículo.
from fechas import fecha


def articulo(linea):
    # 'arroz; 2; 2026-11-20' -> {'nombre': 'arroz', 'cantidad': 2, 'caduca': date(2026, 11, 20)}
    nombre, cantidad, caduca = (parte.strip() for parte in linea.split(';'))
    return {'nombre': nombre, 'cantidad': int(cantidad), 'caduca': fecha(caduca)}


def leer_despensa(texto):
    # Todas las líneas que son artículos, en el orden en que están.
    articulos = []
    for linea in texto.splitlines():
        linea = linea.strip()
        if linea and not linea.startswith('#'):
            articulos.append(articulo(linea))
    return articulos


def cantidad(despensa, nombre):
    # Cuántos hay de un artículo, sumando todas sus líneas: puede haber dos paquetes de arroz.
    return sum(a['cantidad'] for a in despensa if a['nombre'] == nombre)


def gastar(despensa, nombre, cuantos):
    # Quita cuantos del artículo, empezando por el que caduca antes. Devuelve la despensa
    # sin los artículos que se han acabado.
    if cantidad(despensa, nombre) < cuantos:
        raise ValueError('no hay %d de %s' % (cuantos, nombre))
    for a in sorted((a for a in despensa if a['nombre'] == nombre), key=lambda a: a['caduca']):
        quito = min(a['cantidad'], cuantos)
        a['cantidad'] -= quito
        cuantos -= quito
    return [a for a in despensa if a['cantidad'] > 0]
