import sys

from gramatica import (
    ErrorGramatica,
    leer_lineas,
    construir_gramatica,
    imprimir_gramatica,
    formatear_cuerpo,
    simbolo_inicial,
)
from validador import validar_lineas
from epsilon import (
    encontrar_anulables,
    producciones_anulables,
    imprimir_pasos_anulables,
    ordenar_como_gramatica,
    eliminar_epsilon,
    imprimir_pasos_eliminacion,
)

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def titulo(texto):
    print(f"\n{'='*44}")
    print(texto)
    print(f"{'='*44}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_gramatica>")
        return

    ruta = sys.argv[1]
    print(f"\nArchivo de gramatica: {ruta}")

    try:
        lineas = leer_lineas(ruta)
        titulo("VALIDACION DE PRODUCCIONES")
        validar_lineas(lineas)
        gramatica = construir_gramatica(lineas)
    except ErrorGramatica as error:
        print(f"\nError: {error}")
        print("Ejecucion detenida.")
        sys.exit(1)

    print("\nTodas las producciones son validas.")

    titulo("GRAMATICA ORIGINAL")
    imprimir_gramatica(gramatica)

    titulo("SIMBOLOS ANULABLES")
    anulables, pasos = encontrar_anulables(gramatica)
    imprimir_pasos_anulables(pasos)

    lista = ordenar_como_gramatica(anulables, gramatica)
    print(f"\nSimbolos anulables: {{{', '.join(lista)}}}" if lista else "\nNo hay simbolos anulables.")

    print("\nProducciones anulables:")
    producciones = producciones_anulables(gramatica, anulables)
    if not producciones:
        print("  (ninguna)")
    for cabeza, cuerpo in producciones:
        print(f"  {cabeza} -> {formatear_cuerpo(cuerpo)}")

    titulo("ELIMINACION DE PRODUCCIONES EPSILON")
    nueva, pasos, eliminadas, sin_producciones = eliminar_epsilon(gramatica, anulables)
    imprimir_pasos_eliminacion(pasos)

    print("\nProducciones epsilon eliminadas:")
    if not eliminadas:
        print("  (ninguna)")
    for cabeza in eliminadas:
        print(f"  {cabeza} -> ε")
    for cabeza in sin_producciones:
        print(f"\nAviso: {cabeza} solo producia ε, queda sin producciones (es un simbolo inutil).")

    titulo("GRAMATICA SIN PRODUCCIONES EPSILON")
    imprimir_gramatica(nueva)

    inicial = simbolo_inicial(gramatica)
    if inicial in anulables:
        print(f"\nNota: {inicial} es anulable, por lo que ε pertenece a L(G).")
        print("La gramatica resultante genera L(G) - {ε}.")


if __name__ == "__main__":
    main()
