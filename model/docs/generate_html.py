from typing import List
from controller.token import Token
from controller.object import (
    Button,
    CheckBox,
    Container,
    Tag,
    TextArea,
    TextField,
    RadioButton,
)


class GenerateHTML:
    def __init__(self, table_of_tokens: List[Token]) -> None:
        self._table_of_tokens = table_of_tokens
        self._symbol_table = []

    def crate_html_objects(self) -> None:
        for token in self._table_of_tokens:
            pass

    def header_html(self) -> str:
        header: str = ''''
        <html>
            <head>
            <link href="prueba.css" rel="stylesheet" type="text/css" />
            </head>
        '''

    def body_html(self) -> str:
        body: str = f'''
        <body>
        {self._generate_body()}
        </body>
        '''

    def _generate_body(self) -> str:
        pass
