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
        
    states: List[str] = []
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    digits = '0123456789'

    def next_token(self) -> Token:
        pass
