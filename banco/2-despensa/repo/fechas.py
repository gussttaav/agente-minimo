# Las fechas de la despensa: cuántos días faltan para una y si ya ha pasado.
from datetime import date

MARGEN = 3      # un artículo caduca pronto si le quedan 3 días o menos


def fecha(texto):
    # '2026-11-20' -> date(2026, 11, 20)
    anio, mes, dia = (int(parte) for parte in texto.split('-'))
    return date(anio, mes, dia)


def dias_hasta(caduca, hoy):
    # Los días que faltan desde hoy hasta caduca: 0 si es hoy, negativo si ya ha pasado.
    return (hoy - caduca).days


def caducado(caduca, hoy):
    # Si ya no se puede comer: caducó antes de hoy.
    return dias_hasta(caduca, hoy) < 0


def caduca_pronto(caduca, hoy, margen=MARGEN):
    # Si todavía se puede comer, pero le quedan margen días o menos.
    return 0 <= dias_hasta(caduca, hoy) <= margen
