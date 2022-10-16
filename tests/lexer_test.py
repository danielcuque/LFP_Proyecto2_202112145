from unittest import TestCase

from typing import List

from controller.lexer import Lexer

from controller.token import (
    Token,
    TokenType,
)


class LexerTest(TestCase):

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

        print(tokens)

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

        print(tokens)

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

        
