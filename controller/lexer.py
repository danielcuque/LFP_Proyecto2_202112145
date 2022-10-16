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

    _skip_characters: bool = False

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self._skip_characters:
            self._skip_characters = False
            while self._character != '*' and self._peek_character() != '/' and self._character != '':
                self._read_character()
            if self._character == '':
                return Token(TokenType.EOF, '')

            token = self._make_two_character_token(
                TokenType.CLOSE_BLOCK_COMMENT)
            self._read_character()
            return token

        if self._character == '(':
            token = Token(TokenType.LPAREN, self._character)
        elif self._character == ')':
            token = Token(TokenType.RPAREN, self._character)
        elif self._character == ';':
            token = Token(TokenType.SEMICOLON, self._character)
        elif self._character == ',':
            token = Token(TokenType.COMMA, self._character)
        elif self._character == '/':
            if self._peek_character() == '/':
                while self._character != '\n':
                    self._read_character()
                return self.next_token()
            elif self._peek_character() == "*":
                token = self._make_two_character_token(
                    TokenType.OPEN_BLOCK_COMMENT)
                self._skip_characters = True
                self._read_character()
            else:
                token = Token(TokenType.ILLEGAL, self._character)
        elif self._character == '':
            token = Token(TokenType.EOF, '')
        else:
            token = Token(TokenType.ILLEGAL, self._character)

        self._read_character()
        return token

    def _make_two_character_token(self, token_type: TokenType) -> Token:
        prefix = self._character
        self._read_character()
        susfix = self._character

        return Token(token_type, f'{prefix}{susfix}')

    def _peek_character(self) -> str:
        if self._read_position >= len(self._source):
            return ''
        else:
            return self._source[self._read_position]

    def _read_character(self) -> None:
        if self._read_position >= len(self._source):
            self._character = ''
        else:
            self._character = self._source[self._read_position]

        self._position = self._read_position
        self._read_position += 1

    def _read_identifier(self) -> str:
        position = self._position
        while self._character.isalpha():
            self._read_character()
        return self._source[position:self._position]

    def _read_number(self) -> str:
        position = self._position
        while self._character.isdigit():
            self._read_character()
        return self._source[position:self._position]

    def _skip_whitespace(self) -> None:
        while self._character.isspace():
            self._read_character()
