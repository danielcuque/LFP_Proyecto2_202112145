from typing import List, Optional
from controller.lexer import Lexer


from controller.token import (
    Token,
    TokenType,
)


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        pass
    #     self._lexer = lexer
    #     self._current_token = Optional[Token] = None
    #     self._peek_token = Optional[Token] = None
    #     self._errors: List[str] = []

    # @property
    # def errors(self) -> List[str]:
    #     return self._errors

    # def _advance_tokens(self) -> None:
    #     self._current_token = self._peek_token
    #     self._peek_token = self._lexer.next_token()