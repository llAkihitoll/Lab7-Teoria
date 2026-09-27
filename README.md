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
- `validador.py`: validación de cada producción con la regex
  `upper->(alnum+|/ε)(/|(alnum+|/ε))*`, simulada sobre un AFN construido con el
  motor del Proyecto 1. Si una línea es inválida la ejecución se detiene.
- `epsilon.py`: detección de símbolos anulables (directos e indirectos, por
  iteraciones hasta que no aparecen nuevos).
- `gramaticas/`: gramáticas del Problema 2 usadas como entrada.
  `gramatica_con_error.txt` es un ejemplo con un error para probar la validación.
- `tokenizer.py`, `stack.py`, `shunting_yard.py`, `syntax_tree.py`, `tree_builder.py`,
  `thompson.py`, `afn.py`, `simulador.py`, `variables.py`: motor de expresiones
  regulares reutilizado del Proyecto 1 (regex → postfix → árbol → AFN → simulación).
