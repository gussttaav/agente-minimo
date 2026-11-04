"""El contrato de la compactación, sin servidor. Lección 36 del curso."""
import unittest

from agente import inicio
from compactar import INSTRUCCION, UMBRAL, compactar
from entorno import llamada, resultado, texto


class Contado:
    """Un modelo que contó n tokens en la última petición y que apunta lo que le piden."""
    def __init__(self, n, respuesta):
        self.usage, self.respuesta, self.pedidas = {"input_tokens": n, "output_tokens": 0}, respuesta, []

    def __call__(self, mensajes, herramientas=()):
        self.pedidas.append(mensajes)
        return self.respuesta


def con_turnos(n):
    """M justo después de la respuesta del turno n: su llamada todavía no tiene observación."""
    M = inicio("Arregla recetario.py.")
    for i in range(1, n + 1):
        M.append(("asistente", [llamada("t%d" % i, "leer", ruta="f%d.py" % i)]))
        M += [("usuario", [resultado("t%d" % i, "el fichero %d" % i)])] if i < n else []
    return M


class TestCompactar(unittest.TestCase):
    def test_por_debajo_del_umbral_no_cambia_nada(self):
        M, modelo = con_turnos(4), Contado(UMBRAL, [texto("Resumen.")])
        self.assertIs(compactar(modelo, M), M)
        self.assertEqual(modelo.pedidas, [])

    def test_el_inicio_un_resumen_y_los_turnos_recientes(self):
        M, modelo = con_turnos(4), Contado(UMBRAL + 1, [texto("He leído f1.py y f2.py.")])
        nuevo = compactar(modelo, M)
        self.assertEqual(modelo.pedidas, [M[:-3] + [("usuario", INSTRUCCION)]])
        self.assertEqual(nuevo[:2], M[:2])                     # el prompt de sistema y el pedido
        self.assertTrue(nuevo[2][1].endswith("He leído f1.py y f2.py."))
        self.assertEqual(nuevo[3:], M[-3:])                    # los turnos 3 y 4, tal cual

    def test_ninguna_llamada_pierde_su_observacion(self):
        nuevo = compactar(Contado(UMBRAL + 1, [texto("Resumen.")]), con_turnos(5))
        bloques = [b for _, c in nuevo if isinstance(c, list) for b in c]
        self.assertEqual([b["id"] for b in bloques if b["type"] == "tool_use"], ["t4", "t5"])
        self.assertEqual([b["tool_use_id"] for b in bloques if b["type"] == "tool_result"], ["t4"])

    def test_sin_turnos_viejos_o_sin_resumen_no_cambia_nada(self):
        M = con_turnos(2)
        self.assertIs(compactar(Contado(UMBRAL + 1, [texto("Resumen.")]), M), M)
        M = con_turnos(4)
        self.assertIs(compactar(Contado(UMBRAL + 1, [llamada("t9", "leer", ruta="f1.py")]), M), M)


if __name__ == "__main__":
    unittest.main()
