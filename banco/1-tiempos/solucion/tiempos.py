# Los tiempos de las recetas: '1:30' es una hora y media.


def minutos(tiempo):
    # '1:30' -> 90
    horas, resto = tiempo.split(':')
    return int(horas) * 60 + int(resto)


def total(tiempos):
    # ['0:20', '1:30'] -> 110
    return sum(minutos(t) for t in tiempos)
