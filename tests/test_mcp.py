"""El cliente MCP, con el servidor de verdad como subproceso y sin modelo. Lección 40 del curso."""
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import permisos
from cliente_mcp import ServidorMCP, con_servidor, herramienta
from entorno import FUNCIONES, HERRAMIENTAS, llamada

SERVIDOR = str(Path(__file__).parent.parent / "servidor_incidencias.py")


class TestMCP(unittest.TestCase):
    def setUp(self):
        self.servidor = ServidorMCP(sys.executable, SERVIDOR)
        self.addCleanup(self.servidor.cerrar)

    def correr(self, ll):
        herramientas, funciones = con_servidor(self.servidor, HERRAMIENTAS, FUNCIONES)
        with tempfile.TemporaryDirectory() as entorno:
            return permisos.ejecutar(ll, entorno, herramientas=herramientas, funciones=funciones)

    def test_lo_que_anuncia_el_servidor_es_una_herramienta_mas(self):
        herramientas, _ = con_servidor(self.servidor, HERRAMIENTAS, FUNCIONES)
        self.assertEqual([h["name"] for h in herramientas][-1], "incidencias")
        self.assertEqual(herramientas[-1]["input_schema"]["required"], ["estado"])

    def test_vuelve_una_observacion_y_un_fallo_tambien(self):
        bien = self.correr(llamada("t1", "incidencias", estado="abierta"))
        self.assertFalse(bien["is_error"])
        self.assertIn("#5 [abierta] compra.py", bien["content"])
        mal = self.correr(llamada("t2", "incidencias", estado="pendiente"))
        self.assertTrue(mal["is_error"])
        self.assertIn("abierta o cerrada", mal["content"])

    def test_sin_clase_declarada_se_deniega(self):
        with mock.patch.dict(permisos.AJENAS, clear=True):
            r = self.correr(llamada("t1", "incidencias", estado="abierta"))
        self.assertEqual(r["content"], "no se ha ejecutado: permiso denegado")

    def test_no_ofrece_lo_que_no_sabe_comprobar(self):
        suma = {"name": "suma", "description": "",
                "inputSchema": {"type": "object", "properties": {"a": {"type": "number"}}}}
        self.assertIsNone(herramienta(suma))

    def test_no_pisa_una_herramienta_del_agente(self):
        leer = {"name": "leer", "description": "", "inputSchema": {"type": "object"}}
        with mock.patch.object(self.servidor, "herramientas", return_value=[leer]):
            with self.assertRaises(ValueError):
                con_servidor(self.servidor, HERRAMIENTAS, FUNCIONES)


if __name__ == "__main__":
    unittest.main()
