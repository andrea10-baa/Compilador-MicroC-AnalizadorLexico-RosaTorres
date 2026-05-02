**PRE-COMPILADOR MICROC**


| Campo | Información |
|-------|-------------|
| **Nombre** | Rosa Andrea Fernanda Torres Del Aguila |
| **Carné** | 202425516 |
| **Curso** | Autómatas y Lenguajes |
| **Proyecto** | Pre-Compilador MicroC |
| **Universidad** | Universidad Mesoamericana |
| **Año** | 2026 |

---

## Descripción del Proyecto

El Pre-Compilador MicroC es una aplicación de escritorio desarrollada como parte del curso de Autómatas y Lenguajes. Consiste en una interfaz gráfica que simula el entorno de un compilador para el lenguaje MicroC (basado en C/C++).

La aplicación permite:
- Crear nuevos archivos de código en modo edición
- Abrir archivos existentes con extensión `.c`
- Guardar archivos con extensión `.c`
- Editar archivos cargados en la aplicación
- Visualizar mensajes y resultados en el panel de compilación
- Cerrar la aplicación con confirmación de guardado

---

## Tecnologías Usadas

| Tecnología | Descripción |
|------------|-------------|
| **Python 3.13** | Lenguaje de programación principal |
| **Tkinter** | Librería para la interfaz gráfica (incluida en Python) |

---

## Instrucciones de Ejecución

### Requisitos previos
- Tener instalado **Python 3.x** en la computadora
- Verificar la instalación con: `python --version`

### Pasos para ejecutar

1. Clonar el repositorio:
```bash
git clone https://github.com/andrea10-baa/Compilador-MicroC-RosaTorres.git
```

2. Ingresar a la carpeta del proyecto:
```bash
cd Compilador-MicroC-RosaTorres
```

3. Ejecutar el compilador:
```bash
python src/"MicroC compiler.py"
```

---

## Funcionalidades

| Botón | Función |
|-------|---------|
| **Nuevo** | Crea un nuevo archivo en modo edición |
| **Abrir** | Carga un archivo `.c` existente (solo lectura) |
| **Guardar** | Guarda el archivo con extensión `.c` |
| **Editar** | Habilita la edición del archivo abierto |
| **Compilar** | Función en desarrollo para próximas entregas |
| **Ayuda** | Muestra información de uso de la aplicación |
| **Salir** | Cierra la aplicación con confirmación de guardado |

---

## Capturas de Pantalla

*Las capturas de pantalla se encuentran en la carpeta `/assets/`*

---

## Video Demostrativo

*Enlace al video demostrativo:* [Ver video](https://youtu.be/Udzv8dCWWm0)

---

## Estructura del Proyecto

```
Compilador-MicroC-RosaTorres/
│
├── src/                    → Código fuente
│   └── MicroC compiler.py
│
├── assets/                 → Capturas de pantalla e imágenes
│
├── docs/                   → Documentación y manual de usuario
│
└── README.md               → Documentación principal
```
