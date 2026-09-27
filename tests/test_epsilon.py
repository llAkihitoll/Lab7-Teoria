import unittest

from gramatica import construir_gramatica
from epsilon import encontrar_anulables, generar_combinaciones, eliminar_epsilon


def gramatica_desde(*lineas):
    return construir_gramatica(list(enumerate(lineas, start=1)))


def texto(gramatica):
    return {cabeza: ["".join(c) for c in cuerpos] for cabeza, cuerpos in gramatica.items()}


class TestAnulables(unittest.TestCase):
    def test_anulable_directo(self):
        anulables, _ = encontrar_anulables(gramatica_desde("S -> aA", "A -> ε | a"))
        self.assertEqual(anulables, {"A"})

    def test_anulable_indirecto(self):
        gramatica = gramatica_desde("S -> a | A", "A -> BC", "B -> ε", "C -> ε")
        anulables, pasos = encontrar_anulables(gramatica)
        self.assertEqual(anulables, {"S", "A", "B", "C"})
        # B y C en la iteracion 1, A en la 2, S en la 3 y una ultima sin cambios
        self.assertEqual([[c for c, _ in nuevos] for nuevos in pasos], [["B", "C"], ["A"], ["S"], []])

    def test_produccion_con_simbolo_no_anulable(self):
        anulables, _ = encontrar_anulables(gramatica_desde("A -> BC", "B -> ε", "C -> c"))
        self.assertEqual(anulables, {"B"})

    def test_gramatica_sin_anulables(self):
        anulables, pasos = encontrar_anulables(gramatica_desde("S -> ab | T", "T -> c"))
        self.assertEqual(anulables, set())
        self.assertEqual(pasos, [[]])


class TestCombinaciones(unittest.TestCase):
    def test_sin_simbolos_anulables(self):
        self.assertEqual(generar_combinaciones(list("aBc"), set()), [("aBc", list("aBc"))])

    def test_un_simbolo_anulable(self):
        resultados = [r for _, r in generar_combinaciones(list("0A0"), {"A"})]
        self.assertEqual(resultados, [list("0A0"), list("00")])

    def test_varios_simbolos_anulables_generan_2_a_la_m(self):
        combinaciones = generar_combinaciones(list("BCD"), {"B", "C"})
        self.assertEqual(len(combinaciones), 4)
        self.assertEqual(
            sorted("".join(r) for _, r in combinaciones),
            sorted(["BCD", "CD", "BD", "D"]),
        )

    def test_apariciones_repetidas_cuentan_por_separado(self):
        combinaciones = generar_combinaciones(list("AbAcA"), {"A"})
        self.assertEqual(len(combinaciones), 8)
        self.assertIn(("_bAc_", list("bAc")), combinaciones)


class TestEliminacionEpsilon(unittest.TestCase):
    def _eliminar(self, gramatica):
        anulables, _ = encontrar_anulables(gramatica)
        nueva, _, _, _ = eliminar_epsilon(gramatica, anulables)
        return texto(nueva)

    def test_gramatica_sin_producciones_epsilon_no_cambia(self):
        gramatica = gramatica_desde("S -> ab | Tc", "T -> d")
        self.assertEqual(self._eliminar(gramatica), texto(gramatica))

    def test_evita_duplicados_y_descarta_epsilon(self):
        resultado = self._eliminar(gramatica_desde("S -> BB | a", "B -> b | ε"))
        self.assertEqual(resultado, {"S": ["BB", "B", "a"], "B": ["b"]})

    def test_descarta_produccion_a_si_misma(self):
        resultado = self._eliminar(gramatica_desde("S -> SA | a", "A -> ε | a"))
        self.assertEqual(resultado, {"S": ["SA", "a"], "A": ["a"]})

    def test_gramatica_1(self):
        gramatica = gramatica_desde("S -> 0A0 | 1B1 | BB", "A -> C", "B -> S | A", "C -> S | ε")
        self.assertEqual(self._eliminar(gramatica), {
            "S": ["0A0", "00", "1B1", "11", "BB", "B"],
            "A": ["C"],
            "B": ["S", "A"],
            "C": ["S"],
        })

    def test_gramatica_2(self):
        gramatica = gramatica_desde(
            "S -> aAa | bBb | ε", "A -> C | a", "B -> C | b", "C -> CDE | ε", "D -> A | B | ab"
        )
        self.assertEqual(self._eliminar(gramatica), {
            "S": ["aAa", "aa", "bBb", "bb"],
            "A": ["C", "a"],
            "B": ["C", "b"],
            "C": ["CDE", "DE", "CE", "E"],
            "D": ["A", "B", "ab"],
        })

    def test_gramatica_3(self):
        gramatica = gramatica_desde("S -> ASA | aB", "A -> B | S", "B -> b | ε")
        self.assertEqual(self._eliminar(gramatica), {
            "S": ["ASA", "SA", "AS", "aB", "a"],
            "A": ["B", "S"],
            "B": ["b"],
        })


if __name__ == "__main__":
    unittest.main()
