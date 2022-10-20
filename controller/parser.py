from typing import List, Optional

from enum import (
    Enum,
    auto,
    unique,
)


from controller.token import (
    Token,
    TokenType,
)


@unique
class NoTerminal(Enum):
    START = auto()
    LET_STATEMENT = auto()
    CALL_FUNCTION = auto()
    PARAMETERS = auto()
    PARAMETER = auto()


class Error:
    def __init__(self, token, expected_token) -> None:
        self.token = token
        self.expected_token = expected_token


class Parser:

    def __init__(self, valid_tokens: List[Token]) -> None:
        self._valid_tokens = valid_tokens
        self._stack = [TokenType.EOF, NoTerminal.START]
        self._errors: List[str] = []

        self._position: int = 0

    @property
    def errors(self) -> List[str]:
        return self._errors

    def parse_programm(self) -> None:
        while self._stack[-1] != TokenType.EOF:
            print(self._stack)
            self._next_state()

    def _next_state(self) -> bool:
        current_stack = self._stack[-1]

        current_token: Token

        # No terminals
        try:
            current_token = self._valid_tokens[self._position]
        except IndexError:
            current_tokent = Token(TokenType.EMPTY, '')

            # todo: Validar que no hayan no terminales en la pila
            self._errors.append('Unexpected EOF')
            return False

        if current_stack == NoTerminal.START:
            self._append_state_zero()
            return True

        elif current_stack == NoTerminal.LET_STATEMENT:
            if current_token.token_type == TokenType.CONTROL:
                self._append_state_one()
                return True
            self._stack.pop()
            return True
        elif current_stack == NoTerminal.CALL_FUNCTION:
            self._append_state_two()
        elif current_stack == NoTerminal.PARAMETERS:
            if current_token.token_type == TokenType.BOOLEAN:
                pass
            elif current_token.token_type == TokenType.INT:
                self._replace_top([
                    Token(TokenType.INT, ''),
                    NoTerminal.PARAMETER,
                ])
                return True

            elif current_token.token_type == TokenType.STRING:
                self._replace_top([
                    Token(TokenType.STRING, ''),
                ])
                return True
            elif current_token.token_type == TokenType.JUSTIFY:
                self._replace_top([
                    Token(TokenType.JUSTIFY, ''),
                ])
                return True
            elif current_token.token_type == TokenType.IDENT:
                self._replace_top([
                    Token(TokenType.IDENT, ''),
                ])
                return True
            self._errors.append(Error(current_token, [
                                TokenType.BOOLEAN, TokenType.INT, TokenType.STRING, TokenType.JUSTIFY, TokenType.IDENT]))
            return

        elif current_stack == NoTerminal.PARAMETER:
            if current_token.token_type == TokenType.INT:
                self._replace_top([
                    Token(TokenType.INT, ''),
                    Token(TokenType.COMMA, ''),
                ])
                return True
            self._stack.pop()
            return

        # Terminals
        elif current_stack.token_type == TokenType.OPEN_TAG \
                and current_token.token_type == TokenType.OPEN_TAG:

            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.CLOSE_TAG \
                and current_token.token_type == TokenType.CLOSE_TAG:

            self._stack.pop()
            self._position += 1
            return True
        elif current_stack.token_type == TokenType.WRAPPER \
                and current_token.token_type == TokenType.WRAPPER:

            self._stack.pop()
            self._position += 1
            return True
        elif current_stack.token_type == TokenType.CONTROL \
                and current_token.token_type == TokenType.CONTROL:

            self._stack.pop()
            self._position += 1
            return True
        elif current_stack.token_type == TokenType.IDENT \
                and current_token.token_type == TokenType.IDENT:

            self._stack.pop()
            self._position += 1
            return True
        elif current_stack.token_type == TokenType.DOT \
                and current_token.token_type == TokenType.DOT:

            self._stack.pop()
            self._position += 1
            return True
        elif current_stack.token_type == TokenType.FUNCTION \
                and current_token.token_type == TokenType.FUNCTION:

            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.SEMICOLON \
                and current_token.token_type == TokenType.SEMICOLON:
            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.COMMA \
                and current_token.token_type == TokenType.COMMA:
            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.BOOLEAN \
                and current_token.token_type == TokenType.BOOLEAN:
            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.INT \
                and current_token.token_type == TokenType.INT:
            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.STRING \
                and current_token.token_type == TokenType.STRING:
            self._stack.pop()
            self._position += 1
            return True

        elif current_stack.token_type == TokenType.JUSTIFY \
                and current_token.token_type == TokenType.JUSTIFY:
            self._stack.pop()
            self._position += 1
            return True

        self._errors.append(Error(current_token, [current_stack]))
        self._stack.pop()
        return False

    def _next_token(self):
        pass

    def _append_state_zero(self) -> None:
        self._replace_top([
            Token(TokenType.OPEN_TAG, ''),
            Token(TokenType.WRAPPER, ''),
            NoTerminal.LET_STATEMENT,
            Token(TokenType.WRAPPER, ''),
            Token(TokenType.CLOSE_TAG, ''),

            Token(TokenType.OPEN_TAG, ''),
            Token(TokenType.WRAPPER, ''),
            NoTerminal.CALL_FUNCTION,
            Token(TokenType.WRAPPER, ''),
            Token(TokenType.CLOSE_TAG, ''),

            Token(TokenType.OPEN_TAG, ''),
            Token(TokenType.WRAPPER, ''),
            NoTerminal.CALL_FUNCTION,
            Token(TokenType.WRAPPER, ''),
            Token(TokenType.CLOSE_TAG, ''),
        ])

    def _append_state_one(self) -> None:
        self._replace_top([
            Token(TokenType.CONTROL, ''),
            Token(TokenType.IDENT, ''),
            Token(TokenType.SEMICOLON, ''),
            NoTerminal.LET_STATEMENT,
        ])

    def _append_state_two(self) -> None:
        self._replace_top([
            Token(TokenType.IDENT, 'btn1'),
            Token(TokenType.DOT, '.'),
            Token(TokenType.FUNCTION, 'setColor'),
            Token(TokenType.LPAREN, '('),
            NoTerminal.PARAMETERS,
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ])

    def _append_state_three(self) -> None:
        self._replace_top([
            Token(TokenType.BOOLEAN, 'true'),
        ])

    def _append_state_four(self) -> None:
        self._replace_top([
            Token(TokenType.COMMA, ','),
            NoTerminal.PARAMETERS, 'parameters'
        ])

    def _replace_top(self, nodes: List) -> None:
        self._stack.pop()
        for node in nodes[::-1]:
            self._stack.append(node)
