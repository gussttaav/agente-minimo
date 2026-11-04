"""La lista de la compra de un menú, a partir del recetario de recetario.py."""
from recetario import parecidas


def menu(recetario, nombres):
    """Las recetas de un menú, comprobando que todas están en el recetario.

    menu(recetario, ["Tortilla", "Gazpacho"]) -> [("Tortilla", [...]), ("Gazpacho", [...])]
    Una receta que no está lanza KeyError, con las parecidas si las hay.
    """
    platos = []
    for nombre in nombres:
        if nombre not in recetario:
            sugerencias = parecidas(recetario, nombre)
            pista = " ¿Quizá %s?" % ", ".join(sugerencias) if sugerencias else ""
            raise KeyError("no hay ninguna receta %r.%s" % (nombre, pista))
        platos.append((nombre, recetario[nombre]))
    return platos


def despensa(lista):
    """Lo que hay en casa, de una lista escrita a mano: «pan, leche, Patatas» -> un conjunto."""
    return {i.strip().lower() for i in lista.split(",") if i.strip()}


def compra(recetario, nombres, en_casa=""):
    """Lo que hay que comprar para un menú: cada ingrediente una vez, en el orden en que
    aparece por primera vez en el menú, sin lo que ya hay en casa.

    compra(recetario, ["Tortilla"], "patatas, sal") -> ["huevos", "cebolla", "aceite"]
    """
    hay = despensa(en_casa)
    falta = []
    for _, lista in menu(recetario, nombres):
        for ingrediente in lista:
            if ingrediente not in hay and ingrediente not in falta:
                falta.append(ingrediente)
    return falta


def veces(recetario, nombres):
    """Cuántas recetas del menú usan cada ingrediente, de más a menos y, a igualdad, por orden
    alfabético: lo que conviene comprar en cantidad."""
    cuenta = {}
    for _, lista in menu(recetario, nombres):
        for ingrediente in lista:
            cuenta[ingrediente] = cuenta.get(ingrediente, 0) + 1
    return sorted(cuenta.items(), key=lambda par: (par[1], par[0]))


def lista_de_la_compra(recetario, nombres, en_casa=""):
    """La lista de la compra como texto, un ingrediente por línea, lista para imprimir."""
    falta = compra(recetario, nombres, en_casa)
    if not falta:
        return "No hace falta comprar nada."
    return "\n".join("- " + ingrediente for ingrediente in falta)
