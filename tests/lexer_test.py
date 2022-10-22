from unittest import TestCase

from typing import List

from controller.lexer import Lexer

from controller.token import (
    Token,
    TokenType,
)


class LexerTest(TestCase):

    def test_illegal_token(self) -> None:
        source: str = '!/<=>'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '!'),
            Token(TokenType.ILLEGAL, '/'),
            Token(TokenType.ILLEGAL, '<'),
            Token(TokenType.ILLEGAL, '='),
            Token(TokenType.ILLEGAL, '>'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source: str = '(),;'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_eof(self) -> None:
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(len(source) + 1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_comment_line(self) -> None:
        source: str = '// This is a comment'
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(1):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_comment_block(self) -> None:
        source: str = '''
        /*
        This is a comment
        */
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(3):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.OPEN_BLOCK_COMMENT, '/*'),
            Token(TokenType.CLOSE_BLOCK_COMMENT, '*/'),
            Token(TokenType.EOF, ''),

        ]

        self.assertEquals(tokens, expected_tokens)

    def test_line_comment_and_block_comment(self) -> None:

        source: str = '''
        // This is a comment
        // This is another comment
        /*
        Multi
        line
        comment/////
        /*
        52136789∑©√ß∂∫
        */
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(3):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.OPEN_BLOCK_COMMENT, '/*'),
            Token(TokenType.CLOSE_BLOCK_COMMENT, '*/'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_fail_multi_comment(self) -> None:
        source: str = '''
        /*
        This is a comment
        /*
        This is a comment
        */
        '''
        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []
        for i in range(3):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.OPEN_BLOCK_COMMENT, '/*'),
            Token(TokenType.CLOSE_BLOCK_COMMENT, '*/'),
            Token(TokenType.EOF, ''),

        ]

        self.assertEquals(tokens, expected_tokens)

    def test_control_statement(self) -> None:
        source: str = 'Boton1.setColorFondo(64, 64, 64);'

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(12):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'Boton1'),
            Token(TokenType.DOT, '.'),
            Token(TokenType.FUNCTION, 'setColorFondo'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '64'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.INT, '64'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.INT, '64'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_open_close_tag(self) -> None:

        source: str = '''
        <!-- 
        Controles 
        -->
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(4):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.OPEN_TAG, '<!--'),
            Token(TokenType.WRAPPER, 'Controles'),
            Token(TokenType.CLOSE_TAG, '-->'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_open_close_tag_bad(self) -> None:

        source: str = '''
        <!-
        Controles 
        ->
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(4):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '<!-'),
            Token(TokenType.WRAPPER, 'Controles'),
            Token(TokenType.ILLEGAL, '-'),
            Token(TokenType.ILLEGAL, '>'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_all_controls(self) -> None:
        source: str = '''
        <!--Controles
            Contenedor contlogin; 
            Contenedor contFondo; 
            Boton cmdIngresar; 
            Clave pswClave; 
            Etiqueta passw; 
            Etiqueta Nombre; 
            Texto Texto0; 
            Contenedor contlogo2; 
            Contenedor ContLogo1; 
            Contenedor ContBody;
        Controles-->
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(35):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.OPEN_TAG, '<!--'),
            Token(TokenType.WRAPPER, 'Controles'),
            Token(TokenType.CONTROL, 'Contenedor'),
            Token(TokenType.IDENT, 'contlogin'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Contenedor'),
            Token(TokenType.IDENT, 'contFondo'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Boton'),
            Token(TokenType.IDENT, 'cmdIngresar'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Clave'),
            Token(TokenType.IDENT, 'pswClave'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Etiqueta'),
            Token(TokenType.IDENT, 'passw'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Etiqueta'),
            Token(TokenType.IDENT, 'Nombre'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Texto'),
            Token(TokenType.IDENT, 'Texto0'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Contenedor'),
            Token(TokenType.IDENT, 'contlogo2'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Contenedor'),
            Token(TokenType.IDENT, 'ContLogo1'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.CONTROL, 'Contenedor'),
            Token(TokenType.IDENT, 'ContBody'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.WRAPPER, 'Controles'),
            Token(TokenType.CLOSE_TAG, '-->'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_strings(self) -> None:
        source: str = '''
            "Password 1";
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(2):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.STRING, "Password 1"),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_justify_values(self) -> None:
        source: str = '''
        boton1.setAlineacion(Centro);
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(7):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'boton1'),
            Token(TokenType.DOT, '.'),
            Token(TokenType.FUNCTION, 'setAlineacion'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.JUSTIFY, 'Centro'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_keywords(self) -> None:
        source: str = '''
        this.add(contFondo);
        '''

        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(7):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.IDENT, 'this'),
            Token(TokenType.DOT, '.'),
            Token(TokenType.FUNCTION, 'add'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'contFondo'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)
