"""Las cinco herramientas del agente, una por fichero. Lección 34 del curso.

Cada fichero tiene tres partes, para tres lectores: HERRAMIENTA, lo que lee el modelo; CLASE,
lo que lee el permiso; y la función, lo que ejecuta el harness sobre el entorno, que es una
carpeta de tu disco.
"""
from herramientas import buscar, editar, ejecutar, escribir, leer

MODULOS = [leer, buscar, editar, escribir, ejecutar]
HERRAMIENTAS = [m.HERRAMIENTA for m in MODULOS]
CLASES = {m.HERRAMIENTA["name"]: m.CLASE for m in MODULOS}
RUTAS = {m.HERRAMIENTA["name"]: m.RUTAS for m in MODULOS}       # lección 37
FUNCIONES = {"leer": leer.leer, "buscar": buscar.buscar, "editar": editar.editar,
             "escribir": escribir.escribir, "ejecutar": ejecutar.ejecutar}
