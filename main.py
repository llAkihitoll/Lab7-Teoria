import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <archivo_gramatica>")
        return

    ruta = sys.argv[1]
    print(f"\nArchivo de gramatica: {ruta}")


if __name__ == "__main__":
    main()
