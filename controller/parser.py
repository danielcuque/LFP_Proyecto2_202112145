from typing import List, Optional
from controller.lexer import Lexer

from controller.ast import (
    Block,
    BlockStatement,
    Boolean,
    LetStatement,
    Program,
    Statement,
)
from controller.token import (
    Token,
    TokenType,
)


class Parser:

    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: List[str] = []

        self._advance_tokens()
        self._advance_tokens()

    @property
    def errors(self) -> List[str]:
        return self._errors

    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                program.statements.append(statement)

            self._advance_tokens()

        return program

    def _advance_tokens(self) -> None:
        self._current_token = self._peek_token
        self._peek_token = self._lexer.next_token()

    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None
        if self._peek_token.token_type == token_type:
            self._advance_tokens()

            return True

        self._expected_token_error(token_type)
        return False

    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        error = f'Se esperaba que el siguiente token fuera {token_type}, pero se obtuvo {self._peek_token.token_type}'
        self._errors.append(error)

    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None
        return Boolean(token=self._current_token, value=self._current_token.token_type == TokenType.TRUE)
    
    def _parse_block_statement(self) -> BlockStatement:
        assert self._current_token is not None
        statement = BlockStatement(token=self._current_token)

        self._advance_tokens()

        assert self._current_token is not None
        statement.name = self._current_token

        self._advance_tokens()

        assert self._current_token is not None
        statement.block = self._parse_block()

        return statement

    def _parse_block(self) -> Block:
        assert self._current_token is not None
        block = Block(token=self._current_token)

        self._advance_tokens()

        assert self._current_token is not None
        while self._current_token.token_type != TokenType.CLOSE_TAG:
            statement = self._parse_statement()
            if statement is not None:
                block.statements.append(statement)

            self._advance_tokens()

        return block

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None
        if self._current_token.token_type == TokenType.OPEN_TAG:
            return self._parse_block_statement()
