from re import match
from typing import List
from controller.token import (
    Token,
    TokenType,
)


class Lexer:

    def __init__(self, source: str) -> None:
        self._source = source
        self._character: str = ''
        self._position: int = 0
        self._read_position: int = 0
        self._read_character()

    states: List[str] = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    def next_token(self) -> Token:
        self._skip_whitespace()

        if match(r'^\($', self._character):
            token = Token(TokenType.LPAREN, self._character)
        elif match(r'^\)$', self._character):
            token = Token(TokenType.RPAREN, self._character)
        elif match(r'^;$', self._character):
            token = Token(TokenType.SEMICOLON, self._character)
        elif match(r'^$', self._character):
            token = Token(TokenType.EOF, '')
        elif match(r'^,$', self._character):
            token = Token(TokenType.COMMA, self._character)
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()
        return token

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character =  self._source[self._read_position]
        
        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        position = self._position
        while self._character in self.alphabet:
            self._read_character()
        return self._source[position:self._position]

    def _read_number(self) -> str:
        position = self._position
        while self._character in self.digits:
            self._read_character()
        return self._source[position:self._position]

    def _skip_whitespace(self) -> None:
        while self._character.isspace():
            self._read_character()
