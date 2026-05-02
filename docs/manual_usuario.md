# Manual de Usuario — Analizador Léxico MicroC

**Versión:** 2.0  
**Autor:** Rosa Andrea Fernanda Torres Del Aguila  
**Carné:** 202425516  
**Curso:** Autómatas y Lenguajes — Universidad Mesoamericana 2026

---

## ¿Qué es el Analizador Léxico MicroC?

El Analizador Léxico MicroC es una aplicación de escritorio que analiza código escrito en el lenguaje MicroC (basado en C/C++). Identifica cada token del código e indica si las cadenas **pertenecen o no pertenecen** al lenguaje MicroC.

---

## Requisitos del Sistema

- Sistema operativo: Windows 10/11
- Python 3.x instalado
- No requiere instalación de librerías adicionales

---

## Cómo Ejecutar la Aplicación

1. Abrir una terminal (PowerShell o CMD)
2. Navegar a la carpeta del proyecto:
```bash
cd ruta\del\proyecto
```
3. Ejecutar el archivo:
```bash
python src/"microC compiler.py"
```

---

## Interfaz de la Aplicación

La aplicación tiene dos paneles principales:

| Panel | Descripción |
|-------|-------------|
| **Panel izquierdo** | Editor de código MicroC (TextBox1) |
| **Panel derecho** | Resultados del análisis léxico (TextBox2) |

---

## Botones y Funciones

| Botón | Atajo | Función |
|-------|-------|---------|
| **Nuevo** | Ctrl+N | Crea un nuevo archivo en modo edición |
| **Abrir** | Ctrl+A | Carga un archivo .c existente |
| **Guardar** | Ctrl+G | Guarda el archivo con extensión .c |
| **Editar** | — | Habilita la edición del archivo abierto |
| **Compilar** | F5 | Ejecuta el análisis léxico |
| **Salir** | — | Cierra la aplicación |

---

## Cómo Usar el Analizador Léxico

### Paso 1 — Ingresar código
- Haz clic en **Nuevo** para escribir código directamente, o
- Haz clic en **Abrir** para cargar un archivo `.c` existente

### Paso 2 — Ejecutar el análisis
- Presiona el botón **Compilar** o la tecla **F5**

### Paso 3 — Ver resultados
El panel derecho mostrará:
```
#     TIPO                   VALOR              LINEA
1     Palabra Reservada      int                1
2     Palabra Reservada      main               1
3     Delimitador            (                  1
...
  Análisis léxico: EXITOSO
```

---

## Tokens Reconocidos

| Token | Descripción | Ejemplos válidos | Ejemplos inválidos |
|-------|-------------|------------------|--------------------|
| **Palabra Reservada** | Palabras del lenguaje | `int`, `if`, `while` | `Int`, `IF` |
| **Identificador** | Nombres de variables | `x`, `total`, `var1` | `1var`, `-abc` |
| **Entero** | Números enteros | `0`, `42`, `100` | `-5`, `3.` |
| **Real** | Números decimales | `3.14`, `1.0` | `3.`, `.14` |
| **Op Aritmético** | Operadores matemáticos | `+`, `-`, `*`, `/` | `++`, `**` |
| **Op Relacional** | Comparaciones | `==`, `!=`, `<`, `>` | `=>`, `=<` |
| **Op Asignación** | Asignación | `=`, `+=`, `-=` | `:=` |
| **Delimitador** | Separadores | `(`, `)`, `;`, `{` | — |
| **Comentario Sl** | Comentario de línea | `// texto` | `/ texto` |
| **Comentario Ml** | Comentario de bloque | `/* texto */` | `/* sin cerrar` |

---

## Interpretación de Resultados

### Código válido ✅
La barra inferior se pone **verde** y muestra:
```
Análisis léxico exitoso
```

### Código con errores ✗
La barra inferior se pone **roja** y muestra:
```
✗ N error(es) léxico(s)
```
En el panel de resultados aparece:
```
  ERRORES LÉXICOS

  Línea 3: símbolo desconocido '@'
```

---

## Ejemplo Completo

### Código de prueba
```c
#include <stdio.h>

int main() {
    int x = 5;
    if (x > 0) {
        return x; // retorna x
    }
    return 0;
}
```

### Resultado esperado
```
#     TIPO                   VALOR              LINEA
1     Preprocesador          #include <std...   1
2     Palabra Reservada      int                3
3     Palabra Reservada      main               3
4     Delimitador            (                  3
...
  Análisis léxico: EXITOSO
```

---

## Preguntas Frecuentes

**¿Por qué mi variable no se reconoce como identificador?**  
Verifica que no empiece con un número o símbolo especial. Solo puede empezar con letra o guion bajo `_`.

**¿Por qué el número negativo no se reconoce?**  
El signo `-` es un operador separado. `-5` se analiza como `OP(-)` + `NUM(5)`, no como un número negativo.

**¿El archivo tiene que ser .c obligatoriamente?**  
Para abrir con el botón **Abrir** sí, pero con **Nuevo** puedes escribir cualquier código directamente.

---

*Manual generado para el curso de Autómatas y Lenguajes — Universidad Mesoamericana 2026*
