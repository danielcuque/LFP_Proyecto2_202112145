from typing import List, cast
from unittest import TestCase

from controller.lexer import Lexer
from controller.parser import Parser


class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = '''
        <!-- Controles
        Contenedor contlogin;
        Contenedor contFondo;
        Boton cmdIngresar;
        Clave pswClave;

        Controles -->
        '''

        lexer = Lexer(source)

        lexer.fill_table_of_tokens()

        parser = Parser(lexer.get_valid_tokens())

        

        
