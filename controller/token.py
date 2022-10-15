from enum import (
    Enum,
    auto,
    unique,
)


@unique
class TokenType(Enum):
    """Token types"""
    CLOSE_TAG = auto()
    CONTROL = auto()
    DOT = auto()
    DOUBLE_QUOTE = auto()
    IDENT = auto()
    LPAREN = auto()
    MULTI_COMMENT = auto()
    OPEN_TAG = auto()
    RPAREN = auto()
    SEMICOLON = auto()
    SINGLE_COMMENT = auto()
    SINGLE_QUOTE = auto()
    WRAPPER = auto()


class Token:
    """Token class"""

    def __init__(self, token_type, literal):
        self.token_type = token_type
        self.literal = literal

    def __str__(self):
        return f"Token({self.token_type}, {self.literal})"

    def __repr__(self):
        return self.__str__()
