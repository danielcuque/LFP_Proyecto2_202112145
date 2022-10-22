from typing import List
from controller.token import (
    Token,
    TokenType,
    lookup_token_type
)


class Lexer:

    def __init__(self, source: str) -> None:
        self._source = source
        self._character: str = ''
        self._position: int = 0
        self._read_position: int = 0

        self._row: int = 0
        self._column: int = 0

        self._table_of_valid_tokens: List[Token] = []
        self._table_of_invalid_tokens: List[Token] = []
        self._read_character()

    def fill_table_of_tokens(self) -> None:
        while True:
            token = self.next_token()
            token.row = self._row
            token.column = self._column

            if token.token_type == TokenType.ILLEGAL:
                self._table_of_invalid_tokens.append(token)
            elif token.token_type != TokenType.OPEN_BLOCK_COMMENT and token.token_type != TokenType.CLOSE_BLOCK_COMMENT:
                self._table_of_valid_tokens.append(token)
            if token.token_type == TokenType.EOF:
                break

    _skip_characters: bool = False

    def next_token(self) -> Token:
        self._skip_whitespace()

        if self._skip_characters:
            while (self._character != '*' or self._peek_character() != '/') and self._character != '':
                self._read_character()
                self._skip_characters = False

        if self._character == '(':
            token = Token(TokenType.LPAREN, self._character)
        elif self._character == ')':
            token = Token(TokenType.RPAREN, self._character)
        elif self._character == ';':
            token = Token(TokenType.SEMICOLON, self._character)
        elif self._character == ',':
            token = Token(TokenType.COMMA, self._character)
        elif self._character == '.':
            token = Token(TokenType.DOT, self._character)
        elif self._character == '\"':
            literal = self._read_string()

            return Token(TokenType.STRING, literal)
        elif self._character == '/':
            if self._peek_character() == '/':
                while self._character != '\n' and self._character != '':
                    self._read_character()
                return self.next_token()
            elif self._peek_character() == "*":
                token = self._make_two_character_token(
                    TokenType.OPEN_BLOCK_COMMENT)
                self._skip_characters = True
            else:
                token = Token(TokenType.ILLEGAL, self._character)
        elif self._character == '<':
            token = self._read_open_tag()
        elif self._character == '-':
            token = self._read_close_tag()
        elif self._character == '*':
            if self._peek_character() == '/':
                token = self._make_two_character_token(
                    TokenType.CLOSE_BLOCK_COMMENT)
            else:
                token = Token(TokenType.ILLEGAL, self._character)
        elif self._character.isalpha():
            literal = self._read_identifier()
            token_type = lookup_token_type(literal)
            return Token(token_type, literal)
        elif self._character.isdigit():
            literal = self._read_number()
            return Token(TokenType.INT, literal)
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
        self._column += 1

    def _read_close_tag(self) -> Token:
        initial_position = self._position
        if self._peek_character() != '-':
            return Token(TokenType.ILLEGAL, self._character)
        self._read_character()  # -

        if self._peek_character() != '>':
            return Token(TokenType.ILLEGAL, self._source[initial_position:self._position+1])
        self._read_character()  # >

        return Token(TokenType.CLOSE_TAG, self._source[initial_position:self._position+1])

    def _read_identifier(self) -> str:
        position = self._position

        is_first_letter = True
        while self._character.isalpha() or (not is_first_letter and self._character.isdigit()):
            self._read_character()
            is_first_letter = False
        return self._source[position:self._position]

    def _read_open_tag(self) -> Token:
        initial_position = self._position
        if self._peek_character() != '!':
            return Token(TokenType.ILLEGAL, self._character)
        self._read_character()  # !
        if self._peek_character() != '-':
            return Token(TokenType.ILLEGAL, self._source[initial_position:self._position+1])
        self._read_character()  # -
        if self._peek_character() != '-':
            return Token(TokenType.ILLEGAL, self._source[initial_position:self._position+1])
        self._read_character()  # -
        return Token(TokenType.OPEN_TAG, self._source[initial_position:self._position+1])

    def _read_number(self) -> str:
        position = self._position
        while self._character.isdigit():
            self._read_character()
        return self._source[position:self._position]

    def _read_string(self) -> str:
        self._read_character()

        initial_position = self._position
        while self._character != '\"' \
                and self._position <= len(self._source):
            self._read_character()

        string = self._source[initial_position:self._position]

        self._read_character()

        return string

    def _skip_whitespace(self) -> None:
        while self._character.isspace():
            if self._character == '\n':
                self._row += 1
                self._column = 0
            self._read_character()

    def get_invalid_tokens(self) -> List[Token]:
        return self._table_of_invalid_tokens

    def get_valid_tokens(self) -> List[Token]:
        return self._table_of_valid_tokens
