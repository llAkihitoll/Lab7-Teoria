from variables import expandir_variables
from shunting_yard import convertir_a_postfix, mostrar_expresion
from tree_builder import construir_arbol
from thompson import construir_afn
from simulador import simular
from gramatica import ErrorGramatica, EPSILON, FLECHA, normalizar_linea

# Regex de una produccion, escrita con la sintaxis del Proyecto 1:
#   upper      -> un no terminal (A-Z)
#   ->         -> la flecha
#   alnum+|/ε  -> un cuerpo: simbolos A-Z, a-z, 0-9 o bien ε sola
#   (/|...)*   -> mas cuerpos separados por un | literal
# El / escapa | y ε para que se lean como caracteres y no como operadores.
REGEX_PRODUCCION = "upper->(alnum+|/ε)(/|(alnum+|/ε))*"

_afn_produccion = None


# Construye (una sola vez) el AFN de la regex: variables -> postfix -> arbol -> Thompson
def afn_produccion():
    global _afn_produccion
    if _afn_produccion is None:
        expresion = expandir_variables(REGEX_PRODUCCION)
        postfix, _ = convertir_a_postfix(expresion)
        raiz, _ = construir_arbol(postfix)
        _afn_produccion = construir_afn(raiz)
    return _afn_produccion


def es_produccion_valida(linea):
    return simular(afn_produccion(), normalizar_linea(linea))


# Explica por que una linea rechazada por la regex no es valida
def describir_error(linea):
    linea = normalizar_linea(linea)
    if FLECHA not in linea:
        return f"falta la flecha '{FLECHA}'"

    cabeza, lado_derecho = linea.split(FLECHA, 1)
    if cabeza == "":
        return "falta el lado izquierdo (no terminal)"
    if len(cabeza) != 1 or not ("A" <= cabeza <= "Z"):
        return f"el lado izquierdo '{cabeza}' debe ser una sola letra mayuscula"
    if lado_derecho == "":
        return "falta el lado derecho"

    cuerpos = lado_derecho.split("|")
    if "" in cuerpos:
        return f"uso incorrecto de '|': hay una produccion vacia (use {EPSILON})"

    for cuerpo in cuerpos:
        if EPSILON in cuerpo and cuerpo != EPSILON:
            return f"'{EPSILON}' debe ir sola en su produccion, se encontro '{cuerpo}'"

    no_permitidos = sorted({c for c in lado_derecho if not c.isascii() or not (c.isalnum() or c == "|")} - {EPSILON})
    if no_permitidos:
        return f"simbolos no permitidos: {' '.join(no_permitidos)}"

    return "formato invalido"


# Valida cada linea mostrando el resultado; se detiene en la primera invalida
def validar_lineas(lineas):
    print(f"Regex utilizada: {mostrar_expresion(REGEX_PRODUCCION)}")
    for numero, linea in lineas:
        if es_produccion_valida(linea):
            print(f"  Linea {numero}: {linea}  -> valida")
        else:
            print(f"  Linea {numero}: {linea}  -> INVALIDA")
            raise ErrorGramatica(
                f"La gramatica contiene un error en la linea {numero}: '{linea}'\n"
                f"Motivo: {describir_error(linea)}."
            )
