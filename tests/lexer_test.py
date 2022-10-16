from unittest import TestCase

from typing import List

from controller.lexer import Lexer

from controller.token import (
    Token,
    TokenType,
)


class LexerTest(TestCase):

    def test_delimiter(self):
        source: str = '();'


        lexer: Lexer = Lexer(source)

        tokens: List[Token] = []

        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: List[Token] = [
            Token(TokenType.LPAREN, ''),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)


