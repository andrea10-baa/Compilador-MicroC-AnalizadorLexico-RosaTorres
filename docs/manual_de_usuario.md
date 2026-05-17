# Manual de Usuario — Analizador Léxico MicroC

**Versión:** 3.0  
**Autor:** Rosa Andrea Fernanda Torres Del Aguila  
**Carné:** 202425516  
**Curso:** Autómatas y Lenguajes — Universidad Mesoamericana 2026  
**Catedrático:** Ing. Baudilio Boteo

---

## ¿Qué es el Analizador Léxico MicroC?

El **Analizador Léxico MicroC** es una aplicación de escritorio que analiza código escrito en el lenguaje MicroC (basado en C/C++). Identifica cada token del código e indica si las cadenas pertenecen o no al lenguaje MicroC.

Incluye además un módulo de **Autómatas AFD y AFND** que permite ingresar expresiones regulares, determinar si corresponden a un autómata determinista o no determinista, y validar cadenas de entrada.

---

## Requisitos del Sistema

- Sistema operativo: Windows 10/11
- Python 3.8 o superior instalado
- No requiere instalación de librerías adicionales (usa solo `tkinter` y `re`, incluidas en Python estándar)

---

## Cómo Ejecutar la Aplicación

1. Abrir una terminal (PowerShell o CMD)
2. Navegar a la carpeta del proyecto:

```
cd ruta\del\proyecto
```

3. Ejecutar el archivo principal:

```
python compilador.py
```

> En Linux, si `tkinter` no está instalado: `sudo apt-get install python3-tk`

---

## Interfaz de la Aplicación

La aplicación tiene dos paneles principales:

| Panel | Descripción |
|---|---|
| Panel izquierdo | Editor de código MicroC con numeración de líneas |
| Panel derecho | Resultados del análisis léxico (tabla de tokens) |
| Barra inferior | Muestra el modo actual y el archivo abierto |

---

## Botones y Funciones

| Botón | Atajo | Función |
|---|---|---|
| Nuevo | `Ctrl+N` | Crea un nuevo archivo en modo edición |
| Abrir | `Ctrl+A` | Carga un archivo `.c` existente |
| Guardar | `Ctrl+G` | Guarda el archivo con extensión `.c` |
| Editar | — | Habilita la edición del archivo abierto |
| Compilar | `F5` | Ejecuta el análisis léxico |
| Autómatas | `F6` | Abre el módulo de análisis AFD y AFND |
| Salir | — | Cierra la aplicación |

---

## Cómo Usar el Analizador Léxico

### Paso 1 — Ingresar código

- Haz clic en **Nuevo** para escribir código directamente, o
- Haz clic en **Abrir** para cargar un archivo `.c` existente

### Paso 2 — Ejecutar el análisis

Presiona el botón **Compilar** o la tecla `F5`

### Paso 3 — Ver resultados

El panel derecho mostrará el resumen y la tabla de tokens:

```
  Código analizado correctamente.

  Líneas de código :  8
  Total de tokens  : 28

  RESUMEN POR TIPO DE TOKEN
  --------------------------------------------------
  Palabra Reservada          6
  Identificador              2
  Entero                     2
  Delimitador               10
  ...

  TOKENS ENCONTRADOS
  ------------------------------------------------------------
  TIPO                   LEXEMA              LIN    TOKEN
  ---------------------  ----------------    ----   ------
  Preprocesador          #include <std...      1      205
  Palabra Reservada      int                   3       17
  Palabra Reservada      main                  3       60
  Delimitador            (                     3       92
  ...

  Análisis léxico: EXITOSO
```

---

## Tokens Reconocidos

| Token | Descripción | Ejemplos válidos | Ejemplos inválidos |
|---|---|---|---|
| Palabra Reservada | Palabras del lenguaje C/C++ | `int` `if` `while` `float` | `Int` `IF` `While` |
| Identificador | Nombres de variables o funciones | `x` `total` `var1` `_aux` | `1var` `-abc` `@val` |
| Entero | Números enteros literales | `0` `42` `100` | `-5` `3.` |
| Real | Números decimales o notación científica | `3.14` `1.0` `2.5e10` | `3.` `.14` |
| Op Aritmético | Operadores matemáticos | `+` `-` `*` `/` `%` | `**` |
| Op Relacional | Comparaciones entre valores | `==` `!=` `<` `>` `<=` `>=` | `=>` `=<` |
| Op Asignación | Asignación y asignación compuesta | `=` `+=` `-=` `*=` `/=` `%=` | `:=` |
| Op Incremento | Incremento y decremento | `++` `--` | |
| Op Lógico | Operadores lógicos booleanos | `&&` `\|\|` `!` | |
| Delimitador | Separadores y agrupadores | `(` `)` `{` `}` `;` `,` | |
| Preprocesador | Directiva completa de preprocesador | `#include <stdio.h>` `#define N 10` | |
| Comentario Sl | Comentario de una línea | `// texto` | `/ texto` |
| Comentario Ml | Comentario de bloque multilínea | `/* texto */` | `/* sin cerrar` |
| Carácter | Literal de un solo carácter | `'A'` `'\n'` `'0'` | |
| Cadena | Literal de texto entre comillas dobles | `"hola mundo"` | `'hola mundo'` |

---

## Tabla de Números de Token

### Palabras Reservadas (Tokens 1–64)

