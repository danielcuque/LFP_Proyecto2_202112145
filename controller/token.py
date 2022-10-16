from enum import (
    Enum,
    auto,
    unique,
)
from typing import Dict


@unique
class TokenType(Enum):
    """Token types"""
    CLOSE_MULTI_COMMENT = auto()
    CLOSE_TAG = auto()
    COMMA = auto()
    CONTROL = auto()
    DOT = auto()
    FALSE = auto()
    IDENT = auto()
    LPAREN = auto()
    OPEN_MULTI_COMMENT = auto()
    OPEN_TAG = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    SIMPLE_COMMENT = auto()
    SINGLE_QUOTE = auto()
    STRING = auto()
    TRUE = auto()


class Token:
    """Token class"""

    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal

    def __str__(self):
        return f"Token({self.token_type}, {self.literal})"

    def __repr__(self):
        return self.__str__()


def lookup_token_type(literal: str) -> TokenType:
    keywords: Dict[str, TokenType] = {
        'true': TokenType.TRUE,
        'false': TokenType.FALSE,
    }
    return keywords.get(literal, TokenType.IDENT)
