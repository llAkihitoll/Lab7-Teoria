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
