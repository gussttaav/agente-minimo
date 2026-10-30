"""El adaptador, sin servidor: la traducción de M y la respuesta cortada. Lección 33 del curso."""
import unittest
from unittest import mock

import api
from agente import SISTEMA, inicio
from entorno import HERRAMIENTAS, llamada, resultado


class TestAdaptador(unittest.TestCase):
    def test_la_traduccion(self):
        r = [llamada("t1", "leer", ruta="lista.txt")]
        M = inicio("¿Qué hay en lista.txt?") + [("asistente", r), ("usuario", [resultado("t1", "pan")])]
        p = api.peticion("local", 1024, M, HERRAMIENTAS)
        self.assertEqual(p["system"], SISTEMA)
        self.assertEqual([m["role"] for m in p["messages"]], ["user", "assistant", "user"])
        self.assertEqual([m["content"] for m in p["messages"]], [c for _, c in M[1:]])
        self.assertEqual(p["tools"], HERRAMIENTAS)

    def test_la_respuesta_cortada(self):
        cortada = {"content": [{"type": "text", "text": "pan, le"}], "stop_reason": "max_tokens",
                   "usage": {"input_tokens": 453, "output_tokens": 1024}}
        with mock.patch("api.enviar", return_value=cortada):
            with self.assertRaises(RuntimeError):
                api.ModeloAPI()(inicio("¿Qué hay en lista.txt?"), HERRAMIENTAS)


if __name__ == "__main__":
    unittest.main()
