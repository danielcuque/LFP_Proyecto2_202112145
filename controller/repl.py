from controller.lexer import Lexer

from controller.token import (
    Token,
    TokenType,
)

EOF_TOKEN: Token = Token(TokenType.EOF, '')


def start_repl(source: str) -> None:
    lexer: Lexer = Lexer(source)

    while (token := lexer.next_token()) != EOF_TOKEN:
        print(token)