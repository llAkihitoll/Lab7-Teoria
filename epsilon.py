from gramatica import formatear_cuerpo


# Un no terminal A es anulable si tiene una produccion A -> X1 X2 ... Xn
# donde todos los Xi ya son anulables. Con el cuerpo vacio (A -> ε) esto
# se cumple directamente; los casos indirectos aparecen en iteraciones siguientes.
# Se repite hasta que una iteracion no agregue ningun simbolo nuevo.
def encontrar_anulables(gramatica):
    anulables = set()
    pasos = []

    while True:
        previos = set(anulables)
        nuevos = []
        for cabeza, cuerpos in gramatica.items():
            if cabeza in previos:
                continue
            for cuerpo in cuerpos:
                if all(simbolo in previos for simbolo in cuerpo):
                    anulables.add(cabeza)
                    nuevos.append((cabeza, cuerpo))
                    break

        pasos.append(nuevos)
        if not nuevos:
            return anulables, pasos


# Producciones cuyo cuerpo completo puede derivar ε
def producciones_anulables(gramatica, anulables):
    return [
        (cabeza, cuerpo)
        for cabeza, cuerpos in gramatica.items()
        for cuerpo in cuerpos
        if all(simbolo in anulables for simbolo in cuerpo)
    ]


def imprimir_pasos_anulables(pasos):
    for numero, nuevos in enumerate(pasos, start=1):
        print(f"\nIteracion {numero}:")
        if not nuevos:
            print("  No se encontraron nuevos simbolos anulables. Fin.")
        for cabeza, cuerpo in nuevos:
            if not cuerpo:
                motivo = "produccion epsilon directa"
            else:
                simbolos = list(dict.fromkeys(cuerpo))
                verbo = "es anulable" if len(simbolos) == 1 else "son anulables"
                motivo = f"{', '.join(simbolos)} ya {verbo}"
            print(f"  {cabeza} es anulable por {cabeza} -> {formatear_cuerpo(cuerpo)}  ({motivo})")


def ordenar_como_gramatica(simbolos, gramatica):
    return [cabeza for cabeza in gramatica if cabeza in simbolos]


# Todas las formas de quitar o conservar cada aparicion anulable del cuerpo.
# Si hay m apariciones anulables se generan 2^m combinaciones: el bit i de
# 'mascara' indica si se quita (1) o se conserva (0) la i-esima aparicion.
# Devuelve [(patron, resultado)] donde patron marca con _ lo que se quito.
def generar_combinaciones(cuerpo, anulables):
    posiciones = [i for i, simbolo in enumerate(cuerpo) if simbolo in anulables]
    combinaciones = []

    for mascara in range(2 ** len(posiciones)):
        quitadas = {posiciones[i] for i in range(len(posiciones)) if mascara & (1 << i)}
        patron = "".join("_" if i in quitadas else s for i, s in enumerate(cuerpo))
        resultado = [s for i, s in enumerate(cuerpo) if i not in quitadas]
        combinaciones.append((patron, resultado))

    return combinaciones


# Construye la gramatica sin producciones epsilon.
# Cada combinacion queda con un estado que explica que se hizo con ella:
#   "agregada"  -> pasa a la nueva gramatica
#   "repetida"  -> ya existia en ese no terminal
#   "vacia"     -> quedo ε, se descarta
#   "trivial"   -> quedo A -> A, se descarta porque no aporta nada
def eliminar_epsilon(gramatica, anulables):
    nueva = {}
    pasos = []
    eliminadas = []

    for cabeza, cuerpos in gramatica.items():
        producciones = nueva.setdefault(cabeza, [])
        for cuerpo in cuerpos:
            if not cuerpo:
                eliminadas.append(cabeza)
                continue

            detalle = []
            for patron, resultado in generar_combinaciones(cuerpo, anulables):
                if not resultado:
                    estado = "vacia"
                elif resultado == [cabeza]:
                    estado = "trivial"
                elif resultado in producciones:
                    estado = "repetida"
                else:
                    estado = "agregada"
                    producciones.append(resultado)
                detalle.append((patron, resultado, estado))

            anulables_en_cuerpo = [s for s in cuerpo if s in anulables]
            pasos.append((cabeza, cuerpo, anulables_en_cuerpo, detalle))

    sin_producciones = [cabeza for cabeza, cuerpos in nueva.items() if not cuerpos]
    for cabeza in sin_producciones:
        del nueva[cabeza]

    return nueva, pasos, eliminadas, sin_producciones


_DESCRIPCION_ESTADO = {
    "agregada": "",
    "repetida": "(repetida, se ignora)",
    "vacia": "(queda ε, se descarta)",
    "trivial": "(produccion {0} -> {0}, se descarta)",
}


def imprimir_pasos_eliminacion(pasos):
    for cabeza, cuerpo, anulables_en_cuerpo, detalle in pasos:
        print(f"\nProcesando: {cabeza} -> {formatear_cuerpo(cuerpo)}")
        if not anulables_en_cuerpo:
            print("  Sin simbolos anulables: se conserva igual.")
            continue

        m = len(anulables_en_cuerpo)
        print(f"  Apariciones anulables: {', '.join(anulables_en_cuerpo)}  (m = {m}, 2^{m} = {2 ** m} combinaciones)")
        print("  Combinaciones (_ = simbolo quitado):")
        for patron, resultado, estado in detalle:
            linea = f"    {patron:<{len(cuerpo)}}  ->  {cabeza} -> {formatear_cuerpo(resultado)}"
            print(f"{linea}  {_DESCRIPCION_ESTADO[estado].format(cabeza)}".rstrip())
