import unittest

from jack_compiler.jack_tokenizer import JackTokenizer


class TestJackTokenizer(unittest.TestCase):
    def test_has_more_tokens_given_empty_line(self):
        tokenizer = JackTokenizer("")
        self.assertFalse(tokenizer.has_more_tokens())

        tokenizer = JackTokenizer("	")
        self.assertFalse(tokenizer.has_more_tokens())

        tokenizer = JackTokenizer("\n   \n     \n")
        self.assertFalse(tokenizer.has_more_tokens())

        tokenizer = JackTokenizer("\r\n   \r\n     \r\n")
        self.assertFalse(tokenizer.has_more_tokens())

        tokenizer = JackTokenizer("\n   \n     return;\n")
        self.assertTrue(tokenizer.has_more_tokens())

    def test_has_more_tokens_given_one_line_comment(self):
        tokenizer = JackTokenizer("// comment")
        self.assertFalse(tokenizer.has_more_tokens())

    def test_has_more_tokens_given_multi_line_comment(self):
        tokenizer = JackTokenizer("/* comment\nreturn;\n*/")
        self.assertFalse(tokenizer.has_more_tokens())

    def test_has_more_tokens_given_symbols(self):
        symbol_text = "{}()[].,;+-*/&|<>=~"
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, symbol_text)

    def test_has_more_tokens_given_symbols_with_space(self):
        symbol_text = "{}()[] .,;+    -*/&   |<>=~"
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(19))

    def test_has_more_tokens_given_symbols_with_newline(self):
        symbol_text = "{}()[].,;+\n-*/&\n|<>=~"
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(19))

    def test_has_more_tokens_given_symbols_with_keyword(self):
        symbol_text = "return;"
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(2))

    def test_has_more_tokens_given_if_statement(self):
        symbol_text = "if (num > 0) {\n  num = num + 1;\n  return num;"
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(16))

    def test_has_more_tokens_given_string(self):
        symbol_text = '"this is string"'
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(1))

    def _verify_has_more_tokens(self, tokenizer, iterator):
        for _ in iterator:
            self.assertTrue(tokenizer.has_more_tokens())
            tokenizer.advance()

        self.assertFalse(tokenizer.has_more_tokens())
