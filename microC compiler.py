import tkinter as tk
from tkinter import filedialog, messagebox, font
import os
import re

# ─────────────────────────────────────────────
#  TABLA DE UNIDADES LÉXICAS (del código 2)
# ─────────────────────────────────────────────

PALABRAS = {
    # ── Palabras reservadas C/C++ ──────────────────────────────── 1–33
    "auto": 1,      "break": 2,     "case": 3,      "char": 4,      "const": 5,
    "continue": 6,  "default": 7,   "do": 8,        "double": 9,    "else": 10,
    "enum": 11,     "extern": 12,   "float": 13,    "for": 14,      "goto": 15,
    "if": 16,       "int": 17,      "long": 18,     "register": 19, "return": 20,
    "short": 21,    "signed": 22,   "sizeof": 23,   "static": 24,   "struct": 25,
    "switch": 26,   "typedef": 27,  "union": 28,    "unsigned": 29, "void": 30,
    "volatile": 31, "while": 32,    "bool": 33,

    # ── Directivas de preprocesador ───────────────────────────── 34–39
    "include": 34,  "define": 35,   "ifdef": 36,    "ifndef": 37,
    "endif": 38,    "undef": 39,

    # ── Funciones stdio.h ─────────────────────────────────────── 40–49
    "printf": 40,   "scanf": 41,    "fprintf": 42,  "fscanf": 43,
    "fopen": 44,    "fclose": 45,   "fgets": 46,    "fputs": 47,
    "fputc": 48,    "fgetc": 49,

    # ── Funciones stdlib.h ────────────────────────────────────── 50–59
    "malloc": 50,   "free": 51,     "exit": 52,     "atoi": 53,
    "atof": 54,     "atol": 55,     "rand": 56,     "srand": 57,
    "calloc": 58,   "realloc": 59,

    # ── Generales / otras ─────────────────────────────────────── 60–69
    "main": 60,     "null": 61,     "NULL": 62,     "true": 63,
    "false": 64,
}

SIMBOLOS = {
    # ── Aritméticos ───────────────────────────────────────────── 70–74
    "+": 70,  "-": 71,  "*": 72,  "/": 73,  "%": 74,

    # ── Asignación / incremental / decremental ────────────────── 75–82
    "=": 75,  "+=": 76, "-=": 77, "*=": 78, "/=": 79, "%=": 80,
    "++": 81, "--": 82,

    # ── Relacionales ──────────────────────────────────────────── 83–88
    "==": 83, "!=": 84, "<": 85,  ">": 86,  "<=": 87, ">=": 88,

    # ── Lógicos ───────────────────────────────────────────────── 89–91
    "&&": 89, "||": 90, "!": 91,

    # ── Agrupación ────────────────────────────────────────────── 92–97
    "(": 92,  ")": 93,  "{": 94,  "}": 95,  "[": 96,  "]": 97,

    # ── Misceláneos ───────────────────────────────────────────── 98–107
    ";": 98,  ",": 99,  ".": 100, ":": 101,
    "&": 102, "|": 103, "^": 104, "~": 105, "<<": 106, ">>": 107,

    # ── Generales / otros ─────────────────────────────────────── 108–109
    "#": 108, "?": 109,
}


def get_token_palabra(lexema):
    return PALABRAS.get(lexema, 300)   # 300 = identificador


def get_token_simbolo(lexema):
    return SIMBOLOS.get(lexema, -1)    # -1 = símbolo no encontrado


# ─────────────────────────────────────────────
#  PATRONES DEL ANALIZADOR LÉXICO
# ─────────────────────────────────────────────

TOKEN_SPEC = [
    ("COMENTARIO_ML", r"/\*[\s\S]*?\*/"),           # /* comentario */
    ("COMENTARIO_SL", r"//[^\n]*"),                  # // comentario
    ("PREPROCESADOR",  r"#\s*\w+[^\n]*"),            # #include, #define
    ("REAL",           r"\d+\.\d+([eE][+-]?\d+)?"),  # 3.14, 1.0e5
    ("ENTERO",         r"\d+"),                       # 42
    ("CADENA",         r'"[^"\\]*(\\.[^"\\]*)*"'),   # "hola"
    ("CARACTER",       r"'(?:[^'\\]|\\.)'"),             # 'a' '\n'
    ("OP_LOGICO",      r"&&|\|\|"),                   # && ||
    ("OP_RELACIONAL",  r"==|!=|<=|>=|<|>"),           # == != <= >= < >
    ("OP_ASIGNACION",  r"\+=|-=|\*=|/=|%=|="),       # = += -= etc.
    ("OP_INCREMENTO",  r"\+\+|--"),                   # ++ --
    ("OP_ARITMETICO",  r"[+\-*/%]"),                  # + - * / %
    ("OP_BITS",        r"&|\||\^|~|<<|>>"),           # & | ^ ~ << >>
    ("DELIMITADOR",    r"[(){}\[\];,.:]"),              # ( ) { } [ ] ; , . :
    ("IDENTIFICADOR",  r"[a-zA-Z_]\w*"),              # variables, funciones
    ("ESPACIO",        r"[ \t\r\n]+"),                # espacios (ignorar)
    ("DESCONOCIDO",    r"."),                          # cualquier otro
]

TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)


# ─────────────────────────────────────────────
#  ANÁLISIS LÉXICO  (retorna token numérico)
# ─────────────────────────────────────────────

def analizar_lexico(codigo):
    """
    Retorna:
      tokens  → lista de (tipo_str, valor, linea, num_token)
      errores → lista de (linea, valor)
    """
    tokens = []
    errores = []
    linea = 1

    for mo in TOKEN_REGEX.finditer(codigo):
        tipo = mo.lastgroup
        valor = mo.group()
        linea += valor.count("\n")

        if tipo == "ESPACIO":
            continue

        elif tipo == "DESCONOCIDO":
            errores.append((linea, valor))

        elif tipo == "IDENTIFICADOR":
            num_token = get_token_palabra(valor)
            tipo_nombre = "PALABRA_RESERVADA" if num_token != 300 else "IDENTIFICADOR"
            tokens.append((tipo_nombre, valor, linea, num_token))

        elif tipo in ("OP_LOGICO", "OP_RELACIONAL", "OP_ASIGNACION",
                      "OP_INCREMENTO", "OP_ARITMETICO", "OP_BITS", "DELIMITADOR"):
            num_token = get_token_simbolo(valor)
            tokens.append((tipo, valor, linea, num_token))

        elif tipo == "ENTERO":
            tokens.append((tipo, valor, linea, 200))
        elif tipo == "REAL":
            tokens.append((tipo, valor, linea, 201))
        elif tipo == "CADENA":
            tokens.append((tipo, valor, linea, 202))
        elif tipo == "COMENTARIO_SL":
            tokens.append((tipo, valor, linea, 203))
        elif tipo == "COMENTARIO_ML":
            tokens.append((tipo, valor, linea, 204))
        elif tipo == "PREPROCESADOR":
            tokens.append((tipo, valor, linea, 205))
        elif tipo == "CARACTER":
            tokens.append((tipo, valor, linea, 206))
        else:
            tokens.append((tipo, valor, linea, -1))

    return tokens, errores


# ─────────────────────────────────────────────
#  FORMATO DE RESULTADO  (del código 1 + token)
# ─────────────────────────────────────────────

def formatear_resultado(tokens, errores, codigo):
    lineas_codigo = codigo.splitlines()
    total_lineas = len(lineas_codigo)

    # Contadores por tipo
    conteo = {}
    for tipo, _, _, _ in tokens:
        conteo[tipo] = conteo.get(tipo, 0) + 1

    resultado = []
    resultado.append("   ANALIZADOR LÉXICO - MicroC Compiler")
    resultado.append("")

    if errores:
        resultado.append(f"  TOKENS NO RECONOCIDOS: {len(errores)}")
        resultado.append("  El código contiene símbolos inválidos.")
    else:
        resultado.append("  Código analizado correctamente.")
        resultado.append("  Todos los tokens pertenecen al lenguaje MicroC.")

    resultado.append(f"\n  Líneas de código : {total_lineas}")
    resultado.append(f"  Total de tokens  : {len(tokens)}")

    # ── Resumen por tipo ──
    resultado.append("")
    resultado.append("  RESUMEN POR TIPO DE TOKEN")
    resultado.append("-" * 50)
    orden = [
        "PALABRA_RESERVADA", "IDENTIFICADOR", "ENTERO", "REAL",
        "CADENA", "CARACTER", "OP_ARITMETICO", "OP_RELACIONAL",
        "OP_ASIGNACION", "OP_LOGICO", "OP_INCREMENTO", "OP_BITS",
        "DELIMITADOR", "PREPROCESADOR", "COMENTARIO_SL", "COMENTARIO_ML",
    ]
    for tipo in orden:
        if tipo in conteo:
            nombre = tipo.replace("_", " ").title()
            resultado.append(f"  {nombre:<25} {conteo[tipo]:>4}")

    # ── Lista detallada ──
    resultado.append("\n" + "-" * 60)
    resultado.append("  TOKENS ENCONTRADOS")
    resultado.append("-" * 60)
    resultado.append(f"  {'TIPO':<22} {'LEXEMA':<18} {'LÍN':>4}  {'TOKEN':>6}")
    resultado.append(f"  {'-'*22:<22} {'-'*17:<18} {'----':>4}  {'------':>6}")

    for tipo, valor, lin, num_token in tokens:
        nombre = tipo.replace("_", " ").title()
        val_corto = valor if len(valor) <= 16 else valor[:13] + "..."
        resultado.append(f"  {nombre:<22} {val_corto:<18} {lin:>4}  {num_token:>6}")

    # ── Errores ──
    if errores:
        resultado.append("")
        resultado.append("  TOKENS NO RECONOCIDOS (ERRORES)")
        resultado.append("-" * 50)
        for lin, val in errores:
            resultado.append(f"  Línea {lin}: símbolo desconocido '{val}'  →  Token: -1")

    estado = "EXITOSO ✓" if not errores else f"CON {len(errores)} ERROR(ES) ✗"
    resultado.append(f"\n  Análisis léxico: {estado}")

    return "\n".join(resultado)


