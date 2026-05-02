import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import re


#  ANALIZADOR LÉXICO

PALABRAS_RESERVADAS = {
    "int", "float", "double", "char", "void", "bool",
    "if", "else", "while", "for", "do", "return",
    "break", "continue", "switch", "case", "default",
    "struct", "typedef", "sizeof", "const", "static",
    "include", "define", "main", "printf", "scanf",
    "true", "false", "null", "NULL"
}

# Orden importa: los patrones más específicos van primero
TOKEN_SPEC = [
    ("COMENTARIO_ML", r"/\*[\s\S]*?\*/"),          # /* comentario */
    ("COMENTARIO_SL", r"//[^\n]*"),                 # // comentario
    ("PREPROCESADOR",  r"#\s*\w+[^\n]*"),           # #include, #define
    ("REAL",           r"\d+\.\d+([eE][+-]?\d+)?"), # 3.14, 1.0e5
    ("ENTERO",         r"\d+"),                      # 42
    ("CADENA",         r'"[^"\\]*(\\.[^"\\]*)*"'),  # "hola"
    ("CARACTER",       r"'[^'\\]*(\\.)?' "),         # 'a'
    ("OP_LOGICO",      r"&&|\|\|"),                  # && ||
    ("OP_RELACIONAL",  r"==|!=|<=|>=|<|>"),          # == != <= >=
    ("OP_ASIGNACION",  r"\+=|-=|\*=|/=|%=|="),      # = += -= etc
    ("OP_INCREMENTO",  r"\+\+|--"),                  # ++ --
    ("OP_ARITMETICO",  r"[+\-*/%]"),                 # + - * / %
    ("OP_BITS",        r"&|\||\^|~|<<|>>"),          # & | ^ ~
    ("DELIMITADOR",    r"[(){}\[\];,.]"),             # ( ) { } [ ] ; ,
    ("IDENTIFICADOR",  r"[a-zA-Z_]\w*"),             # variables, funciones
    ("ESPACIO",        r"[ \t\r\n]+"),               # espacios (ignorar)
    ("DESCONOCIDO",    r"."),                         # cualquier otro
]

TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

def analizar_lexico(codigo):
    tokens = []
    errores = []
    linea = 1

    for mo in TOKEN_REGEX.finditer(codigo):
        tipo = mo.lastgroup
        valor = mo.group()

        # Contar saltos de línea para rastrear número de línea
        linea += valor.count("\n")

        if tipo == "ESPACIO":
            continue
        elif tipo == "DESCONOCIDO":
            errores.append((linea, valor))
        elif tipo == "IDENTIFICADOR":
            if valor in PALABRAS_RESERVADAS:
                tokens.append(("PALABRA_RESERVADA", valor, linea))
            else:
                tokens.append(("IDENTIFICADOR", valor, linea))
        else:
            tokens.append((tipo, valor, linea))

    return tokens, errores


def formatear_resultado(tokens, errores, codigo):
    lineas_codigo = codigo.splitlines()
    total_lineas = len(lineas_codigo)

    # Contadores por tipo
    conteo = {}
    for tipo, _, _ in tokens:
        conteo[tipo] = conteo.get(tipo, 0) + 1

    resultado = []
    resultado.append("   ANÁLIZADOR LÉXICO - MicroC Compiler")
    resultado.append("")

    # ── Resultado general ──
    if errores:
        resultado.append(f"\n TOKENS NO RECONOCIDOS: {len(errores)}")
        resultado.append("  El código contiene símbolos inválidos.")
    else:
        resultado.append(f"\n Código analizado correctamente.")
        resultado.append(f"  Todos los tokens pertenecen al lenguaje MicroC.")

    resultado.append(f"\n  Líneas de código : {total_lineas}")
    resultado.append(f"  Total de tokens  : {len(tokens)}")

    # Tabla de tokens por tipo 
    resultado.append("")
    resultado.append("  RESUMEN POR TIPO DE TOKEN")
    resultado.append("-" * 48)
    orden = [
        "PALABRA_RESERVADA", "IDENTIFICADOR", "ENTERO", "REAL",
        "CADENA", "CARACTER", "OP_ARITMETICO", "OP_RELACIONAL",
        "OP_ASIGNACION", "OP_LOGICO", "OP_INCREMENTO", "OP_BITS",
        "DELIMITADOR", "PREPROCESADOR", "COMENTARIO_SL", "COMENTARIO_ML"
    ]
    for tipo in orden:
        if tipo in conteo:
            nombre = tipo.replace("_", " ").title()
            resultado.append(f"  {nombre:<25} {conteo[tipo]:>4}")

    # ── Lista detallada de tokens ──
    resultado.append("\n" + "-" * 48)
    resultado.append("  TOKENS ENCONTRADOS")
    resultado.append("-" * 48)
    resultado.append(f"  {'#':<4} {'TIPO':<18} {'VALOR':<14} {'LÍNEA'}")
    resultado.append(f"  {'-'*4:<4} {'-'*21:<18} {'-'*17:<14} ----")

    for i, (tipo, valor, lin) in enumerate(tokens, 1):
        nombre = tipo.replace("_", " ").title()
        # truncar valores largos
        val_corto = valor if len(valor) <= 16 else valor[:13] + "..."
        resultado.append(f"  {i:<5} {nombre:<22} {val_corto:<18} {lin}")

    # ── Errores si los hay ──
    if errores:
        resultado.append("")
        resultado.append("TOKENS NO RECONOCIDOS (ERRORES)")
        resultado.append("-" * 48)
        for lin, val in errores:
            resultado.append(f"  Línea {lin}: símbolo desconocido '{val}'")

    estado = "EXITOSO! " if not errores else f"CON {len(errores)} ERROR(ES) "
    resultado.append(f"\n  Análisis léxico: {estado}")

    return "\n".join(resultado)


