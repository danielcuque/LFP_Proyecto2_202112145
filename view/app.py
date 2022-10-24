from platform import system
from tkinter import (
    filedialog,
    Menu,
    messagebox,
    Text,
    ttk,
)


import customtkinter as ctk
from typing import List

# Data
from controller.lexer import Lexer
from controller.parser import Error, Parser
from controller.token import Token
from model.docs.generate_html import GenerateHTML

# Model
from model.helpers.WindowPosition import get_window_position
from model.helpers.ManageInformation import (
    read_information,
    save_information
)
from view.token_table import TokenTable

# # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")

# # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    # Size of the window
    APP_WIDTH: int = 1400
    APP_HEIGHT: int = 700

    PATH_FILE: str = ""
    VALID_TOKENS: List[Token] = []
    INVALID_TOKENS: List[Token] = []
    PARSER_ERROR: List[Error] = []

    def __init__(self):
        super().__init__()

        # Set minimum size of window
        self.minsize(self.APP_WIDTH, self.APP_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.command_to_execute = ""
        my_os = system()

        if my_os == "Windows":
            self.command_to_execute = "Ctrl"
        elif my_os == "Darwin":
            self.command_to_execute = "Cmd"

        # Position of the app
        self.geometry(get_window_position(self.winfo_screenwidth(
        ), self.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

        self.title("Analizador")

        self.create_menu()

        # Custom grid layout (3x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, minsize=12)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, minsize=100)

        self.info_label = ctk.CTkLabel(
            self, text=f"Archivo: Ninguno ", text_font=("Arial", 12))
        self.info_label.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ''' ====== Information frame ====== '''
        self.entry_information = Text(self, width=50)
        self.entry_information.grid(
            row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.create_error_frame()
        self.create_short_cut()

    def create_menu(self) -> None:
        # Menu
        self.menu_options = Menu(self)
        self.configure(menu=self.menu_options)

        # Menu File

        self.file_menu = Menu(self.menu_options, tearoff=0)
        self.file_menu.add_command(label='Nuevo archivo de texto', command=self.new_file,
                                   accelerator=f"{self.command_to_execute}+n")

        self.file_menu.add_separator()

        self.file_menu.add_command(label="Abrir...", command=self.open_file,
                                   accelerator=f"{self.command_to_execute}+O")

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Guardar", command=self.save_file, accelerator=f'{self.command_to_execute}+S')
        self.file_menu.add_command(
            label="Guardar como", command=self.save_file_as, accelerator=f"{self.command_to_execute}+Shift+S")

        self.file_menu.add_separator()
        self.file_menu.add_command(
            label='Salir', command=self.destroy, accelerator=f"{self.command_to_execute}+Q")

        # Menu Tools
        self.analizer_menu = Menu(self.menu_options, tearoff=0)
        self.analizer_menu.add_command(
            label='Ejecutar', command=self.run_program, accelerator=f"{self.command_to_execute}+r")

        # Menu Tokens
        self.tokens_menu = Menu(self.menu_options, tearoff=0)
        self.tokens_menu.add_command(
            label='Ver tokens', command=self.show_tokens, accelerator=f"{self.command_to_execute}+t")

        # Add menus to menu bar
        self.exit_menu = Menu(self.menu_options, tearoff=0)
        self.exit_menu.add_command(
            label="Salir", command=self.destroy, accelerator=f"{self.command_to_execute}+q")

        # Adding menus to menu bar
        self.menu_options.add_cascade(label="Archivo", menu=self.file_menu)
        self.menu_options.add_cascade(
            label="Analizador", menu=self.analizer_menu)
        self.menu_options.add_cascade(
            label='Tokens', menu=self.tokens_menu)

    def create_error_frame(self) -> None:
        self.treeview = ttk.Treeview(self)

        self.treeview['columns'] = (
            'Tipo de error',
            'Posición',
            'Se esperaba',
            'Descripción del error'
        )

        self.treeview.column("#0", width=0, stretch="NO")
        self.treeview.column("Tipo de error", anchor="w", width=50)
        self.treeview.column("Posición", anchor="w", width=80)
        self.treeview.column("Se esperaba", anchor="w")
        self.treeview.column("Descripción del error",
                             anchor="w")

        self.treeview.heading("#0", text="", anchor="center")
        self.treeview.heading(
            "Tipo de error", text="Tipo de error", anchor="w")
        self.treeview.heading("Posición", text="Posición", anchor="w")
        self.treeview.heading("Se esperaba", text="Se esperaba", anchor="w")
        self.treeview.heading("Descripción del error",
                              text="Descripción del error", anchor="w")

        self.treeview.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

    def destroy(self):
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            if self.PATH_FILE:
                self.save_file()
            super().destroy()

    def generate_code(self) -> None:
        if self.PATH_FILE and len(self.VALID_TOKENS) > 0:
            doc = GenerateHTML(self.VALID_TOKENS, self.PATH_FILE)
            doc.generate_file()
            messagebox.showinfo(
                "Código generado", "El código ha sido generado correctamente")

        else:
            messagebox.showerror(
                "Error", "No se ha generado ningún código")

    def list_errors(self) -> None:
        self.treeview.delete(*self.treeview.get_children())

        for error_lexicon in self.INVALID_TOKENS:
            self.treeview.insert('', 'end', text="", values=(
                'Léxico',
                f'Fila: {error_lexicon.row}, Columna: {error_lexicon.column}',
                '',
                f'La expresión {str(error_lexicon)} no es valido'
            ))

        for error in self.PARSER_ERROR:
            self.treeview.insert('', 'end', text="", values=(
                'Sintáctico',
                f'Fila: {error.token.row}, Columna: {error.token.column}',
                str(error),
                'Sentencia mal formada'
            ))

    def new_file(self) -> None:
        if self.entry_information.get("1.0", "end-1c"):
            if messagebox.askyesno("Nuevo archivo", "¿Desea guardar el archivo actual?"):
                self.save_file()
            self.entry_information.delete("1.0", "end")
        self.save_file_as()

    def open_file(self):
        path_file = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.gpw"), ("all files", "*.*")))
        if len(path_file) <= 0:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
        else:
            self.PATH_FILE = path_file
            uploaded_information: str = read_information(
                self.PATH_FILE)
            self.show_info_file(uploaded_information)

    def show_info_file(self, uploaded_information: str):
        self.entry_information.delete("1.0", "end")
        self.entry_information.insert("1.0", uploaded_information)
        self.refresh_path_file()

    def save_file(self):
        if self.PATH_FILE:
            information: str = self.entry_information.get("1.0", "end-1c")
            save_information(self.PATH_FILE, information)
        else:
            self.save_file_as()

    def save_file_as(self):
        path_to_save = filedialog.asksaveasfilename(
            initialdir="/", title="Guardar como", filetypes=(("Text files", "*.gpw"), ("all files", "*.*")))
        if len(path_to_save) > 0:
            information: str = self.entry_information.get("1.0", "end-1c")
            save_information(path_to_save, information)
            self.PATH_FILE = path_to_save

        self.refresh_path_file()

    def show_tokens(self) -> None:
        if len(self.INVALID_TOKENS) > 0 or len(self.VALID_TOKENS) > 0:
            all_tokens: List[Token] = self.VALID_TOKENS + self.INVALID_TOKENS
            TokenTable(self, all_tokens)
        else:
            messagebox.showerror(
                "Error", "Ejecute el analizador para ver los tokens")

    def refresh_path_file(self) -> None:
        self.info_label.configure(text=f'Archivo: {self.PATH_FILE}')

    def run_program(self):
        code: str = self.entry_information.get("1.0", "end-1c")
        if code:
            lexer: Lexer = Lexer(code)
            lexer.fill_table_of_tokens()
            self.INVALID_TOKENS = lexer.get_invalid_tokens()
            self.VALID_TOKENS = lexer.get_valid_tokens()

            if len(self.VALID_TOKENS) > 0:
                parser: Parser = Parser(self.VALID_TOKENS)
                parser.parse_programm()
                self.PARSER_ERROR = parser.errors

            self.list_errors()

            if len(self.INVALID_TOKENS) == 0 and len(self.PARSER_ERROR) == 0:
                self.generate_code()

        else:
            messagebox.showerror("Error", "No hay código para analizar")

    def create_short_cut(self):
        # Meny Files
        self.bind_all("<Command-n>", lambda event: self.new_file())
        self.bind_all("<Command-o>", lambda event: self.open_file())
        self.bind_all("<Command-s>", lambda event: self.save_file())
        self.bind_all("<Command-Shift-s>", lambda event: self.save_file_as())

        # Menu Analizer
        self.bind_all("<Command-r>", lambda event: self.run_program())

        # Menu Tokens
        self.bind_all("<Command-t>", lambda event: self.show_tokens())
