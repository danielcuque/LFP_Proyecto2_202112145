from typing import List, Tuple
from .token import Token


class ObjectHTML:
    def __init__(self, id_control: Token) -> None:
        self.id_control = id_control
        self.background_color = (255, 255, 255)
        self.group: Token = None
        self.height = 100
        self.width = 100
        self._position: Tuple[int, int] = (0, 0)

    def get_id(self) -> str:
        return self.id_control.literal

    def set_width(self, width: int) -> None:
        self.width = width

    def set_height(self, height: int) -> None:
        self.height = height

    def set_background_color(self, colors: Tuple) -> None:
        self.background_color = colors

    def set_group(self, group: Token) -> None:
        self.group = group

    def set_position(self, position: Tuple[int, int]) -> None:
        self._position = position

    def get_group(self) -> str:
        return self.group.literal

    def __str__(self) -> str:
        return f'{self.id_control.literal}'


class Button(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = ""

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify


class CheckBox(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.checked: bool = False
        self.text: str = ""

    def set_text(self, text: str) -> None:
        self.text = text

    def set_checked(self, checked: bool) -> None:
        self.checked = checked


class Container(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.color_background: str = "white"
        self.controls: List[ObjectHTML] = []

    def add(self, control: ObjectHTML) -> None:
        self.controls.append(control)

    def set_color_background(self, color: str) -> None:
        self.color_background = color

    def set_height(self, height: int) -> None:
        self.height = height

    def set_width(self, width: int) -> None:
        self.width = width


class RadioButton(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.checked: bool = False
        self.text: str = ""

    def set_text(self, text: str) -> None:
        self.text = text

    def set_checked(self, checked: bool) -> None:
        self.checked = checked


class Tag(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.color_letter: str = "black"
        self.text: str = ""
        self.color_background: str = "white"

    def set_text(self, text: str) -> None:
        self.text = text

    def set_color_letter(self, color: str) -> None:
        self.color_letter = color

    def set_color_background(self, color: str) -> None:
        self.color_background = color


class TextArea(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = "center"
        self.width: int = 150
        self.height: int = 150

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify


class TextField(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = "center"
        is_password: bool = False

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify

    def set_is_password(self, is_password: bool) -> None:
        self.is_password = is_password
