"""El recetario de casa: qué recetas hay y qué lleva cada una.

recetas.txt tiene una receta por línea, «Nombre: ingrediente, ingrediente.», comentarios que
empiezan por # y una línea en blanco entre secciones. Un recetario, en este proyecto, es un
diccionario {nombre: [ingrediente, ...]}, en el orden del fichero. La lista de la compra está
en compra.py.
"""
import difflib
from pathlib import Path

RECETAS = Path(__file__).with_name("recetas.txt")


def es_comentario(linea):
    """Una línea que no es una receta: un comentario."""
    return linea.lstrip().startswith("#")


def separar(receta):
    """«Tortilla: huevos, patatas, cebolla.» -> ("Tortilla", "huevos, patatas, cebolla.")"""
    if receta.count(":") != 1:
        raise ValueError("una receta tiene un solo «:», y ésta no: %r" % receta)
    nombre, lista = receta.split(":")
    return nombre.strip(), lista


def ingredientes(receta):
    """«Tortilla: Huevos, patatas, cebolla.» -> ["huevos", "patatas", "cebolla"]

    Sin el punto final y sin espacios, y en minúsculas: «Tomates» y «tomates» son el mismo
    ingrediente, y la lista de la compra no puede llevar los dos.
    """
    _, lista = separar(receta)
    lista = lista.strip().rstrip(".")
    return [i.strip() for i in lista.split(",") if i.strip()]


def leer_recetario(texto):
    """El recetario de un texto con el formato de recetas.txt."""
    recetario = {}
    for n, linea in enumerate(texto.split("\n"), 1):
        if es_comentario(linea):
            continue
        nombre, _ = separar(linea)
        if nombre in recetario:
            raise ValueError("la receta %r está dos veces (línea %d)" % (nombre, n))
        recetario[nombre] = ingredientes(linea)
    return recetario


def cargar(ruta=RECETAS):
    """El recetario del fichero ruta, por omisión el recetas.txt de esta carpeta."""
    return leer_recetario(Path(ruta).read_text(encoding="utf-8"))


def con(recetario, ingrediente):
    """Los nombres de las recetas que llevan ese ingrediente, en el orden del recetario."""
    ingrediente = ingrediente.strip().lower()
    return [nombre for nombre, lista in recetario.items() if ingrediente in lista]


def sin(recetario, prohibidos):
    """Los nombres de las recetas que no llevan ninguno de los ingredientes prohibidos.

    Para una alergia o para lo que no le gusta a alguien: sin(recetario, ["huevos", "leche"]).
    """
    prohibidos = {p.strip().lower() for p in prohibidos}
    return [nombre for nombre, lista in recetario.items() if not prohibidos & set(lista)]


def parecidas(recetario, nombre, n=3):
    """Hasta n nombres del recetario que se parecen a nombre, para sugerirlos."""
    return difflib.get_close_matches(nombre, list(recetario), n=n, cutoff=0.6)
