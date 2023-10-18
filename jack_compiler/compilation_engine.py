from jack_compiler.jack_tokenizer import JackTokenizer, KeywordType, TokenType


def tag(tag_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            self = args[0]
            self._output_file.write(f"{self._get_indent()}<{tag_name}>\n")
            self._inc_indent()

            func(*args, **kwargs)

            self._dec_indent()
            self._output_file.write(f"{self._get_indent()}</{tag_name}>\n")

        return wrapper
    return decorator


class CompilationEngine:
    def __init__(self, input_path: str, output_path: str):
        with open(input_path, "r") as input_file:
            input_text = input_file.read()
            self._tokenizer = JackTokenizer(input_text)

        self._output_file = open(output_path, "w")
        self._indent_width = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._output_file.close()

    def _inc_indent(self):
        self._indent_width += 2

    def _dec_indent(self):
        self._indent_width -= 2

    @tag("class")
    def compile_class(self):
        self._write_keyword()
        self._write_identifier()
        self._write_symbol()

        self._tokenizer.advance()
        while self._tokenizer.token_type() == TokenType.KEYWORD and \
                self._tokenizer.keyword() in (KeywordType.STATIC, KeywordType.FIELD):
            self.compile_class_var_dec()

        while self._tokenizer.token_type() == TokenType.KEYWORD and \
                self._tokenizer.keyword() in (
                    KeywordType.CONSTRUCTOR, KeywordType.FUNCTION, KeywordType.METHOD):
            self.compile_subroutine_dec()

        self._write_symbol(advance=False)

    @tag("subroutineDec")
    def compile_subroutine_dec(self):
        self._write_keyword(advance=False)
        self._tokenizer.advance()

        if self._tokenizer.token_type() == TokenType.KEYWORD:
            self._write_keyword(advance=False)
        else:
            self._write_identifier(advance=False)

        self._write_identifier()
        self._write_symbol()

        self._tokenizer.advance()
        self.compile_parameter_list()

        self._write_symbol(advance=False)

        self._tokenizer.advance()
        self.compile_subroutine_body()

    @tag("parameterList")
    def compile_parameter_list(self):
        if self._tokenizer.token_type() == TokenType.SYMBOL:
            return

        self._write_type(advance=False)
        self._write_identifier()
        self._tokenizer.advance()

        while self._tokenizer.symbol() == ",":
            self._write_symbol(advance=False)
            self._write_type()
            self._write_identifier()
            self._tokenizer.advance()

    @tag("subroutineBody")
    def compile_subroutine_body(self):
        self._write_symbol(advance=False)
        self._tokenizer.advance()
        while self._tokenizer.token_type() == TokenType.KEYWORD and \
                self._tokenizer.keyword() == KeywordType.VAR:
            self.compile_var_dec()

        self.compile_statements()
        self._write_symbol(advance=False)
        self._tokenizer.advance()

    @tag("statements")
    def compile_statements(self):
        while self._tokenizer.token_type() == TokenType.KEYWORD:
            match self._tokenizer.keyword():
                case KeywordType.LET:
                    self.compile_let()
                case KeywordType.IF:
                    self.compile_if()
                case _:
                    break

    @tag("ifStatement")
    def compile_if(self):
        self._write_keyword(advance=False)
        self._write_symbol()
        self._tokenizer.advance()
        self.compile_expression()
        self._write_symbol(advance=False)

        self._write_statements_block()

        self._tokenizer.advance()
        if self._tokenizer.token_type() == TokenType.KEYWORD and \
           self._tokenizer.keyword() == KeywordType.ELSE:

            self._write_keyword(advance=False)
            self._write_statements_block()
            self._tokenizer.advance()

    def _write_statements_block(self):
        self._write_symbol()
        self._tokenizer.advance()
        self.compile_statements()
        self._write_symbol(advance=False)

    @tag("letStatement")
    def compile_let(self):
        self._write_keyword(advance=False)
        self._write_identifier()
        self._tokenizer.advance()

        if self._tokenizer.symbol() == "[":
            self._write_symbol(advance=False)
            self._tokenizer.advance()
            self.compile_expression()
            self._write_symbol(advance=False)
            self._tokenizer.advance()

        self._write_symbol(advance=False)
        self._tokenizer.advance()
        self.compile_expression()

        self._write_symbol(advance=False)
        self._tokenizer.advance()

    @tag("expression")
    def compile_expression(self):
        self.compile_term()
        # (op term)*

    @tag("term")
    def compile_term(self):
        # temp implementation
        self._write_identifier(advance=False)
        self._tokenizer.advance()

    @tag("varDec")
    def compile_var_dec(self):
        self._write_keyword(advance=False)
        self._write_type()
        self._write_identifier()

        self._tokenizer.advance()
        while self._tokenizer.symbol() == ",":
            self._write_symbol(advance=False)
            self._write_identifier()
            self._tokenizer.advance()

        self._write_symbol(advance=False)
        self._tokenizer.advance()

    @tag("classVarDec")
    def compile_class_var_dec(self):
        self._write_keyword(advance=False)
        self._write_type()
        self._write_identifier()

        self._tokenizer.advance()
        while self._tokenizer.symbol() == ",":
            self._write_symbol(advance=False)
            self._write_identifier()
            self._tokenizer.advance()

        self._write_symbol(advance=False)
        self._tokenizer.advance()

    def _write_type(self, advance=True):
        if advance:
            self._tokenizer.advance()

        if self._tokenizer.token_type() == TokenType.KEYWORD:
            self._write_keyword(advance=False)
        else:
            self._write_identifier(advance=False)

    def _write_keyword(self, advance=True):
        if advance:
            self._tokenizer.advance()

        self._output_file.write(
            f"{self._get_indent()}<keyword>{self._tokenizer.keyword().value}</keyword>\n")

    def _write_identifier(self, advance=True):
        if advance:
            self._tokenizer.advance()

        self._output_file.write(
            f"{self._get_indent()}<identifier>{self._tokenizer.identifier()}</identifier>\n")

    def _write_symbol(self, advance=True):
        if advance:
            self._tokenizer.advance()

        self._output_file.write(
            f"{self._get_indent()}<symbol>{self._tokenizer.symbol()}</symbol>\n")

    def _get_indent(self):
        return " " * self._indent_width
