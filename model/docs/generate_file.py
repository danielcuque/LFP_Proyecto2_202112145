from tkinter import filedialog
from typing import List, Tuple, Optional
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

from ..helpers.utils import (
    lookup_justify,
)


class GenerateFile:
    def __init__(self, table_of_tokens: List[Token], path_file: str) -> None:
        self._table_of_tokens = table_of_tokens
        self._table_of_symbols: List[ObjectHTML] = []
        self._controls: List[Token] = []
        self._properties: List[Token] = []
        self._positon: List[Token] = []
        self.path_file = path_file

        self._body_container: List[ObjectHTML] = []
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

    @staticmethod
    def _lookup_prop(list_to_search: List, index: int, position: int) -> Token:
        return list_to_search[index+position]

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
                    clave: TextField = TextField(self._controls[index + 1])
                    clave.set_is_password(True)
                    self._table_of_symbols.append(clave)
                elif literal == 'contenedor':
                    self._table_of_symbols.append(
                        Container(self._controls[index + 1]))
                elif literal == 'areatexto':
                    self._table_of_symbols.append(
                        TextArea(self._controls[index + 1]))

        self._set_properties()
        self._set_position()

    def _set_properties(self) -> None:
        for index in range(len(self._properties)):
            token: Token = self._properties[index]
            if token.token_type == TokenType.IDENT:
                object_html: ObjectHTML = self._search_object(token.literal)
                if object_html is not None:
                    current_function: str = self._lookup_prop(
                        self._properties, index, 2).literal
                    if current_function == 'setAncho':
                        object_html.set_width(
                            int(self._lookup_prop(self._properties, index, 4).literal))
                        continue

                    elif current_function == 'setAlto':
                        object_html.set_height(
                            int(self._lookup_prop(self._properties, index, 4).literal))
                        continue

                    elif current_function == 'setColorFondo':
                        background_colors: Tuple[int, int, int] = (
                            int(self._lookup_prop(
                                self._properties, index, 4).literal),
                            int(self._lookup_prop(
                                self._properties, index, 6).literal),
                            int(self._lookup_prop(self._properties, index, 8).literal))
                        object_html.set_background_color(background_colors)
                        continue

                    elif current_function == 'setTexto':
                        object_html.set_text(
                            self._lookup_prop(self._properties, index, 4).literal)
                        continue
                    elif current_function == 'setAlineacion':
                        object_html.set_justify(
                            self._lookup_prop(self._properties, index, 4).literal)
                        continue
                    elif current_function == 'setColorLetra':
                        color: Tuple[int, int, int] = (
                            int(self._lookup_prop(
                                self._properties, index, 4).literal),
                            int(self._lookup_prop(
                                self._properties, index, 6).literal),
                            int(self._lookup_prop(self._properties, index, 8).literal))
                        object_html.set_color_letter(color)
                        continue
                    elif current_function == 'setMarcada':
                        operator: str = self._lookup_prop(
                            self._properties, index, 4).literal
                        if operator.lower() == 'true':
                            object_html.set_checked(True)
                        continue
                    elif current_function == 'setGrupo':
                        object_html.set_group(
                            self._lookup_prop(self._properties, index, 4))
                        continue

    def _set_position(self) -> None:
        for index in range(len(self._positon)):
            token: Token = self._positon[index]
            if token.token_type == TokenType.IDENT:
                current_function: str = self._lookup_prop(
                    self._positon, index, 2).literal
                if current_function == 'add':
                    object_html: ObjectHTML = self._search_object(
                        self._lookup_prop(self._positon, index, 4).literal)
                    if token.literal == 'this':
                        self._body_container.append(object_html)
                    else:
                        container: Optional[Container] = self._search_object(
                            token.literal)
                        container.add(object_html)

                elif current_function == 'setPosicion':
                    object_html: ObjectHTML = self._search_object(
                        token.literal)
                    if object_html is not None:
                        position: Tuple[int, int] = (
                            int(self._lookup_prop(self._positon, index, 4).literal), int(self._lookup_prop(self._positon, index, 6).literal))
                        object_html.set_position(position)
                        object_html._is_absolute = True

    def _search_object(self, name: str) -> Optional[ObjectHTML]:
        for object_html in self._table_of_symbols:
            if object_html.get_id() == name:
                return object_html
        return None

    def _get_css_code(self) -> str:
        content: str = ''
        for object_html in self._table_of_symbols:
            content += f'#{object_html.get_id()} {{\n' \
                       f'width:{object_html.width}px;\n' \
                       f'height:{object_html.height}px;\n' \

            if object_html.get_is_absolute():
                content += f'position:absolute;\n' \

            if type(object_html.background_color) is tuple:
                content += f'background-color: rgb{object_html.background_color[0], object_html.background_color[1], object_html.background_color[2]};\n' \

            if type(object_html.get_position()) is tuple:
                content += f'left:{object_html.get_position()[0]}px;\n' \
                           f'top:{object_html.get_position()[1]}px;\n'

            if isinstance(object_html, Tag):
                content += f'color: rgb{object_html.color_letter[0], object_html.color_letter[1], object_html.color_letter[2]};\n' \
                    f'font-size: 12px;\n' \


            content += f'}}\n'

        return content

    @staticmethod
    def _get_button(button: Button) -> str:
        return f'<input type="submit" id="{button.get_id()}" value="{button.text}" style="text-align: {lookup_justify(button.justify)}" />\n'

    @staticmethod
    def _get_checkbox(checkbox: CheckBox) -> str:
        checked: str = 'checked' if checkbox.checked else ''
        return f'<input type="checkbox" id="{checkbox.get_id()}" value="{checkbox.text}" ' \
               f'{checked} > {checkbox.text} </input>\n'

    def _get_container(self, container: Container) -> str:
        content: str = ""
        for object_html in container.controls:
            if isinstance(object_html, Button):
                content += self._get_button(object_html)
            elif isinstance(object_html, CheckBox):
                content += self._get_checkbox(object_html)
            elif isinstance(object_html, Tag):
                content += self._get_tag(object_html)
            elif isinstance(object_html, RadioButton):
                content += self._get_radio_button(object_html)
            elif isinstance(object_html, TextField):
                content += self._get_text_field(object_html)
            elif isinstance(object_html, TextArea):
                content += self._get_text_area(object_html)
            elif isinstance(object_html, Container):
                content += self._get_container(object_html)
        return f'<div id="{container.get_id()}"> {content} </div>'

    @staticmethod
    def _get_radio_button(radiobutton: RadioButton) -> str:
        checked: str = 'checked' if radiobutton.checked else ''
        return f'<input type="radio" id="{radiobutton.get_id()}" name="{radiobutton.group.literal}" {checked} > {radiobutton.text} </input>\n'

    @staticmethod
    def _get_tag(tag: Tag) -> str:
        return f'<label id="{tag.get_id()}">{tag.text}</label>\n'

    @staticmethod
    def _get_text_area(textarea: TextArea) -> str:
        return f'<textarea id="{textarea.get_id()}">{textarea.text}</textarea>\n'

    @staticmethod
    def _get_text_field(textfield: TextField) -> str:
        input_type: str = "text"
        if textfield.is_password:
            input_type = "password"
        return f'<input type="{input_type}" id="{textfield.get_id()}" value="{textfield.text}"/>\n'

    def _header_html(self) -> str:
        header: str = f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <link rel="stylesheet" href="{self._get_name_file()}.css">
            <title>{self._get_name_file()}</title>
        </head>
        '''
        return header

    def body_html(self) -> str:
        body: str = f'''
        <body>
            {self._generate_body()}
            </body>
        </html>
        '''
        return body

    def _get_name_file(self) -> str:
        return self.path_file.split('/')[-1].split('.')[0]

    def _generate_body(self) -> str:
        content: str = ""
        for control in self._body_container:
            if isinstance(control, Button):
                content += self._get_button(control)
            elif isinstance(control, CheckBox):
                content += self._get_checkbox(control)
            elif isinstance(control, Tag):
                content += self._get_tag(control)
            elif isinstance(control, RadioButton):
                content += self._get_radio_button(control)
            elif isinstance(control, TextField):
                content += self._get_text_field(control)
            elif isinstance(control, TextArea):
                content += self._get_text_area(control)
            elif isinstance(control, Container):
                content += self._get_container(control)
        return content

    def generate_file(self) -> None:
        path_file: str = filedialog.askdirectory()
        if path_file != '':
            self._generate_html(path_file)
            self._generate_css_file(path_file)

    def _generate_html(self, path_file: str) -> None:
        name_file: str = self._get_name_file()
        with open(f'{path_file}/{name_file}.html', 'w') as file:
            file.write(self._header_html())
            file.write(self.body_html())
            file.close()

    def _generate_css_file(self, path_file: str) -> None:
        name_file: str = self._get_name_file()
        with open(f'{path_file}/{name_file}.css', 'w') as file:
            file.write(self._get_css_code())
            file.close()