| Rango | Categoría | Ejemplos |
|---|---|---|
| 1–33 | Palabras reservadas C/C++ | `auto` `break` `char` `const` `do` `double` `else` `float` `for` `if` `int` `long` `return` `short` `static` `struct` `switch` `void` `while` `bool` ... |
| 34–39 | Directivas de preprocesador | `include` `define` `ifdef` `ifndef` `endif` `undef` |
| 40–49 | Funciones `stdio.h` | `printf` `scanf` `fprintf` `fopen` `fclose` `fgets` `fputs` ... |
| 50–59 | Funciones `stdlib.h` | `malloc` `free` `exit` `atoi` `rand` `srand` `calloc` `realloc` ... |
| 60–64 | Generales | `main` `null` `NULL` `true` `false` |

### Símbolos y Operadores (Tokens 70–109)

| Rango | Categoría | Símbolos |
|---|---|---|
| 70–74 | Aritméticos | `+` `-` `*` `/` `%` |
| 75–82 | Asignación / Inc / Dec | `=` `+=` `-=` `*=` `/=` `%=` `++` `--` |
| 83–88 | Relacionales | `==` `!=` `<` `>` `<=` `>=` |
| 89–91 | Lógicos | `&&` `\|\|` `!` |
| 92–97 | Agrupación | `(` `)` `{` `}` `[` `]` |
| 98–107 | Misceláneos | `;` `,` `.` `:` `&` `\|` `^` `~` `<<` `>>` |
| 108–109 | Generales | `#` `?` |

### Tokens Especiales

| Número | Tipo | Descripción |
|---|---|---|
| `200` | `ENTERO` | Número entero literal |
| `201` | `REAL` | Número real o flotante |
| `202` | `CADENA` | Literal de texto entre comillas dobles |
| `203` | `COMENTARIO_SL` | Comentario de línea `// ...` |
| `204` | `COMENTARIO_ML` | Comentario multilínea `/* ... */` |
| `205` | `PREPROCESADOR` | Directiva `#include`, `#define`, etc. |
| `206` | `CARACTER` | Literal de carácter `'x'` |
| `300` | `IDENTIFICADOR` | Nombre definido por el usuario |
| `-1` | `DESCONOCIDO` | Símbolo no reconocido — **error léxico** |

---

## Interpretación de Resultados

### Código válido

La barra inferior se pone **verde** y muestra:

```
Análisis léxico exitoso
```

### Código con errores

La barra inferior se pone **roja** y muestra:

```
N error(es) léxico(s)
```

En el panel de resultados aparece la sección de errores:

```
  TOKENS NO RECONOCIDOS (ERRORES)
  --------------------------------------------------
  Línea 3: símbolo desconocido '@'  →  Token: -1
```

---

## Módulo de Autómatas AFD y AFND

Accedé desde el botón **Autómatas** o presionando `F6`.

### ¿Qué hace?

Permite ingresar una expresión regular, determinar si el autómata que representa es **determinista (AFD)** o **no determinista (AFND)**, y validar si una cadena es aceptada o rechazada.

### Diferencia entre AFD y AFND

| Tipo | Definición | Cuándo ocurre |
|---|---|---|
| **AFD** | Desde cada estado hay exactamente UN camino por símbolo | Expresión sin `\|`, `?` ni `*` |
| **AFND** | Desde un estado puede haber MÁS DE UN camino por símbolo | Expresión con `\|`, `?` o `*` |

### Cómo usarlo

1. Ingresar una expresión regular en el campo **Expresión regular**
2. Ingresar una cadena en el campo **Cadena a validar**
3. Presionar **Analizar y Validar**

El resultado mostrará el tipo de autómata detectado y si la cadena fue aceptada o rechazada.

### Ejemplos

| Expresión | Tipo | Cadena | Resultado |
|---|---|---|---|
| `(a\|b)*` | AFND | `aabb` | ACEPTADA |
| `ab+a` | AFD | `abba` | ACEPTADA |
| `(0\|1)+` | AFND | `1010` | ACEPTADA |
| `a?b+` | AFND | `bbb` | ACEPTADA |
| `ab+a` | AFD | `aa` | RECHAZADA |

---

## Ejemplo Completo

### Código de prueba

```c
#include <stdio.h>

// Programa de prueba
int main() {
    int x = 5;
    if (x > 0) {
        return x;
    }
    return 0;
}
```

### Resultado esperado

```
  Código analizado correctamente.

  Líneas de código : 10
  Total de tokens  : 30

  RESUMEN POR TIPO DE TOKEN
  --------------------------------------------------
  Palabra Reservada          5
  Identificador              2
  Entero                     2
  Op Relacional              1
  Op Asignacion              1
  Delimitador               11
  Preprocesador              1
  Comentario Sl              1

  Análisis léxico: EXITOSO
```

---

## Preguntas Frecuentes

**¿Por qué mi variable no se reconoce como identificador?**  
Verificá que no empiece con un número o símbolo especial. Solo puede comenzar con letra o guion bajo `_`.

**¿Por qué el número negativo no se reconoce como un solo token?**  
El signo `-` es un operador separado. `-5` se analiza como `OP(-)` + `NUM(5)`, no como un número negativo.

**¿El archivo tiene que ser `.c` obligatoriamente?**  
Para usar el botón **Abrir** sí, pero con **Nuevo** podés escribir cualquier código directamente sin guardar.

**¿Puedo analizar código con errores?**  
Sí. El analizador detecta los errores léxicos, los reporta con número de línea y continúa con el resto del código.

**¿Qué diferencia hay entre AFD y AFND en el módulo de Autómatas?**  
Un AFD tiene exactamente un camino por símbolo desde cada estado. Un AFND puede tener más de uno. En la expresión regular, la presencia de `|`, `?` o `*` indica no determinismo.

---

*Manual generado para el curso de Autómatas y Lenguajes — Universidad Mesoamericana 2026*
