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
class NoTermimal(Enum):
    S0 = auto()
    S1 = auto()
    S2 = auto()
    S3 = auto()
    S4 = auto()


class Parser:

    def __init__(self, valid_tokens: List[Token]) -> None:
        self._valid_tokens = valid_tokens
        self._errors: List[str] = []
        self._stack: List[Token] = []

        self._position: int = 0

        self._stack.append(Token(TokenType.EOF, ''))
        self._stack.append(NoTermimal.S0)

    def run_parser(self) -> None:
        while self._stack[-1].token_type != TokenType.EOF:
            self._next_state()

    def _next_state(self) -> bool:
        current_stack = self._stack[-1]

        if current_stack == NoTermimal.S0:
            self._append_state_zero()
        elif current_stack == NoTermimal.S1:
            self._append_state_one()
        elif current_stack == NoTermimal.S2:
            self._append_state_two()
        elif current_stack == NoTermimal.S3:
            self._append_state_three()
        elif current_stack == NoTermimal.S4:
            self._append_state_four()
        elif current_stack.token_type == TokenType.EOF:
            return True

    def _next_token(self):
        pass

    def _append_state_zero(self) -> None:
        self._replace_top([
            Token(TokenType.OPEN_TAG, '<!--'),
            Token(TokenType.WRAPPER, 'Controles'),
            NoTermimal.S1,
            Token(TokenType.WRAPPER, 'Controles'),
            Token(TokenType.CLOSE_TAG, '-->'),
            Token(TokenType.WRAPPER, 'Propiedades'),
            NoTermimal.S2,
            Token(TokenType.WRAPPER, 'Propiedades'),
            Token(TokenType.CLOSE_TAG, '-->'),
            Token(TokenType.OPEN_TAG, '<!--'),
            Token(TokenType.WRAPPER, 'Colocacion'),
            NoTermimal.S2,
            Token(TokenType.WRAPPER, 'Colocacion'),
            Token(TokenType.CLOSE_TAG, '-->'),

        ])

    def _append_state_one(self) -> None:
        pass

    def _append_state_two(self) -> None:
        pass

    def _append_state_three(self) -> None:
        pass

    def _append_state_four(self) -> None:
        pass

    def _replace_top(self, nodes) -> None:
        self._stack.pop()
        for node in nodes[::-1]:
            self._stack.append(nodes)

    # @property
    # def errors(self) -> List[str]:
    #     return self._errors

    # def parse_program(self) -> Program:
    #     program: Program = Program(statements=[])

    #     assert self._current_token is not None
    #     while self._current_token.token_type != TokenType.EOF:
    #         statement = self._parse_statement()
    #         if statement is not None:
    #             program.statements.append(statement)

    #         self._advance_tokens()

    #     return program

    # def _advance_tokens(self) -> None:
    #     self._current_token = self._peek_token
    #     self._peek_token = self._lexer.next_token()

    # def _expected_token(self, token_type: TokenType) -> bool:
    #     assert self._peek_token is not None
    #     if self._peek_token.token_type == token_type:
    #         self._advance_tokens()

    #         return True

    #     self._expected_token_error(token_type)
    #     return False

    # def _expected_token_error(self, token_type: TokenType) -> None:
    #     assert self._peek_token is not None
    #     error = f'Se esperaba que el siguiente token fuera {token_type}, pero se obtuvo {self._peek_token.token_type}'
    #     self._errors.append(error)

    # def _parse_boolean(self) -> Boolean:
    #     assert self._current_token is not None
    #     return Boolean(token=self._current_token, value=self._current_token.token_type == TokenType.TRUE)

    # def _parse_block_statement(self) -> BlockStatement:
    #     assert self._current_token is not None
    #     statement = BlockStatement(token=self._current_token)

    #     self._advance_tokens()

    #     assert self._current_token is not None
    #     statement.name = self._current_token

    #     self._advance_tokens()

    #     assert self._current_token is not None
    #     statement.block = self._parse_block()

    #     return statement

    # def _parse_block(self) -> Block:
    #     assert self._current_token is not None
    #     block = Block(token=self._current_token)

    #     self._advance_tokens()

    #     assert self._current_token is not None
    #     while self._current_token.token_type != TokenType.CLOSE_TAG:
    #         statement = self._parse_statement()
    #         if statement is not None:
    #             block.statements.append(statement)

    #         self._advance_tokens()

    #     return block

    # def _parse_statement(self) -> Optional[Statement]:
    #     assert self._current_token is not None
    #     if self._current_token.token_type == TokenType.OPEN_TAG:
    #         pass
    #     else:

    #         return None
