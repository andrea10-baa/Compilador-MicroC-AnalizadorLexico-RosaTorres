# Compilador-MicroC-AnalizadorLexico-RosaTorres

| Campo | Información |
| --- | --- |
| **Nombre** | Rosa Andrea Fernanda Torres Del Aguila |
| **Carné** | 202425516 |
| **Curso** | Autómatas y Lenguajes |
| **Proyecto** | Analizador Léxico MicroC — Etapa 1 |
| **Universidad** | Universidad Mesoamericana |
| **Año** | 2026 |

---

## Descripción del Proyecto

El Analizador Léxico MicroC es la primera etapa del compilador, desarrollada como parte del curso de Autómatas y Lenguajes. Implementa el análisis léxico utilizando expresiones regulares y autómatas finitos para reconocer tokens del lenguaje MicroC (basado en C/C++).

El analizador indica si el código ingresado **pertenece o no pertenece** al lenguaje MicroC, identificando cada token y reportando errores léxicos con número de línea.

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
| **Ayuda** | Muestra información de uso de la aplicación |
| **Salir** | Cierra la aplicación con confirmación de guardado |

---

## Ejemplo de Uso

### CÓDIGO VÁLIDO!

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

### CÓDIGO CON ERRORES 

```c
int main() {
    int x = 10 @ 2;
    return 0;
}
```

**Resultado:** CON 1 ERROR — Línea 2: símbolo desconocido '@'

---

## Video Demostrativo

Enlace al video demostrativo: [Ver video]()

---

## Estructura del Proyecto

```
Compilador-MicroC-AnalizadorLexico-RosaTorres/
│
├── microC compiler.py      → Código fuente con analizador léxico
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
