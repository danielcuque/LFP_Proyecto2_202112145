from enum import (
    Enum,
    auto,
    unique,
)
from typing import Dict


@unique
class TokenType(Enum):
    """Token types"""
    BOOLEAN = auto()
    CLOSE_TAG = auto()
    CLOSE_BLOCK_COMMENT = auto()
    COMMA = auto()
    CONTROL = auto()
    DOT = auto()
    EOF = auto()
    EMPTY = auto()
    FUNCTION = auto()
    IDENT = auto()
    INT = auto()
    ILLEGAL = auto()
    JUSTIFY = auto()
    LPAREN = auto()
    OPEN_TAG = auto()
    OPEN_BLOCK_COMMENT = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    STRING = auto()
    WRAPPER = auto()


class Token:
    def __init__(self, token_type: TokenType, literal: str):
        self.token_type = token_type
        self.literal = literal
    row: int = 0
    column: int = 0

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal} at row: {self.row}, column: {self.column}'


def lookup_token_type(literal: str) -> TokenType:
    literal = literal.lower()
    """Lookup token type by literal"""
    if len(literal) >= 3:
        if literal[0:3] == 'set' or literal[0:3] == 'add':
            return TokenType.FUNCTION

    keywords_justify: Dict[str, TokenType] = {
        'derecho': TokenType.JUSTIFY,
        'izquierdo': TokenType.JUSTIFY,
        'centro': TokenType.JUSTIFY,
    }

    if literal in keywords_justify:
        return keywords_justify[literal]

    keywords_wrapper: Dict[str, TokenType] = {
        'controles': TokenType.WRAPPER,
        'propiedades': TokenType.WRAPPER,
        'colocacion': TokenType.WRAPPER,
    }

    if literal in keywords_wrapper:
        return keywords_wrapper[literal]

    keywords_control: Dict[str, TokenType] = {
        'areatexto': TokenType.CONTROL,
        'boton': TokenType.CONTROL,
        'check': TokenType.CONTROL,
        'clave': TokenType.CONTROL,
        'contenedor': TokenType.CONTROL,
        'etiqueta': TokenType.CONTROL,
        'radioboton': TokenType.CONTROL,
        'texto': TokenType.CONTROL,
    }

    if literal in keywords_control:
        return keywords_control[literal]

    keywords: Dict[str, TokenType] = {
        'true': TokenType.BOOLEAN,
        'false': TokenType.BOOLEAN,
    }
    
    return keywords.get(literal, TokenType.IDENT)
