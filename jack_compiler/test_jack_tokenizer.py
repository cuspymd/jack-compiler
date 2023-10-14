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

    def test_has_more_tokens_given_comment(self):
        tokenizer = JackTokenizer("// comment")
        self.assertFalse(tokenizer.has_more_tokens())
