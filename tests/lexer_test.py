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

        print(tokens)

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
            Token(TokenType.IDENT, 'setColorFondo'),
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
            Token(TokenType.IDENT, 'Controles'),
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

        for i in range(3):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.ILLEGAL, '<!-'),
            Token(TokenType.IDENT, 'Controles'),
            Token(TokenType.ILLEGAL, '->'),
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
            Token(TokenType.IDENT, 'Controles'),
            Token(TokenType.IDENT, 'Contenedor'),
            Token(TokenType.IDENT, 'contlogin'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Contenedor'),
            Token(TokenType.IDENT, 'contFondo'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Boton'),
            Token(TokenType.IDENT, 'cmdIngresar'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Clave'),
            Token(TokenType.IDENT, 'pswClave'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Etiqueta'),
            Token(TokenType.IDENT, 'passw'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Etiqueta'),
            Token(TokenType.IDENT, 'Nombre'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Texto'),
            Token(TokenType.IDENT, 'Texto0'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Contenedor'),
            Token(TokenType.IDENT, 'contlogo2'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Contenedor'),
            Token(TokenType.IDENT, 'ContLogo1'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Contenedor'),
            Token(TokenType.IDENT, 'ContBody'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.IDENT, 'Controles'),
            Token(TokenType.CLOSE_TAG, '-->'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEquals(tokens, expected_tokens)

    def test_total_program(self) -> None:
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
            Controles -->

            <!--propiedades
            /*
            Definicion de propiedades
            */

            //#$inicio de contlogin 
            contlogin.setAncho(190); 
            contlogin.setAlto(150);
            contlogin.setColorFondo(47,79,79); 
            //#$fin de contlogin

            //#$inicio de contFondo 
            contFondo.setAncho(800);
            contFondo.setAlto(100); 
            contFondo.setColorFondo(64,64,64);
            //#$fin de contFondo

            //#$inicio de cmdIngresar 
            cmdIngresar.setTexto("Ingresar"); 
            contlogin.add(cmdIngresar);
            //#$fin de cmdIngresar

            //#$inicio de pswClave 
            pswClave.setTexto("");
            //#$fin de pswClave 

            //#$inicio de etiqueta passw
            passw.setAncho(53); 
            passw.setAlto(13 ); 
            passw.setColorLetra(128,128,128);
            passw.setTexto("Password");
            //#$fin de passw

            //#$inicio de Nombre
            Nombre.setAncho(44); 
            Nombre.setAlto(13);
            Nombre.setColorLetra(128,128,128); 
            Nombre.setTexto("Nombre");
            //#$fin de Nombre

            //#$inicio de JTextField0 
            JTextField0.setTexto("");
            //#$fin de JTextField0

            //#$inicio de contlogo2 
            contlogo2.setAncho(150); 
            contlogo2.setAlto( 50);
            contlogo2.setColorFondo(0,128,128); 
            //#$fin de contlogo2

            //#$inicio de ContLogo1 
            ContLogo1.setAncho(50);
            ContLogo1.setAlto( 50); 
            ContLogo1.setColorFondo(64,64,64);
            //#$fin de ContLogo1

            //#$inicio de ContBody 
            ContBody.setAncho(800);
            ContBody.setAlto(300); 
            ContBody.setColorFondo(64,224,208);
            //#$fin de ContBody
            propiedades -->

            <!--Colocacion
            /*
            Posicionamiento de los controles
            */

            contFondo.setPosicion(25,330); 
            this.add(contFondo);
            contlogin.setPosicion(586,110); 
            ContBody.add(contlogin);
            passw.setPosicion(11,54); 
            contlogin.add(passw); 
            cmdIngresar.setPosicion(40,100);
            pswClave.setPosicion(67,48); 
            contlogin.add(pswClave);

            Nombre.setPosicion(8,21);
            contlogin.add(Nombre);
            JTextField0.setPosicion(65,20); 
            contlogin.add(JTextField0);
            contlogo2.setPosicion(88,25); 
            ContBody.add(contlogo2);
            ContLogo1.setPosicion(36,25); 
            ContBody.add(ContLogo1);
            ContBody.setPosicion(23,21); 
            this.add(ContBody);
            Colocacion -->
                    '''

        tokens: List[Token] = []

        lexer: Lexer = Lexer(source)

        EOF_TOKEN = Token(TokenType.EOF, '')
        while True:
            token: Token = lexer.next_token()
            tokens.append(token)
            if token == EOF_TOKEN:
                break
            


        
