from typing import List

from tkinter import ttk
import customtkinter as ctk

from controller.token import Token

# # Modes: "System" (standard), "Dark", "Light"


class TokenTable(ctk.CTkToplevel):
    def __init__(self, parent, tokens: List[Token]):
        super().__init__(parent)

        self.title("Tabla de tokens")
        self.geometry("800x600")
        self.resizable(False, False)

        self.tokens = tokens

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_table()

    def create_table(self):
        self.treeview = ttk.Treeview(self)

        self.treeview['columns'] = (
            'Correlativo',
            'Tipo',
            'Lexema'
        )

        self.treeview.column("#0", width=0, stretch="NO")
        self.treeview.column("Correlativo", anchor="w")
        self.treeview.column("Tipo", anchor="w")
        self.treeview.column("Lexema", anchor="w")

        self.treeview.heading("#0", text="", anchor="center")
        self.treeview.heading(
            "Correlativo", text="Correlativo", anchor="w")
        self.treeview.heading("Tipo", text="Tipo", anchor="w")
        self.treeview.heading("Lexema", text="Lexema", anchor="w")
        self.show_tokens()

        self.treeview.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def show_tokens(self):
        for index in range(len(self.tokens)):
            self.treeview.insert(
                "", "end", text="", values=(str(index), self.tokens[index].token_type.name, self.tokens[index].literal))
