import re 

# Manejo de variables predefinidas para expresiones regulares

# Funcion para traducir el listado de variables en or
def _union(caracteres):
    return "(" + "|".join(caracteres) + ")"

# Variables comunes predefinidas 
class Variables:
    digit = _union("01")

    digits = _union("0123456789")

    letter = _union("abAB")

    # A-Z (solo mayusculas)
    upper = _union([chr(c) for c in range(ord("A"), ord("Z") + 1)])

    # A-Z, a-z y 0-9
    alnum = _union(
        [chr(c) for c in range(ord("A"), ord("Z") + 1)]
        + [chr(c) for c in range(ord("a"), ord("z") + 1)]
        + [str(d) for d in range(10)]
    )

    @classmethod
    def como_dict(cls):
        return {
            nombre: valor
            for nombre, valor in vars(cls).items()
            if not nombre.startswith("_") and isinstance(valor, str)
        }


# Diccionario {nombre: expresion} que usa expandir_variables.
VARIABLES = Variables.como_dict()

_IDENTIFICADOR = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")

# Reescritura de la variable a sus forma extendida 
def expandir_variables(expresion, variables=None):
    tabla = VARIABLES if variables is None else variables

    def reemplazo(match):
        nombre = match.group(0)
        return tabla.get(nombre, nombre)

    return _IDENTIFICADOR.sub(reemplazo, expresion)

