from jack_compiler.jack_tokenizer import JackTokenizer


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

    def compile_class(self):
        self._output_file.write("<class>\n")
        self._inc_indent()

        self._write_keyword()
        self._write_identifier()
        self._write_symbol()
        self._write_symbol()

        self._dec_indent()
        self._output_file.write("</class>\n")

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
