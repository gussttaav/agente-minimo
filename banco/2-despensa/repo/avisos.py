# Los avisos de la despensa: lo que hay que tirar y lo que hay que comer pronto.
from fechas import caducado, caduca_pronto, dias_hasta


def aviso(a, hoy):
    # El aviso de un artículo, o None si no lo necesita.
    if caducado(a['caduca'], hoy):
        return 'tirar: %s (caducó hace %d días)' % (a['nombre'], -dias_hasta(a['caduca'], hoy))
    if caduca_pronto(a['caduca'], hoy):
        dias = dias_hasta(a['caduca'], hoy)
        if dias == 0:
            return 'comer hoy: %s' % a['nombre']
        return 'comer pronto: %s (quedan %d días)' % (a['nombre'], dias)
    return None


def avisos(despensa, hoy):
    # Los avisos de toda la despensa, lo más urgente primero: lo que hay que tirar, después
    # lo que caduca hoy, y después lo que caduca antes.
    con_aviso = [a for a in despensa if aviso(a, hoy) is not None]
    con_aviso.sort(key=lambda a: dias_hasta(a['caduca'], hoy))
    return [aviso(a, hoy) for a in con_aviso]