#  APLICACIÓN PRINCIPAL

class MicroCCompiler:
    def __init__(self, root):
        self.root = root
        self.root.title("MicroC Compiler - [Sin archivo]")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e1e1e")

        self.archivo_actual = None
        self.archivo_modificado = False
        self.modo_edicion = False

        self._construir_menu()
        self._construir_interfaz()
        self._actualizar_estado()

        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    def _construir_menu(self):
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white",
                          activebackground="#0078d4", activeforeground="white",
                          borderwidth=0)

        menu_archivo = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white",
                               activebackground="#0078d4", activeforeground="white")
        menu_archivo.add_command(label="  Nuevo        Ctrl+N", command=self.nuevo)
        menu_archivo.add_command(label="  Abrir...      Ctrl+A", command=self.abrir)
        menu_archivo.add_command(label="  Guardar      Ctrl+G", command=self.guardar)
        menu_archivo.add_separator()
        menu_archivo.add_command(label="  Salir         Alt+F4", command=self.salir)
        menubar.add_cascade(label=" Archivo ", menu=menu_archivo)

        menu_editar = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white",
                              activebackground="#0078d4", activeforeground="white")
        menu_editar.add_command(label="  Editar archivo", command=self.editar)
        menubar.add_cascade(label=" Editar ", menu=menu_editar)

        menu_compilar = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white",
                                activebackground="#0078d4", activeforeground="white")
        menu_compilar.add_command(label="  Análisis Léxico  F5", command=self.compilar)
        menubar.add_cascade(label=" Compilar ", menu=menu_compilar)

        menu_ayuda = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white",
                             activebackground="#0078d4", activeforeground="white")
        menu_ayuda.add_command(label="  Ayuda", command=self.ayuda)
        menu_ayuda.add_command(label="  Acerca de", command=self.acerca_de)
        menu_ayuda.add_command(label="  GitHub", command=self.abrir_github)
        menubar.add_cascade(label=" Ayuda ", menu=menu_ayuda)

        self.root.config(menu=menubar)

        self.root.bind("<Control-n>", lambda e: self.nuevo())
        self.root.bind("<Control-a>", lambda e: self.abrir())
        self.root.bind("<Control-g>", lambda e: self.guardar())
        self.root.bind("<F5>",        lambda e: self.compilar())

    def _construir_interfaz(self):
        toolbar = tk.Frame(self.root, bg="#2d2d2d", height=40)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        btn_style = dict(bg="#0078d4", fg="white", relief="flat",
                         padx=10, pady=4, cursor="hand2",
                         activebackground="#005a9e", activeforeground="white",
                         font=("Segoe UI", 9))

        tk.Button(toolbar, text="Nuevo",    command=self.nuevo,    **btn_style).pack(side=tk.LEFT, padx=(8,2), pady=5)
        tk.Button(toolbar, text="Abrir",    command=self.abrir,    **btn_style).pack(side=tk.LEFT, padx=2,    pady=5)
        tk.Button(toolbar, text="Guardar",  command=self.guardar,  **btn_style).pack(side=tk.LEFT, padx=2,    pady=5)
        tk.Button(toolbar, text="Editar",   command=self.editar,   **btn_style).pack(side=tk.LEFT, padx=2,    pady=5)
        tk.Button(toolbar, text="Compilar", command=self.compilar,
                  bg="#27ae60", fg="white", relief="flat", padx=10, pady=4,
                  cursor="hand2", activebackground="#1e8449", activeforeground="white",
                  font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(toolbar, text="Salir",    command=self.salir,
                  bg="#c0392b", fg="white", relief="flat", padx=10, pady=4,
                  cursor="hand2", activebackground="#922b21", activeforeground="white",
                  font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=8, pady=5)

        labels_frame = tk.Frame(self.root, bg="#1e1e1e")
        labels_frame.pack(fill=tk.X, padx=10, pady=(8, 0))

        tk.Label(labels_frame, text="Codigo MicroC", bg="#1e1e1e", fg="#9cdcfe",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=5)
        tk.Label(labels_frame, text="Resultados del Análisis Léxico", bg="#1e1e1e", fg="#9cdcfe",
                 font=("Segoe UI", 9, "bold")).pack(side=tk.RIGHT, padx=5)

        panel = tk.Frame(self.root, bg="#1e1e1e")
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        codigo_font = font.Font(family="Courier New", size=11)

        frame_codigo = tk.Frame(panel, bg="#252526", bd=1, relief="solid")
        frame_codigo.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.numeros_linea = tk.Text(frame_codigo, width=4, bg="#1e1e1e", fg="#858585",
                                     state="disabled", font=codigo_font,
                                     bd=0, padx=4, pady=6, cursor="arrow")
        self.numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

        self.textbox1 = tk.Text(frame_codigo, bg="#1e1e1e", fg="#d4d4d4",
                                insertbackground="white", font=codigo_font,
                                bd=0, padx=6, pady=6, undo=True,
                                state="disabled", wrap="none")
        self.textbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scroll1 = tk.Scrollbar(frame_codigo, command=self._scroll_codigo)
        scroll1.pack(side=tk.RIGHT, fill=tk.Y)
        self.textbox1.config(yscrollcommand=scroll1.set)

        self.textbox1.bind("<KeyRelease>", self._on_texto_cambiado)
        self.textbox1.bind("<MouseWheel>", self._actualizar_numeros)

        frame_resultado = tk.Frame(panel, bg="#252526", bd=1, relief="solid")
        frame_resultado.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.textbox2 = tk.Text(frame_resultado, bg="#0d1117", fg="#58a6ff",
                                font=("Courier New", 10), bd=0, padx=8, pady=8,
                                state="disabled", wrap="word")
        self.textbox2.pack(fill=tk.BOTH, expand=True)

        scroll2 = tk.Scrollbar(frame_resultado, command=self.textbox2.yview)
        scroll2.pack(side=tk.RIGHT, fill=tk.Y)
        self.textbox2.config(yscrollcommand=scroll2.set)

        self.barra_estado = tk.Label(self.root, text="Listo", bg="#007acc",
                                     fg="white", anchor="w", padx=10,
                                     font=("Segoe UI", 8))
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

        self._log_resultado("MicroC Compiler v2.0 - Análisis Léxico\nListo. Abra o cree un archivo y presione Compilar (F5).")

    def _scroll_codigo(self, *args):
        self.textbox1.yview(*args)
        self.numeros_linea.yview(*args)

    def _actualizar_numeros(self, event=None):
        self.numeros_linea.config(state="normal")
        self.numeros_linea.delete("1.0", "end")
        lineas = int(self.textbox1.index("end-1c").split(".")[0])
        numeros = "\n".join(str(i) for i in range(1, lineas + 1))
        self.numeros_linea.insert("1.0", numeros)
        self.numeros_linea.config(state="disabled")

    def _log_resultado(self, texto, limpiar=True):
        self.textbox2.config(state="normal")
        if limpiar:
            self.textbox2.delete("1.0", "end")
        self.textbox2.insert("end", texto + "\n")
        self.textbox2.see("end")
        self.textbox2.config(state="disabled")

    def _set_codigo(self, texto):
        self.textbox1.config(state="normal")
        self.textbox1.delete("1.0", "end")
        self.textbox1.insert("1.0", texto)
        if not self.modo_edicion:
            self.textbox1.config(state="disabled")
        self._actualizar_numeros()

    def _get_codigo(self):
        return self.textbox1.get("1.0", "end-1c")

    def _actualizar_titulo(self):
        if self.archivo_actual:
            modificado = " *" if self.archivo_modificado else ""
            self.root.title(f"MicroC Compiler - {self.archivo_actual}{modificado}")
        else:
            self.root.title("MicroC Compiler - [Sin archivo]")

    def _actualizar_estado(self):
        modo = "Edicion" if self.modo_edicion else "Solo lectura"
        archivo = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin archivo"
        self.barra_estado.config(text=f"  {modo}   |   {archivo}")

    def _on_texto_cambiado(self, event=None):
        self.archivo_modificado = True
        self._actualizar_titulo()
        self._actualizar_numeros()

    def _confirmar_guardar(self):
        if self.archivo_modificado:
            resp = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "El archivo tiene cambios sin guardar.\n¿Desea guardarlos antes de continuar?"
            )
            if resp is None:
                return False
            elif resp:
                self.guardar()
        return True

    def nuevo(self):
        if not self._confirmar_guardar():
            return
        self.archivo_actual = None
        self.archivo_modificado = False
        self.modo_edicion = True
        self.textbox1.config(state="normal")
        self._set_codigo("")
        self._actualizar_titulo()
        self._actualizar_estado()
        self._log_resultado(" NUEVO ARCHIVO CREADO ")
        self.textbox1.focus()

    def abrir(self):
        if not self._confirmar_guardar():
            return
        ruta = filedialog.askopenfilename(
            title="Abrir archivo MicroC",
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        if not ruta:
            return
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
            self.archivo_actual = ruta
            self.archivo_modificado = False
            self.modo_edicion = False
            self.textbox1.config(state="normal")
            self._set_codigo(contenido)
            self.textbox1.config(state="disabled")
            self._actualizar_titulo()
            self._actualizar_estado()
            self._log_resultado(f"-- Archivo abierto: {ruta} --")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el archivo:\n{e}")

    def guardar(self):
        if not self.archivo_actual:
            ruta = filedialog.asksaveasfilename(
                title="Guardar archivo MicroC",
                defaultextension=".c",
                filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
            )
            if not ruta:
                return
            self.archivo_actual = ruta
        try:
            with open(self.archivo_actual, "w", encoding="utf-8") as f:
                f.write(self._get_codigo())
            self.archivo_modificado = False
            self._actualizar_titulo()
            self._actualizar_estado()
            self._log_resultado(f"-- Archivo guardado: {self.archivo_actual} --")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def editar(self):
        self.modo_edicion = True
        self.textbox1.config(state="normal")
        self._actualizar_estado()
        self._log_resultado(" Modo edicion activado ")
        self.textbox1.focus()

    def compilar(self):
        codigo = self._get_codigo().strip()

        if not codigo:
            self._log_resultado(
                "  No hay código para analizar.\n"
                "  Crea o abre un archivo .c primero."
            )
            return

        tokens, errores = analizar_lexico(codigo)
        resultado = formatear_resultado(tokens, errores, codigo)
        self._log_resultado(resultado)

        # Actualizar barra de estado
        estado = " Análisis léxico exitoso" if not errores else f" {len(errores)} error(es) léxico(s)"
        archivo = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin archivo"
        self.barra_estado.config(
            text=f"  {estado}   |   {archivo}",
            bg="#16a34a" if not errores else "#c0392b"
        )

    def ayuda(self):
        self._log_resultado(
            "=" * 48 + "\n"
            "  AYUDA - MicroC Compiler v2.0\n"
            "-" * 48 + "\n"
            "  Nuevo    → Crear nuevo archivo\n"
            "  Abrir    → Cargar archivo .C\n"
            "  Guardar  → Guardar archivo .C\n"
            "  Editar   → Habilitar edición\n"
            "  Compilar → Ejecutar análisis léxico (F5)\n"
            "  Salir    → Cerrar aplicación\n"
            "-" * 48 + "\n"
            "  El analizador léxico identifica:\n"
            "  Palabras reservadas, identificadores,\n"
            "  números, operadores, delimitadores,\n"
            "  cadenas, comentarios y más.\n"
            "=" * 48
        )

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de MicroC Compiler",
            "MicroC Compiler v2.0\n"
            "Análisis Léxico — Etapa 1\n\n"
            "Proyecto para el curso de Autómatas y Lenguajes\n"
            "Creada por: Rosa Torres\n"
            "Universidad Mesoamericana — 2026"
        )

    def abrir_github(self):
        import webbrowser
        webbrowser.open("https://github.com/andrea10-baa/Compilador-MicroC-RosaTorres")

    def salir(self):
        if not self._confirmar_guardar():
            return
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCCompiler(root)
    root.mainloop()