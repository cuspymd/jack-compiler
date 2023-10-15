import unittest

from jack_compiler.jack_tokenizer import JackTokenizer, TokenType, Token


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

    def test_has_more_tokens_given_etc(self):
        symbol_text = 'function test(int a){\n var num;\n let num=2;}'
        tokenizer = JackTokenizer(symbol_text)

        self._verify_has_more_tokens(tokenizer, range(16))

    def _verify_has_more_tokens(self, tokenizer, iterator):
        for _ in iterator:
            self.assertTrue(tokenizer.has_more_tokens())
            tokenizer.advance()

        self.assertFalse(tokenizer.has_more_tokens())

    def test_token_type_given_keyword(self):
        for keyword in Token.KEYWORD_TABLE.keys():
            tokenizer = JackTokenizer(keyword)
            tokenizer.advance()
            self.assertEqual(TokenType.KEYWORD, tokenizer.token_type())

    def test_token_type_given_symbol(self):
        symbol_text = "{}()[].,;+-*/&|<>=~"
        for symbol in symbol_text:
            tokenizer = JackTokenizer(symbol)
            tokenizer.advance()
            self.assertEqual(TokenType.SYMBOL, tokenizer.token_type())

    def test_token_type_given_identifier(self):
        tokenizer = JackTokenizer("name")
        tokenizer.advance()
        self.assertEqual(TokenType.IDENTFIER, tokenizer.token_type())

    def test_token_type_given_integer_constant(self):
        tokenizer = JackTokenizer("123")
        tokenizer.advance()
        self.assertEqual(TokenType.INT_CONST, tokenizer.token_type())

    def test_token_type_given_string_constant(self):
        tokenizer = JackTokenizer('"test string"')
        tokenizer.advance()
        self.assertEqual(TokenType.STRING_CONST, tokenizer.token_type())

    def test_keyword_given_keyword(self):
        for keyword_text, keyword_type in Token.KEYWORD_TABLE.items():
            tokenizer = JackTokenizer(keyword_text)
            tokenizer.advance()
            self.assertEqual(keyword_type, tokenizer.keyword())

    def test_symbol_given_symbol(self):
        symbol_text = "{}()[].,;+-*/&|<>=~"
        for symbol in symbol_text:
            tokenizer = JackTokenizer(symbol)
            tokenizer.advance()
            self.assertEqual(symbol, tokenizer.symbol())

    def test_identifier_given_identifier(self):
        tokenizer = JackTokenizer("name")
        tokenizer.advance()
        self.assertEqual("name", tokenizer.identifier())

    def test_int_val_given_int_const(self):
        tokenizer = JackTokenizer("123")
        tokenizer.advance()
        self.assertEqual(123, tokenizer.int_val())

    def test_string_val_given_string_const(self):
        tokenizer = JackTokenizer('"test string"')
        tokenizer.advance()
        self.assertEqual("test string", tokenizer.string_val())
