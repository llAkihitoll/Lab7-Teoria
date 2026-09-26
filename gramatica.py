# Representacion de una gramatica:
#   diccionario {no_terminal: [cuerpo1, cuerpo2, ...]}
#   cada cuerpo es una lista de simbolos, por ejemplo S -> 0A0 queda como ["0", "A", "0"]
#   la produccion epsilon se guarda como el cuerpo vacio []
#   el simbolo inicial es el primer no terminal del archivo

EPSILON = "ε"
FLECHA = "->"


class ErrorGramatica(Exception):
    pass


# Lee el archivo y devuelve [(numero_de_linea, texto)] ignorando lineas vacias
def leer_lineas(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        raise ErrorGramatica(f"No se encontro el archivo '{ruta}'.")

    resultado = [
        (numero, linea.strip())
        for numero, linea in enumerate(lineas, start=1)
        if linea.strip() != ""
    ]

    if not resultado:
        raise ErrorGramatica(f"El archivo '{ruta}' esta vacio.")

    return resultado


# Quita los espacios y acepta tambien la flecha →
def normalizar_linea(linea):
    return "".join(linea.replace("→", FLECHA).split())


# Separa una linea en su no terminal y la lista de cuerpos
def interpretar_linea(linea):
    linea = normalizar_linea(linea)
    if FLECHA not in linea:
        raise ErrorGramatica(f"La linea '{linea}' no contiene '{FLECHA}'.")

    cabeza, lado_derecho = linea.split(FLECHA, 1)
    cuerpos = []
    for texto in lado_derecho.split("|"):
        cuerpos.append([] if texto == EPSILON else list(texto))

    return cabeza, cuerpos


# Construye la gramatica juntando las lineas que tengan el mismo no terminal
def construir_gramatica(lineas):
    gramatica = {}
    for _, linea in lineas:
        cabeza, cuerpos = interpretar_linea(linea)
        producciones = gramatica.setdefault(cabeza, [])
        for cuerpo in cuerpos:
            if cuerpo not in producciones:
                producciones.append(cuerpo)

    return gramatica


def cargar_gramatica(ruta):
    return construir_gramatica(leer_lineas(ruta))


def simbolo_inicial(gramatica):
    return next(iter(gramatica))


def es_no_terminal(simbolo):
    return simbolo.isupper()


def formatear_cuerpo(cuerpo):
    return EPSILON if not cuerpo else "".join(cuerpo)


def formatear_produccion(cabeza, cuerpos):
    return f"{cabeza} -> " + " | ".join(formatear_cuerpo(c) for c in cuerpos)


def imprimir_gramatica(gramatica):
    for cabeza, cuerpos in gramatica.items():
        print(f"  {formatear_produccion(cabeza, cuerpos)}")
