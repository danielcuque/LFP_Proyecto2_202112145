from enum import (
    Enum,
    auto,
    unique,
)
from typing import Dict, NamedTuple


@unique
class TokenType(Enum):
    """Token types"""
    CLOSE_TAG = auto()
    CLOSE_BLOCK_COMMENT = auto()
    COMMA = auto()
    CONTROL = auto()
    DOT = auto()
    EOF = auto()
    FALSE = auto()
    IDENT = auto()
    INT = auto()
    ILLEGAL = auto()
    LPAREN = auto()
    OPEN_TAG = auto()
    OPEN_BLOCK_COMMENT = auto()
    PROPERTY = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    SINGLE_QUOTE = auto()
    STRING = auto()
    TRUE = auto()


class Token(NamedTuple):
    token_type: TokenType
    literal: str
    

    def __str__(self) -> str:
        return f'Type: {self.token_type}, Literal: {self.literal}'


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
    }
    return keywords.get(literal, TokenType.IDENT)
