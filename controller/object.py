from .token import Token


class ObjectHTML:
    def __init__(self, id_control: Token) -> None:
        self.id_control = id_control


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

class Button(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = "center"

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify

class CheckBox(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.checked: bool = False
        self.group: str = ""

    def set_text(self, text: str) -> None:
        self.text = text

    def set_checked(self, checked: bool) -> None:
        self.checked = checked
    
    def set_group(self, group: str) -> None:
        self.group = group

class RadioButton(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.checked: bool = False
        self.group: str = ""

    def set_text(self, text: str) -> None:
        self.text = text

    def set_checked(self, checked: bool) -> None:
        self.checked = checked
    
    def set_group(self, group: str) -> None:
        self.group = group

class TextField(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = "center"

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify

class TextArea(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.text: str = ""
        self.justify: str = "center"

    def set_text(self, text: str) -> None:
        self.text = text

    def set_justify(self, justify: str) -> None:
        self.justify = justify

class Container(ObjectHTML):
    def __init__(self, id_control: Token) -> None:
        super().__init__(id_control)
        self.color_background: str = "white"
        self.controls: list[ObjectHTML] = []
        self.height: int = 0
        self.width: int = 0

    def set_color_background(self, color: str) -> None:
        self.color_background = color

    def add_control(self, control: ObjectHTML) -> None:
        self.controls.append(control)
    
    def set_height(self, height: int) -> None:
        self.height = height
    
    def set_width(self, width: int) -> None:
        self.width = width
    
