# Laboratorio 7 - Teoría de la Computación

Simplificación de gramáticas libres de contexto: eliminación de producciones-ε.

El programa lee una gramática desde un archivo de texto, valida cada producción
con una expresión regular (simulada sobre un AFN construido con el motor del
Proyecto 1), detecta los símbolos anulables y construye una gramática
equivalente sin producciones-ε, mostrando cada paso del proceso.

## Video

Enlace al video (no listado): _pendiente_

## Requisitos

- Python 3.8 o superior.
- No se usan librerías externas (solo la biblioteca estándar).

## Ejecución

```
python main.py <archivo_gramatica>
```

Por ejemplo:

```
python main.py gramaticas/gramatica1.txt
python main.py gramaticas/gramatica2.txt
python main.py gramaticas/gramatica3.txt
python main.py gramaticas/gramatica_con_error.txt
```

## Pruebas

```
python -m unittest discover -s tests -v
```

## Formato de las gramáticas

- Cada línea es una producción: `S -> 0A0 | 1B1 | BB`
- Letras mayúsculas: no terminales.
- Letras minúsculas y dígitos: terminales.
- `|` separa varias producciones del mismo no terminal.
- `ε` representa la cadena vacía.
- El símbolo inicial es la cabeza de la primera línea.

Cada línea debe cumplir la expresión regular:

```
upper->(alnum+|/ε)(/|(alnum+|/ε))*
```

donde `upper` es una letra mayúscula, `alnum` una letra o dígito y `/` escapa
los símbolos especiales `|` y `ε`. Si alguna línea no la cumple, se indica la
línea con el error y la ejecución se detiene.

## Salida del programa

Para cada gramática el programa imprime:

1. **Validación de producciones:** cada línea marcada como válida o inválida.
2. **Gramática original.**
3. **Símbolos anulables:** iteraciones del algoritmo indicando qué símbolo se
   vuelve anulable y por qué producción (directa `A -> ε` o indirecta, cuando
   todo el cuerpo está formado por símbolos ya anulables), hasta que no aparecen
   nuevos. Luego se listan el conjunto de anulables y las producciones anulables.
4. **Eliminación de producciones-ε:** por cada producción con m apariciones
   anulables se muestran las 2^m combinaciones (`_` = símbolo quitado),
   indicando cuáles se descartan por repetidas, por quedar en ε o por ser de la
   forma `A -> A`.
5. **Gramática sin producciones-ε.** Si el símbolo inicial es anulable se
   indica que la gramática resultante genera L(G) − {ε}.

### Ejemplo con error

```
Linea 3: B -> S || A  -> INVALIDA

Error: La gramatica contiene un error en la linea 3: 'B -> S || A'
Motivo: uso incorrecto de '|': hay una produccion vacia (use ε).
Ejecucion detenida.
```

## Resultados

### Gramática 1

```
S -> 0A0 | 1B1 | BB
A -> C
B -> S | A
C -> S | ε
```

Anulables: `{S, A, B, C}`

```
S -> 0A0 | 00 | 1B1 | 11 | BB | B
A -> C
B -> S | A
C -> S
```

### Gramática 2

```
S -> aAa | bBb | ε
A -> C | a
B -> C | b
C -> CDE | ε
D -> A | B | ab
```

Anulables: `{S, A, B, C, D}`

```
S -> aAa | aa | bBb | bb
A -> C | a
B -> C | b
C -> CDE | DE | CE | E
D -> A | B | ab
```

### Gramática 3

```
S -> ASA | aB
A -> B | S
B -> b | ε
```

Anulables: `{A, B}`

```
S -> ASA | SA | AS | aB | a
A -> B | S
B -> b
```

En las gramáticas 1 y 2 el símbolo inicial `S` es anulable, por lo que
ε ∈ L(G) y las gramáticas resultantes generan L(G) − {ε}.

## Estructura

- `main.py`: punto de entrada.
- `gramatica.py`: lectura del archivo y representación de la gramática.
- `validador.py`: validación de cada producción con la regex
  `upper->(alnum+|/ε)(/|(alnum+|/ε))*`, simulada sobre un AFN construido con el
  motor del Proyecto 1. Si una línea es inválida la ejecución se detiene.
- `epsilon.py`: detección de símbolos anulables (directos e indirectos, por
  iteraciones hasta que no aparecen nuevos) y eliminación de producciones-ε:
  por cada producción con m apariciones anulables se generan las 2^m
  combinaciones de quitar o conservar cada una, descartando las repetidas,
  las que quedan en ε y las de la forma A -> A.
- `gramaticas/`: gramáticas del Problema 2 usadas como entrada.
  `gramatica_con_error.txt` es un ejemplo con un error para probar la validación.
- `tests/`: pruebas con `unittest` de lectura, validación, símbolos anulables y
  eliminación de producciones-ε.
- `tokenizer.py`, `stack.py`, `shunting_yard.py`, `syntax_tree.py`, `tree_builder.py`,
  `thompson.py`, `afn.py`, `simulador.py`, `variables.py`: motor de expresiones
  regulares reutilizado del Proyecto 1 (regex → postfix → árbol → AFN → simulación).
