# El evaluador de la prueba: lo que tiene que hacer el código, con casos que el agente no ha visto.
import unittest
from pathlib import Path

import cuentas
import ticket


class Evaluador(unittest.TestCase):
    def test_se_llama_importe(self):
        self.assertEqual(cuentas.importe([100, 250, 5]), 355)
        self.assertFalse(hasattr(cuentas, 'suma_precios'))

    def test_lo_que_la_usa_sigue_funcionando(self):
        self.assertEqual(cuentas.por_persona([100, 250, 5], 3), 119)
        self.assertEqual(ticket.ticket([('sal', 60)]), 'sal 0,60 / total 0,60')

    def test_no_queda_el_nombre_viejo(self):
        for f in Path('.').glob('*.py'):
            if f.name != 'evaluador.py':
                self.assertNotIn('suma_precios', f.read_text(encoding='utf-8'), f.name)
