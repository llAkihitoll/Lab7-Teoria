# Laboratorio 7 - Teoría de la Computación

Simplificación de gramáticas libres de contexto: eliminación de producciones-ε.

## Video

Enlace al video (no listado): _pendiente_

## Ejecución

```
python main.py gramaticas/gramatica1.txt
```

## Formato de las gramáticas

- Cada línea es una producción: `S -> 0A0 | 1B1 | BB`
- Letras mayúsculas: no terminales.
- Letras minúsculas y dígitos: terminales.
- `|` separa varias producciones del mismo no terminal.
- `ε` representa la cadena vacía.

## Estructura

- `main.py`: punto de entrada.
- `gramatica.py`: lectura del archivo y representación de la gramática.
- `gramaticas/`: gramáticas del Problema 2 usadas como entrada.
- `tokenizer.py`, `stack.py`, `shunting_yard.py`, `syntax_tree.py`, `tree_builder.py`,
  `thompson.py`, `afn.py`, `simulador.py`, `variables.py`: motor de expresiones
  regulares reutilizado del Proyecto 1 (regex → postfix → árbol → AFN → simulación).
