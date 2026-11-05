"""El contrato del subagente, con los dos modelos fijados por un guion. Lección 38 del curso.

Como en la batería de la lección 31, las observaciones están escritas a mano, a partir del
contrato de cada herramienta, del de ejecutar y del de delegar.
"""
import tempfile
import unittest

from agente import SISTEMA as PRINCIPAL, agente, inicio
from entorno import ENTORNO, error, llamada, resultado, texto
from guionizado import ModeloGuionizado, guion_de
from herramientas.escribir import escribir
from subagente import REGLA, SISTEMA, TOPE
from tests.test_agente import ficheros

PEDIDO = "¿Qué me falta para la tortilla?"
ENCARGO = "¿Qué ingredientes lleva la receta de tortilla? Las recetas están en recetas/."
DELEGA = [llamada("t1", "delegar", encargo=ENCARGO)]
FINAL = [texto("Te faltan huevos y cebolla.")]


def correr(sub_respuestas, sub_observaciones, devuelve):
    """Un pedido con una delegación: (motivo, texto, M del principal, entorno, preguntas)."""
    principal = ModeloGuionizado(guion_de(inicio(PEDIDO, sistema=PRINCIPAL + "\n" + REGLA),
                                          [DELEGA, FINAL], [[devuelve], None]))
    sub = ModeloGuionizado(guion_de([("sistema", SISTEMA), ("usuario", ENCARGO)],
                                    sub_respuestas, sub_observaciones))
    preguntas = []
    def usuario(ll):
        preguntas.append(ll["id"])
        return True
    with tempfile.TemporaryDirectory() as entorno:
        for ruta, contenido in ENTORNO.items():
            escribir(entorno, ruta, contenido)
        motivo, final, M = agente(principal, PEDIDO, entorno, usuario=usuario, delegar=sub)
        despues = ficheros(entorno)
    assert principal.turno == 2 and sub.turno == len(sub.guion), "los guiones no se han acabado"
    return motivo, final, M, despues, preguntas


class TestSubagente(unittest.TestCase):
    def test_empieza_de_cero_y_solo_vuelve_su_texto(self):
        respuestas = [[llamada("s1", "leer", ruta="recetas/tortilla.txt")],
                      [texto("Huevos, patatas y cebolla (recetas/tortilla.txt).")]]
        observaciones = [[resultado("s1", "Tortilla: huevos, patatas, cebolla.")], None]
        motivo, final, M, _, _ = correr(respuestas, observaciones, resultado(
            "t1", "Huevos, patatas y cebolla (recetas/tortilla.txt)."))
        self.assertEqual((motivo, final), ("fin", "Te faltan huevos y cebolla."))
        self.assertEqual(len(M), 5)              # la lectura del subagente no está en M
        self.assertNotIn("s1", str(M))

    def test_solo_lee_y_no_pregunta(self):
        respuestas = [[llamada("s1", "escribir", ruta="notas.txt", contenido="Tortilla."),
                       llamada("s2", "delegar", encargo=ENCARGO),
                       llamada("s3", "leer", ruta="/etc/passwd")],
                      [texto("No he podido leer la receta.")]]
        observaciones = [[error("s1", "no se ha ejecutado: no hay ninguna herramienta 'escribir'"),
                          error("s2", "no se ha ejecutado: no hay ninguna herramienta 'delegar'"),
                          error("s3", "no se ha ejecutado: /etc/passwd está fuera de la carpeta "
                                      "de trabajo")],
                         None]
        _, _, _, despues, preguntas = correr(respuestas, observaciones,
                                             resultado("t1", "No he podido leer la receta."))
        self.assertEqual(despues, ENTORNO)
        self.assertEqual(preguntas, [])

    def test_su_tope_es_un_error_para_el_agente_principal(self):
        respuestas = [[llamada("s%d" % i, "leer", ruta="recetas")] for i in range(1, TOPE + 1)]
        observaciones = [[resultado("s%d" % i, "recetas/gazpacho.txt\nrecetas/tortilla.txt")]
                         for i in range(1, TOPE + 1)]
        _, _, M, _, _ = correr(respuestas, observaciones, error(
            "t1", "el subagente ha llegado a su tope de %d turnos sin contestar" % TOPE))
        self.assertTrue(M[-2][1][0]["is_error"])


if __name__ == "__main__":
    unittest.main()
