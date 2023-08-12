"""A simple implementation of a `ParenthesesFormatter`.

Goals:
  1. Write a basic `Token` `Lexer`.
  2. Use `Lexer` to add characters to the buffer.
  3. Format as a `str` from argv.
"""
from __future__ import annotations

from enum import Enum, auto
from typing import Iterable


class ParenthesesFormatter:
    def __init__(self) -> None:
        self._printer = Printer()

    def fmt(self) -> str:
        if not self._printer:
            return ""
        if not is_parenthesized(self._printer._buffer):
            return f"({self._printer.print()})"

    def parse(self, s: str) -> ParenthesesFormatter:
        lex = Lexer(s)
        i = 0
        for token in lex.tokens():
            if not token:
                return self
            if is_left_parentheses_like(token):
                self._printer.add("(")
            elif is_right_parentheses_like(token):
                self._printer.add(")")
            else:
                self._printer.add(s[i])
            i += 1
        return self


class Lexer:
    def __init__(self, contents: str) -> None:
        self._pos = 0
        self._contents = contents

    def tokens(self) -> Iterable[Token]:
        while self._pos < self.size():
            yield next(self) or Token.EOF

    def size(self) -> int:
        return len(self._contents)

    def __next__(self) -> Token | None:
        if not self._pos < len(self._contents):
            return None
        pos = self._pos
        self._pos += 1
        match self._contents[pos]:
            case "(":
                return Token.OPEN_PARENTHESES
            case ")":
                return Token.CLOSE_PARENTHESES
            case "[":
                return Token.OPEN_BRACKET
            case "]":
                return Token.CLOSE_BRACKET
            case "{":
                return Token.OPEN_BRACE
            case "}":
                return Token.CLOSE_BRACE
            case _:
                return Token.OTHER  # :)


def is_parenthesized(buffer: list[str]) -> bool:
    i, j = 0, len(buffer)
    while i < j:
        if not is_left_parentheses_like(buffer[i]):
            i += 1
        elif not is_right_parentheses_like(buffer[j]):
            j -= 1
        else:
            i, j = i + 1, j - 1
    return buffer[i - 1] == "(" and buffer[j] == ")"


def is_parentheses_like(token: Token) -> bool:
    """Helper for checking if the token is any kind of expected parentheses."""
    return is_left_parentheses_like(token) or is_right_parentheses_like(token)


def is_left_parentheses_like(token: Token) -> bool:
    return token in (Token.OPEN_PARENTHESES, Token.OPEN_BRACKET, Token.OPEN_BRACE)


def is_right_parentheses_like(token: Token) -> bool:
    return token in (Token.CLOSE_PARENTHESES, Token.CLOSE_BRACKET, Token.CLOSE_BRACE)


class Token(Enum):
    OTHER = auto()
    OPEN_PARENTHESES = "("
    CLOSE_PARENTHESES = ")"
    OPEN_BRACKET = "["
    CLOSE_BRACKET = "]"
    OPEN_BRACE = "{"
    CLOSE_BRACE = "}"
    EOF = "EOF"


class Printer:
    def __init__(self) -> None:
        self._buffer = []

    def add(self, ch: str) -> None:
        self._buffer.append(ch)

    def print(self) -> str:
        return "".join(self._buffer)


if __name__ == "__main__":
    import sys

    s = sys.argv[1]
    formatter = ParenthesesFormatter().parse(s)
    print(formatter.fmt())
