from tkinter import filedialog
from typing import List, Tuple
from controller.token import Token, TokenType
from controller.object import (
    Button,
    CheckBox,
    Container,
    ObjectHTML,
    Tag,
    TextArea,
    TextField,
    RadioButton,
)


class GenerateHTML:
    def __init__(self, table_of_tokens: List[Token], path_file: str) -> None:
        self._table_of_tokens = table_of_tokens
        self._table_of_symbols: List[ObjectHTML] = []
        self._controls: List[Token] = []
        self._properties: List[Token] = []
        self._positon: List[Token] = []
        self.path_file = path_file
        self._fill_blocks_of_wrappers()

    def _fill_blocks_of_wrappers(self) -> None:
        current_wrapper: str = ''
        for token in self._table_of_tokens:
            token: Token
            if token.token_type == TokenType.WRAPPER:
                current_wrapper = token.literal
                continue

            if current_wrapper.lower() == 'controles':
                self._controls.append(token)
            elif current_wrapper.lower() == 'propiedades':
                self._properties.append(token)
            elif current_wrapper.lower() == 'colocacion':
                self._positon.append(token)

        self._generate_objects()

    def _lookup_prop(self, index: int, position: int) -> Token:
        return self._properties[index+position]

    def _generate_objects(self) -> str:
        for index in range(len(self._controls)):
            token: Token = self._controls[index]
            literal = token.literal.lower()
            if token.token_type == TokenType.CONTROL:
                if literal == 'boton':
                    self._table_of_symbols.append(
                        Button(self._controls[index + 1]))
                elif literal == 'check':
                    self._table_of_symbols.append(
                        CheckBox(self._controls[index + 1]))
                elif literal == 'etiqueta':
                    self._table_of_symbols.append(
                        Tag(self._controls[index + 1]))
                elif literal == 'radioboton':
                    self._table_of_symbols.append(
                        RadioButton(self._controls[index + 1]))
                elif literal == 'texto':
                    self._table_of_symbols.append(
                        TextField(self._controls[index + 1]))
                elif literal == 'clave':
                    self._table_of_symbols.append(
                        TextArea(self._controls[index + 1]))
                elif literal == 'contenedor':
                    self._table_of_symbols.append(
                        Container(self._controls[index + 1]))
                elif literal == 'areatexto':
                    self._table_of_symbols.append(
                        TextArea(self._controls[index + 1]))

        self._set_properties()

    def _set_properties(self) -> None:
        for index in range(len(self._properties)):
            token: Token = self._properties[index]
            if token.token_type == TokenType.IDENT:
                object_html: ObjectHTML = self._search_object(token.literal)
                if object_html is not None:
                    current_function: str = self._lookup_prop(index, 2).literal
                    if current_function == 'setAncho':
                        object_html.set_width(
                            int(self._lookup_prop(index, 4).literal))
                        continue

                    elif current_function == 'setAlto':
                        object_html.set_height(
                            int(self._lookup_prop(index, 4).literal))
                        continue

                    elif current_function == 'setColorFondo':
                        background_colors: Tuple[str, str] = (
                            self._lookup_prop(index, 4), self._lookup_prop(index, 6), self._lookup_prop(index, 8))
                        object_html.set_background_color(background_colors)
                        continue

                    elif current_function == 'setTexto':
                        object_html.set_text(
                            self._lookup_prop(index, 4).literal)
                        continue
                    elif current_function == 'setAlineacion':
                        object_html.set_align(
                            self._lookup_prop(index, 4).literal)
                        continue
                    elif current_function == 'setColorLetra':
                        color: Tuple[str, str] = (
                            self._lookup_prop(index, 4).literal, self._lookup_prop(index, 6).literal)
                        object_html.set_color_letter(color)
                        continue
                    elif current_function == 'setMarcada':
                        object_html.set_checked(True)
                        continue
                    elif current_function == 'setGrupo':
                        object_html.set_group(
                            self._lookup_prop(index, 4))
                        continue

                    # if type(object_html) == Button:
                    #     pass
                    # elif type(object_html) == CheckBox:
                    #     pass
                    # elif type(object_html) == Container:
                    #     pass
                    # elif type(object_html) == Tag:
                    #     pass
                    # elif type(object_html) == RadioButton:
                    #     pass
                    # elif type(object_html) == TextField:
                    #     pass
                    # elif type(object_html) == TextArea:
                    #     pass
    
    def _set_position(self) -> None:
        pass

    def _search_object(self, name: str) -> ObjectHTML:
        for object_html in self._table_of_symbols:
            if object_html.get_id() == name:
                return object_html
        return None

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

    def _get_name_file(self) -> str:
        return self.path_file.split('/')[-1].split('.')[0]

    def _generate_body(self) -> str:
        pass

    def generate_file(self) -> None:
        path_file: str = filedialog.askdirectory()
        if path_file != '':
            pass
