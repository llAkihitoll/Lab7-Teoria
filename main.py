import sys

from gramatica import ErrorGramatica, leer_lineas, construir_gramatica, imprimir_gramatica
from validador import validar_lineas

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


if __name__ == "__main__":
    main()
