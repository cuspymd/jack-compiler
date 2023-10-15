import re
from enum import Enum
from typing import List


class TokenType(Enum):
    UNKNOWN = 0
    KEYWORD = 1
    SYMBOL = 2
    INTEGER_CONSTANT = 3
    STRING_CONSTANT = 4
    IDENTFIER = 5


class JackTokenizer:
    SYMBOLS = {
        "{", "}", "(", ")", "[", "]", ".", ",", ";",
        "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"
    }

    def __init__(self, file_text: str):
        self.tokens = self._parse_tokens(file_text)
        self.current_token_number = -1

    def _parse_tokens(self, file_text: str) -> List[str]:
        lines = self._get_valid_lines(file_text)
        tokens = []

        for line in lines:
            token_type = TokenType.UNKNOWN
            token_start_index = 0

            for i in range(len(line)):
                if line[i] in JackTokenizer.SYMBOLS:
                    if token_type != TokenType.UNKNOWN:
                        tokens.append(line[token_start_index:i])
                        token_type = TokenType.UNKNOWN

                    tokens.append(line[i])
                elif line[i] == " ":
                    if token_type == token_type.STRING_CONSTANT:
                        continue

                    if token_type != TokenType.UNKNOWN:
                        tokens.append(line[token_start_index:i])
                        token_type = token_type.UNKNOWN
                elif line[i] == '"':
                    if token_type == TokenType.UNKNOWN:
                        token_type = TokenType.STRING_CONSTANT
                        token_start_index = i
                    else:
                        tokens.append(line[token_start_index:i])
                        token_type = token_type.UNKNOWN
                else:
                    if token_type == TokenType.UNKNOWN:
                        token_type = TokenType.IDENTFIER
                        token_start_index = i

            if token_type != TokenType.UNKNOWN:
                tokens.append(line[token_start_index:len(line)])

        return tokens

    def _get_valid_lines(self, file_text: str) -> List[str]:
        file_text = self._delete_comments(file_text)
        return [
            valid_text
            for line in file_text.splitlines()
            if (valid_text := self._get_valid_text(line))
        ]

    def _delete_comments(self, text: str) -> str:
        comment_regex = r"/\*.*?\*/"
        text = re.sub(comment_regex, "", text, flags=re.DOTALL)
        comment_regex = r"//.*"
        return re.sub(comment_regex, "", text)

    def _get_valid_text(self, text: str) -> str:
        return text.strip()

    def has_more_tokens(self):
        return self.current_token_number < len(self.tokens)-1

    def advance(self):
        self.current_token_number += 1
