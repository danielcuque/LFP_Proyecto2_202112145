from platform import system
from tkinter import (
    filedialog,
    Menu,
    messagebox,
    Text
)

import customtkinter as ctk
from typing import List

# Data
from controller.lexer import Lexer
from controller.token import Token

# Model
from model.helpers.WindowPosition import get_window_position
from model.helpers.ManageInformation import (
    read_information,
    save_information
)

# # Modes: "System" (standard), "Dark", "Light"
ctk.set_appearance_mode("dark")

# # Themes: "blue" (standard), "green", "dark-blue"
ctk.set_default_color_theme("blue")


class App(ctk.CTk):

    # Size of the window
    APP_WIDTH: int = 1096
    APP_HEIGHT: int = 700

    PATH_FILE: str = ""
    VALID_TOKENS: List[Token] = []
    INVALID_TOKENS: List[Token] = []
    RESULT_OF_OPERATIONS: List[str] = []

    def __init__(self):
        super().__init__()

        # Set minimum size of window
        self.minsize(self.APP_WIDTH, self.APP_HEIGHT)
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        command_to_execute = ""
        my_os = system()

        if my_os == "Windows":
            command_to_execute = "Ctrl"
        elif my_os == "Darwin":
            command_to_execute = "Cmd"

        # Position of the app
        self.geometry(get_window_position(self.winfo_screenwidth(
        ), self.winfo_screenheight(), self.APP_WIDTH, self.APP_HEIGHT))

        self.title("Analizador")

        # Custom grid layout (2x1)
        # create 2x1 grid system
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Menu
        self.menu_options = Menu(self)
        self.config(menu=self.menu_options)

        # Menu File
        self.file_menu = Menu(self.menu_options, tearoff=0)
        self.file_menu.add_command(label="Abrir", command=self.open_file,
                                   accelerator=f"{command_to_execute}+O")

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label="Guardar", command=self.save_file, accelerator=f'{command_to_execute}+S')
        self.file_menu.add_command(
            label="Guardar como", command=self.save_file_as, accelerator=f"{command_to_execute}+Shift+S")

        # Menu Tools
        self.scanner_menu = Menu(self.menu_options, tearoff=0)
        self.scanner_menu.add_command(
            label="Analizar", command=self.about_creator, accelerator=f"{command_to_execute}+r")
        self.scanner_menu.add_command(
            label="Resultados", command=self.about_creator, accelerator=f'{command_to_execute}+p')
        self.scanner_menu.add_command(
            label="Errores", command=self.about_creator, accelerator=f'{command_to_execute}+e')

        # Menu Help
        self.help_menu = Menu(self.menu_options, tearoff=0)
        self.help_menu.add_command(
            label="Guía de usuario", command=self.about_creator, accelerator=f"{command_to_execute}+U")
        self.help_menu.add_command(
            label="Guía técnica", command=self.about_creator, accelerator=f"{command_to_execute}+T")
        self.help_menu.add_command(
            label="Temas de ayuda", command=self.about_creator, accelerator=f'{command_to_execute}+t')

        # Add menus to menu bar
        self.exit_menu = Menu(self.menu_options, tearoff=0)
        self.exit_menu.add_command(
            label="Salir", command=self.destroy, accelerator=f"{command_to_execute}+q")

        # Adding menus to menu bar
        self.menu_options.add_cascade(label="Archivo", menu=self.file_menu)
        self.menu_options.add_cascade(
            label="Analizador", menu=self.scanner_menu)
        self.menu_options.add_cascade(label="Ayuda", menu=self.help_menu)
        self.menu_options.add_cascade(label="Salir", menu=self.exit_menu)

        ''' ====== Information frame ====== '''
        self.entry_information = Text(self, width=50)
        self.entry_information.grid(
            row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.create_short_cut()

    def destroy(self):
        if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
            if self.PATH_FILE:
                self.save_file()
            super().destroy()

    def new_file(self) -> None:
        self.PATH_FILE = ""
        if self.entry_information.get("1.0", "end-1c"):
            if messagebox.askyesno("Nuevo archivo", "¿Desea guardar el archivo actual?"):
                self.save_file()
            self.entry_information.delete("1.0", "end")

    def open_file(self):
        path_file = filedialog.askopenfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        if len(path_file) <= 0:
            messagebox.showerror(
                "Error", "No se ha seleccionado ningún archivo")
        else:
            self.PATH_FILE = path_file
            uploaded_information: str = read_information(
                self.PATH_FILE)

            if len(uploaded_information) <= 0:
                messagebox.showerror(
                    "Error", "No se ha podido cargar el archivo")
            else:
                self.show_info_file(uploaded_information)

    def show_info_file(self, uploaded_information: str):
        self.entry_information.insert("1.0", uploaded_information)

    def save_file(self):
        information: str = self.entry_information.get("1.0", "end-1c")
        save_information(self.PATH_FILE, information)

    def save_file_as(self):
        path_to_save = filedialog.asksaveasfilename(
            initialdir="/", title="Select file", filetypes=(("Text files", "*.txt"), ("all files", "*.*")))
        if len(path_to_save) > 0:
            information: str = self.entry_information.get("1.0", "end-1c")
            save_information(path_to_save, information)
            self.PATH_FILE = path_to_save

    def create_short_cut(self):
        # Meny Files
        self.bind_all('<Control-n>', self.new_file)
        self.bind_all('<Control-o>', self.open_file)
        self.bind_all('<Control-s>', self.save_file)
        self.bind_all('<Control-S>', self.save_file_as)