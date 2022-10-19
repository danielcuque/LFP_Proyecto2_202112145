from abc import (
    ABC,
    abstractmethod,
)
from typing import List, Optional

from controller.token import Token, TokenType


class ASTNode(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Expression(ASTNode):

    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal


class Program(ASTNode):

    def __init__(self,  statements: List[Statement]) -> None:
        self.statements = statements

    def token_literal(self) -> str:
        if len(self.statements) > 0:
            return self.statements[0].token_literal()
        else:
            return ''

    def __str__(self) -> str:
        out: List[str] = []
        for statement in self.statements:
            out.append(str(statement))

        return ''.join(out)

class Identifier(Expression):

    def __init__(self, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value

class LetStatement(Statement):

    def __init__(self, token: Token, name: Optional[Identifier] = None, value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.token_literal()} {self.name} {self.value};'

class BlockStatement(Statement):

    def __init__(self, token: Token, name: Optional[Identifier] = None) -> None:
        super().__init__(token)
        self.name = name

    def __str__(self) -> str:
        return f'{self.token_literal()} {self.name};'