# ─────────────────────────────────────────────
#  MÓDULO DE AUTÓMATAS AFD / AFND
# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
#  APLICACIÓN PRINCIPAL
# ─────────────────────────────────────────────

class MicroCCompiler:
    def __init__(self, root):
        self.root = root
        self.root.title("MicroC Compiler - [Sin archivo]")
        self.root.geometry("1100x680")
        self.root.configure(bg="#1e1e1e")

        self.archivo_actual = None
        self.archivo_modificado = False
        self.modo_edicion = False

        self._construir_menu()
        self._construir_interfaz()
        self._actualizar_estado()

        self.root.protocol("WM_DELETE_WINDOW", self.salir)

    # ── Menú ──────────────────────────────────

    def _construir_menu(self):
        menubar = tk.Menu(self.root, bg="#2d2d2d", fg="white",
                          activebackground="#0078d4", activeforeground="white",
                          borderwidth=0)

        def menu(label, items):
            m = tk.Menu(menubar, tearoff=0, bg="#2d2d2d", fg="white",
                        activebackground="#0078d4", activeforeground="white")
            for item in items:
                if item is None:
                    m.add_separator()
                else:
                    m.add_command(label=item[0], command=item[1])
            menubar.add_cascade(label=label, menu=m)

        menu(" Archivo ", [
            ("  Nuevo        Ctrl+N", self.nuevo),
            ("  Abrir...      Ctrl+A", self.abrir),
            ("  Guardar      Ctrl+G", self.guardar),
            None,
            ("  Salir         Alt+F4", self.salir),
        ])
        menu(" Editar ", [
            ("  Editar archivo", self.editar),
        ])
        menu(" Compilar ", [
            ("  Análisis Léxico  F5", self.compilar),
        ])
        menu(" Autómatas ", [
            ("  Ver AFD y AFND  F6", self.abrir_automatas),
        ])
        menu(" Ayuda ", [
            ("  Ayuda",     self.ayuda),
            ("  Acerca de", self.acerca_de),
            ("  GitHub",    self.abrir_github),
        ])

        self.root.config(menu=menubar)
        self.root.bind("<Control-n>", lambda e: self.nuevo())
        self.root.bind("<Control-a>", lambda e: self.abrir())
        self.root.bind("<Control-g>", lambda e: self.guardar())
        self.root.bind("<F5>",        lambda e: self.compilar())
        self.root.bind("<F6>",        lambda e: self.abrir_automatas())

    # ── Interfaz ──────────────────────────────

    def _construir_interfaz(self):
        # Toolbar
        toolbar = tk.Frame(self.root, bg="#2d2d2d", height=40)
        toolbar.pack(fill=tk.X, side=tk.TOP)

        btn = dict(bg="#0078d4", fg="white", relief="flat", padx=10, pady=4,
                   cursor="hand2", activebackground="#005a9e",
                   activeforeground="white", font=("Segoe UI", 9))

        for text, cmd in [("Nuevo", self.nuevo), ("Abrir", self.abrir),
                          ("Guardar", self.guardar), ("Editar", self.editar)]:
            tk.Button(toolbar, text=text, command=cmd, **btn).pack(
                side=tk.LEFT, padx=(8 if text == "Nuevo" else 2, 2), pady=5)

        tk.Button(toolbar, text="Compilar", command=self.compilar,
                  bg="#27ae60", fg="white", relief="flat", padx=10, pady=4,
                  cursor="hand2", activebackground="#1e8449",
                  activeforeground="white",
                  font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=5)

        tk.Button(toolbar, text="Autómatas", command=self.abrir_automatas,
                  bg="#8e44ad", fg="white", relief="flat", padx=10, pady=4,
                  cursor="hand2", activebackground="#6c3483",
                  activeforeground="white",
                  font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=2, pady=5)

        tk.Button(toolbar, text="Salir", command=self.salir,
                  bg="#c0392b", fg="white", relief="flat", padx=10, pady=4,
                  cursor="hand2", activebackground="#922b21",
                  activeforeground="white",
                  font=("Segoe UI", 9)).pack(side=tk.RIGHT, padx=8, pady=5)

        # Labels
        lf = tk.Frame(self.root, bg="#1e1e1e")
        lf.pack(fill=tk.X, padx=10, pady=(8, 0))
        lbl = dict(bg="#1e1e1e", fg="#9cdcfe", font=("Segoe UI", 9, "bold"))
        tk.Label(lf, text="Código MicroC", **lbl).pack(side=tk.LEFT, padx=5)
        tk.Label(lf, text="Resultados del Análisis Léxico", **lbl).pack(
            side=tk.RIGHT, padx=5)

        # Panel principal
        panel = tk.Frame(self.root, bg="#1e1e1e")
        panel.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        codigo_font = font.Font(family="Courier New", size=11)

        # Panel izquierdo (código)
        frame_cod = tk.Frame(panel, bg="#252526", bd=1, relief="solid")
        frame_cod.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

        self.numeros_linea = tk.Text(
            frame_cod, width=4, bg="#1e1e1e", fg="#858585",
            state="disabled", font=codigo_font, bd=0, padx=4, pady=6,
            cursor="arrow")
        self.numeros_linea.pack(side=tk.LEFT, fill=tk.Y)

        self.textbox1 = tk.Text(
            frame_cod, bg="#1e1e1e", fg="#d4d4d4", insertbackground="white",
            font=codigo_font, bd=0, padx=6, pady=6, undo=True,
            state="disabled", wrap="none")
        self.textbox1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sc1 = tk.Scrollbar(frame_cod, command=self._scroll_codigo)
        sc1.pack(side=tk.RIGHT, fill=tk.Y)
        self.textbox1.config(yscrollcommand=sc1.set)
        self.textbox1.bind("<KeyRelease>", self._on_texto_cambiado)
        self.textbox1.bind("<MouseWheel>", self._actualizar_numeros)

        # Panel derecho (resultado)
        frame_res = tk.Frame(panel, bg="#252526", bd=1, relief="solid")
        frame_res.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(5, 0))

        self.textbox2 = tk.Text(
            frame_res, bg="#0d1117", fg="#58a6ff",
            font=("Courier New", 10), bd=0, padx=8, pady=8,
            state="disabled", wrap="none")
        self.textbox2.pack(fill=tk.BOTH, expand=True)

        sc2 = tk.Scrollbar(frame_res, command=self.textbox2.yview)
        sc2.pack(side=tk.RIGHT, fill=tk.Y)
        self.textbox2.config(yscrollcommand=sc2.set)

        # Barra de estado
        self.barra_estado = tk.Label(
            self.root, text="Listo", bg="#007acc", fg="white",
            anchor="w", padx=10, font=("Segoe UI", 8))
        self.barra_estado.pack(fill=tk.X, side=tk.BOTTOM)

        self._log_resultado(
            "MicroC Compiler v3.0 - Análisis Léxico\n"
            "Listo. Abra o cree un archivo y presione Compilar (F5).")

    # ── Helpers ───────────────────────────────

    def _scroll_codigo(self, *args):
        self.textbox1.yview(*args)
        self.numeros_linea.yview(*args)

    def _actualizar_numeros(self, event=None):
        self.numeros_linea.config(state="normal")
        self.numeros_linea.delete("1.0", "end")
        lineas = int(self.textbox1.index("end-1c").split(".")[0])
        self.numeros_linea.insert("1.0", "\n".join(str(i) for i in range(1, lineas + 1)))
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
            mod = " *" if self.archivo_modificado else ""
            self.root.title(f"MicroC Compiler - {self.archivo_actual}{mod}")
        else:
            self.root.title("MicroC Compiler - [Sin archivo]")

    def _actualizar_estado(self):
        modo = "Edición" if self.modo_edicion else "Solo lectura"
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

    # ── Acciones ──────────────────────────────

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
        self._log_resultado("  NUEVO ARCHIVO CREADO")
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
            self._log_resultado(f"  Archivo abierto: {ruta}")
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
            self._log_resultado(f"  Archivo guardado: {self.archivo_actual}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

    def editar(self):
        self.modo_edicion = True
        self.textbox1.config(state="normal")
        self._actualizar_estado()
        self._log_resultado("  Modo edición activado")
        self.textbox1.focus()

    def compilar(self):
        codigo = self._get_codigo().strip()
        if not codigo:
            self._log_resultado(
                "  No hay código para analizar.\n"
                "  Crea o abre un archivo .c primero.")
            return

        tokens, errores = analizar_lexico(codigo)
        resultado = formatear_resultado(tokens, errores, codigo)
        self._log_resultado(resultado)

        estado = "Análisis léxico exitoso ✓" if not errores else f"{len(errores)} error(es) léxico(s) ✗"
        archivo = os.path.basename(self.archivo_actual) if self.archivo_actual else "Sin archivo"
        self.barra_estado.config(
            text=f"  {estado}   |   {archivo}",
            bg="#16a34a" if not errores else "#c0392b"
        )

    def abrir_automatas(self):
        """Abre la ventana de autómatas AFD y AFND."""
        win = tk.Toplevel(self.root)
        win.title("Autómatas AFD y AFND - MicroC Compiler")
        win.geometry("950x700")
        win.configure(bg="#1e1e1e")

        # ── Título ──
        tk.Label(win, text="  AUTÓMATAS AFD y AFND",
                 bg="#0078d4", fg="white",
                 font=("Segoe UI", 12, "bold"),
                 anchor="w", padx=10, pady=6).pack(fill=tk.X)

        # ── Panel ARRIBA: ingresar expresión propia ──
        frame_custom = tk.Frame(win, bg="#1a1a2e")
        frame_custom.pack(fill=tk.X, padx=0, pady=0)

        tk.Label(frame_custom,
                 text="  ✏  INGRESAR EXPRESIÓN PROPIA",
                 bg="#1a1a2e", fg="#f39c12",
                 font=("Segoe UI", 9, "bold"),
                 anchor="w").pack(fill=tk.X, padx=10, pady=(6, 2))

        fila1 = tk.Frame(frame_custom, bg="#1a1a2e")
        fila1.pack(fill=tk.X, padx=10, pady=2)

        tk.Label(fila1, text="Expresión regular:",
                 bg="#1a1a2e", fg="#9cdcfe",
                 font=("Segoe UI", 9), width=18, anchor="w").pack(side=tk.LEFT)

        self._expr_entry = tk.Entry(fila1, bg="#252526", fg="#f0f0f0",
                                    insertbackground="white",
                                    font=("Courier New", 11), width=35,
                                    relief="flat", bd=4)
        self._expr_entry.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(fila1,
                 text="Ej: (a|b)*  /  ab+a  /  (0|1)+",
                 bg="#1a1a2e", fg="#555577",
                 font=("Segoe UI", 8)).pack(side=tk.LEFT)

        fila2 = tk.Frame(frame_custom, bg="#1a1a2e")
        fila2.pack(fill=tk.X, padx=10, pady=(2, 8))

        tk.Label(fila2, text="Cadena a validar:",
                 bg="#1a1a2e", fg="#9cdcfe",
                 font=("Segoe UI", 9), width=18, anchor="w").pack(side=tk.LEFT)

        self._cadena_entry = tk.Entry(fila2, bg="#252526", fg="#f0f0f0",
                                      insertbackground="white",
                                      font=("Courier New", 11), width=35,
                                      relief="flat", bd=4)
        self._cadena_entry.pack(side=tk.LEFT, padx=(0, 10))
        self._cadena_entry.bind("<Return>",
                                lambda e: self._validar_personalizado(txt_detalle))

        tk.Button(fila2, text="▶  Analizar y Validar",
                  command=lambda: self._validar_personalizado(txt_detalle),
                  bg="#f39c12", fg="#1e1e1e", relief="flat", padx=12, pady=4,
                  cursor="hand2",
                  font=("Segoe UI", 9, "bold")).pack(side=tk.LEFT, padx=(0, 10))

        tk.Button(fila2, text="Limpiar",
                  command=lambda: [self._expr_entry.delete(0, "end"),
                                   self._cadena_entry.delete(0, "end"),
                                   self._log_automata(txt_detalle,
                                   "  Campos limpiados. Ingresá una nueva expresión.")],
                  bg="#555555", fg="white", relief="flat", padx=8, pady=4,
                  cursor="hand2",
                  font=("Segoe UI", 9)).pack(side=tk.LEFT)

        # ── Separador ──
        tk.Frame(win, bg="#0078d4", height=2).pack(fill=tk.X)

        # ── Panel MEDIO: resultado (textbox grande) ──
        frame_mid = tk.Frame(win, bg="#252526", bd=1, relief="solid")
        frame_mid.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        txt_detalle = tk.Text(frame_mid, bg="#0d1117", fg="#58a6ff",
                              font=("Courier New", 10), bd=0, padx=8, pady=8,
                              state="disabled", wrap="word")
        txt_detalle.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc = tk.Scrollbar(frame_mid, command=txt_detalle.yview)
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        txt_detalle.config(yscrollcommand=sc.set)

        # Mensaje inicial
        self._log_automata(txt_detalle,
            "  Bienvenido al módulo de Autómatas AFD y AFND\n\n"
            "  → Ingresa una expresión regular y una cadena para validar\n\n"
            "  AFD  = Autómata Finito Determinista\n"
            "         Desde cada estado hay exactamente UN camino por símbolo\n\n"
            "  AFND = Autómata Finito No Determinista\n"
            "         Desde un estado puede haber MÁS DE UN camino por símbolo\n"
            "         (causado por | ? * en la expresión regular)\n\n"
            "  RELACIÓN CON EL COMPILADOR:\n"
            "  Cada patrón del TOKEN_SPEC es un autómata.\n"
            "  Python detecta si es AFD o AFND según la expresión,\n"
            "  y convierte internamente los AFND a AFD para ejecutarlos."
        )

    def _log_automata(self, txt, texto):
        txt.config(state="normal")
        txt.delete("1.0", "end")
        txt.insert("end", texto)
        txt.config(state="disabled")

    def _validar_personalizado(self, txt):
        expr   = self._expr_entry.get().strip()
        cadena = self._cadena_entry.get()
        if not expr:
            self._log_automata(txt, "  ⚠ Ingresá una expresión regular primero.\n\n"
                               "  Ejemplos:\n"
                               "    (a|b)*     → AFND\n"
                               "    ab+a       → AFD\n"
                               "    (0|1)+     → AFND\n"
                               "    a?b+       → AFND")
            return
        resultado = analizar_automata_personalizado(expr, cadena)
        self._log_automata(txt, resultado)

    def ayuda(self):
        self._log_resultado(
            "=" * 50 + "\n"
            "  AYUDA - MicroC Compiler v3.0\n"
            "-" * 50 + "\n"
            "  Nuevo    → Crear nuevo archivo\n"
            "  Abrir    → Cargar archivo .C\n"
            "  Guardar  → Guardar archivo .C\n"
            "  Editar   → Habilitar edición\n"
            "  Compilar → Ejecutar análisis léxico (F5)\n"
            "  Salir    → Cerrar aplicación\n"
            "-" * 50 + "\n"
            "  El analizador léxico identifica:\n"
            "  Palabras reservadas, identificadores,\n"
            "  números enteros/reales, operadores,\n"
            "  delimitadores, cadenas y comentarios.\n"
            "  Cada token muestra su número de token\n"
            "  según la tabla de UnidadesLexicas.\n"
            "=" * 50
        )

    def acerca_de(self):
        messagebox.showinfo(
            "Acerca de MicroC Compiler",
            "MicroC Compiler v3.0\n"
            "Análisis Léxico — Etapa 1 Y Etapa 2\n\n"
            "Proyecto para el curso de Autómatas y Lenguajes\n\n"
            "Creada por:\n"
            "Rosa Andrea Fernanda Torres Del Aguila\n"
            "Carné: 202425516\n\n"
            "Universidad Mesoamericana — 2026"
        )

    def abrir_github(self):
        import webbrowser
        webbrowser.open("https://github.com/andrea10-baa/Compilador-MicroC-AnalizadorLexico-RosaTorres")

    def salir(self):
        if not self._confirmar_guardar():
            return
        self.root.destroy()


# ─────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = MicroCCompiler(root)
    root.mainloop()
