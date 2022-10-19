from typing import List, cast
from unittest import TestCase

from controller.lexer import Lexer
from controller.parser import Parser
from controller.ast import (
    BlockStatement,
    Program,
    Statement,
    Expression,
)


class ParserTest(TestCase):
    def test_parse(self):
        source: str = '''
        <-- Controles
        Boton btn1;
        Controles -->
        '''

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self.assertIsNotNone(program)
        self.assertIsInstance(program, Program)

    # This represent the state 1 of the parser
    def test_let_statement(self) -> None:
        source: str = '''
        Boton btn1;
        Etiqueta Etiqueta1;
        Contenedor contenedor1;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        names: List[str] = []
        for statement in program.statements:
            statement = cast(BlockStatement, statement)
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: List[str] = ['btn1', 'Etiqueta1', 'contenedor1']

        self.assertEqual(names, expected_names)

    def test_errors(self) -> None:
        source: str = '''
        Boton btn1;
        Boton;
        '''

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        parser.parse_program()
        print(parser.errors)

        self.assertEqual(len(parser.errors), 1)

    def test_block_statement(self) -> None:
        source: str = '''
        <!-- Controles 
        Boton btn1;
        Boton btn2;
        Boton btn3;
        Boton btn4;
        Controles
        -->
        '''

        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 1)

        for statement in program.statements:
            self.assertIsInstance(statement, Statement)

