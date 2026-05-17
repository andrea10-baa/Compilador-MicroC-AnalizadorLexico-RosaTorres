# Compilador-MicroC-AnalizadorLexico-RosaTorres

| Campo | Información |
| --- | --- |
| **Nombre** | Rosa Andrea Fernanda Torres Del Aguila |
| **Carné** | 202425516 |
| **Curso** | Autómatas y Lenguajes |
| **Proyecto** | Analizador Léxico MicroC — Etapa 1 Y Etapa 2 |
| **Universidad** | Universidad Mesoamericana |
| **Año** | 2026 |

---

## Descripción del Proyecto

El compilador MicroC es un proyecto desarrollado en dos etapas como parte del curso de Autómatas y Lenguajes.

**Etapa 1 — Analizador Léxico:** Implementa el análisis léxico utilizando expresiones regulares para reconocer tokens del lenguaje MicroC (basado en C/C++). El analizador indica si el código ingresado **pertenece o no pertenece** al lenguaje MicroC, identificando cada token con su número correspondiente y reportando errores léxicos con número de línea.

**Etapa 2 — Autómatas AFD y AFND:** Implementa un módulo interactivo de autómatas finitos. Permite ingresar expresiones regulares propias y validar cadenas en tiempo real, detectando automáticamente si la expresión corresponde a un AFD o AFND.

---

## Tokens Reconocidos

| Token | Descripción | Expresión Regular |
| --- | --- | --- |
| **ID** | Identificadores | `[a-zA-Z_][a-zA-Z0-9_]*` |
| **NUM** | Números enteros | `[0-9]+` |
| **REAL** | Números reales | `[0-9]+\.[0-9]+` |
| **OP** | Operadores aritméticos | `[+\-*/%]` |
| **DELIM** | Delimitadores | `[(){}\[\];,.]` |
| **KW** | Palabras reservadas | `if, while, int, float...` |
| **CMT_SL** | Comentarios de línea | `//[^\n]*` |
| **CMT_ML** | Comentarios de bloque | `/\*[\s\S]*?\*/` |

---

## Tabla de Tokens Numéricos

| Rango | Tipo |
| --- | --- |
| 1 – 33 | Palabras reservadas C/C++ (auto, break, char, int, while...) |
| 34 – 39 | Directivas de preprocesador (include, define, ifdef...) |
| 40 – 49 | Funciones stdio.h (printf, scanf, fopen, fclose...) |
| 50 – 59 | Funciones stdlib.h (malloc, free, exit, rand...) |
| 60 – 64 | Generales (main, NULL, true, false) |
| 70 – 74 | Operadores aritméticos (+, -, *, /, %) |
| 75 – 82 | Asignación e incremento (=, +=, -=, ++, --) |
| 83 – 88 | Operadores relacionales (==, !=, <, >, <=, >=) |
| 89 – 91 | Operadores lógicos (&&, \|\|, !) |
| 92 – 97 | Agrupación ( ), { }, [ ] |
| 98 – 109 | Misceláneos (;, ,, ., :, &, \|, #, ?) |
| 200 | Número entero |
| 201 | Número real |
| 202 | Cadena de texto |
| 203 | Comentario de línea (//) |
| 204 | Comentario de bloque (/* */) |
| 205 | Directiva preprocesador (#include, #define) |
| 206 | Carácter ('a', '\n') |
| 300 | Identificador (variable o función definida por el usuario) |
| -1 | Token no reconocido (error léxico) |

---

## Autómatas (Etapa 2)

El módulo de autómatas permite ingresar cualquier expresión regular y una cadena para validar. El sistema detecta automáticamente si la expresión es **AFD** o **AFND** y muestra el resultado del procesamiento.

- **AFD** = Autómata Finito Determinista — cada estado tiene exactamente un camino por símbolo
- **AFND** = Autómata Finito No Determinista — puede haber más de un camino por símbolo (causado por `|`, `?`, `*`)

---

## Tecnologías Usadas

| Tecnología | Descripción |
| --- | --- |
| Python 3.13 | Lenguaje de programación principal |
| Tkinter | Librería para la interfaz gráfica (incluida en Python) |
| re (regex) | Módulo de expresiones regulares para el análisis léxico |

---

## Instrucciones de Ejecución

### Requisitos previos

- Tener instalado Python 3.x en la computadora
- Verificar la instalación con: `python --version`

### Pasos para ejecutar

1. Clonar el repositorio:

```
git clone https://github.com/andrea10-baa/Compilador-MicroC-AnalizadorLexico-RosaTorres.git
```

2. Ingresar a la carpeta del proyecto:

```
cd Compilador-MicroC-AnalizadorLexico-RosaTorres
```

3. Ejecutar el compilador:

```
python "microC compiler.py"
```

---

## Funcionalidades

| Botón | Función |
| --- | --- |
| **Nuevo** | Crea un nuevo archivo en modo edición |
| **Abrir** | Carga un archivo .c existente (solo lectura) |
| **Guardar** | Guarda el archivo con extensión .c |
| **Editar** | Habilita la edición del archivo abierto |
| **Compilar** | Ejecuta el análisis léxico (F5) |
| **Autómatas** | Abre el módulo de autómatas AFD y AFND (F6) |
| **Ayuda** | Muestra información de uso de la aplicación |
| **Salir** | Cierra la aplicación con confirmación de guardado |

---

## Atajos de Teclado

| Atajo | Función |
| --- | --- |
| Ctrl + N | Nuevo archivo |
| Ctrl + A | Abrir archivo |
| Ctrl + G | Guardar archivo |
| F5 | Ejecutar análisis léxico |
| F6 | Abrir módulo de autómatas |

---

## Ejemplo de Uso

### Código válido ✅

```c
int main() {
    int x = 5;
    if (x > 0) {
        return x;
    }
    return 0;
}
```

**Resultado:** Análisis léxico EXITOSO — todos los tokens pertenecen al lenguaje MicroC.

### Código con errores ✗

```c
int main() {
    int x = 10 @ 2;
    return 0;
}
```

**Resultado:** CON 1 ERROR — Línea 2: símbolo desconocido '@'

---

## Video Demostrativo

Enlace al video demostrativo: [Ver video](https://youtu.be/6cNhU_VurHk)

---

## Estructura del Proyecto

```
Compilador-MicroC-AnalizadorLexico-RosaTorres/
│
├── microC compiler.py      → Código fuente con analizador léxico y autómatas
├── assets/                 → Recursos y capturas de pantalla
├── docs/                   → Documentación adicional
├── src/                    → Código fuente organizado
└── README.md               → Documentación principal
```

---

## Historial de Commits

| # | Mensaje |
| --- | --- |
| 1 | Initial commit |
| 2 | feat: implementar analizador lexico - etapa 1 |
| 3 | docs: actualizar README con documentacion del analizador lexico |
| 4 | docs: organizar estructura del repositorio |
| 5 | docs: organizar estructura y agregar manual de usuario |
| 6 | assets: agregar carpeta de recursos |
| 7 | assets: agregar capturas de pantalla |
| 8 | docs: actualizar nombre completo y carné en acerca_de |
| 9 | docs: actualizar README etapa 1 y etapa 2 |
| 10 | feat: eliminar automatas predefinidos del codigo |
| 11 | feat: quitar columna # de la tabla de tokens |
| 12 | feat: quitar ejemplos del mensaje de bienvenida en automatas |
| 13 | fix: version final corregida al 100 |
| 14 | fix: resolver conflicto README |
