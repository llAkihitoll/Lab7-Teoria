import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from gramatica import ErrorGramatica, leer_lineas, construir_gramatica
from validador import es_produccion_valida, describir_error, validar_lineas


class TestValidacion(unittest.TestCase):
    def test_produccion_valida(self):
        self.assertTrue(es_produccion_valida("A -> C"))
        self.assertTrue(es_produccion_valida("A → C"))

    def test_varias_producciones_en_una_linea(self):
        self.assertTrue(es_produccion_valida("S -> 0A0 | 1B1 | BB"))
        self.assertTrue(es_produccion_valida("S->ASA|aB"))

    def test_produccion_con_epsilon(self):
        self.assertTrue(es_produccion_valida("C -> S | ε"))
        self.assertTrue(es_produccion_valida("B -> ε"))

    def test_producciones_invalidas(self):
        invalidas = [
            "S -> ",
            "-> AB",
            "s -> a",
            "SA -> b",
            "S => a",
            "S -> A || B",
            "S -> A |",
            "S -> aεb",
            "S -> a+b",
        ]
        for linea in invalidas:
            with self.subTest(linea=linea):
                self.assertFalse(es_produccion_valida(linea))

    def test_motivos_de_error(self):
        self.assertIn("lado izquierdo", describir_error("-> AB"))
        self.assertIn("lado derecho", describir_error("S -> "))
        self.assertIn("'|'", describir_error("S -> A || B"))
        self.assertIn("ε", describir_error("S -> aεb"))
        self.assertIn("no permitidos", describir_error("S -> a+b"))
        self.assertIn("flecha", describir_error("S => a"))

    def test_validar_lineas_se_detiene_en_la_linea_invalida(self):
        lineas = [(1, "S -> AB"), (2, "A -> a || b"), (3, "B -> b")]
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(ErrorGramatica) as contexto:
                validar_lineas(lineas)
        self.assertIn("linea 2", str(contexto.exception))


class TestLectura(unittest.TestCase):
    def _archivo(self, contenido):
        descriptor, ruta = tempfile.mkstemp(suffix=".txt")
        with os.fdopen(descriptor, "w", encoding="utf-8") as archivo:
            archivo.write(contenido)
        self.addCleanup(os.remove, ruta)
        return ruta

    def test_archivo_inexistente(self):
        with self.assertRaises(ErrorGramatica):
            leer_lineas("no_existe.txt")

    def test_archivo_vacio(self):
        with self.assertRaises(ErrorGramatica):
            leer_lineas(self._archivo("\n   \n"))

    def test_lectura_y_representacion(self):
        lineas = leer_lineas(self._archivo("S -> 0A0 | ε\n\nA -> a\nS -> 0A0 | b\n"))
        self.assertEqual(lineas[1], (3, "A -> a"))

        gramatica = construir_gramatica(lineas)
        self.assertEqual(gramatica, {
            "S": [["0", "A", "0"], [], ["b"]],
            "A": [["a"]],
        })


if __name__ == "__main__":
    unittest.main()
