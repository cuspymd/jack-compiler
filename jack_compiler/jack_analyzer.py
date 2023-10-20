import html
import argparse
from pathlib import Path
from jack_compiler.jack_tokenizer import TokenType, JackTokenizer
from jack_compiler.compilation_engine import CompilationEngine


class JackAnalyzer:
    def run(self, input_path_str: str, token_test: bool):
        input_path = Path(input_path_str)

        if token_test:
            self._run_token_test(input_path)
        else:
            self._run_analysis(input_path)

    def _run_analysis(self, input_path: Path):
        if input_path.is_file():
            self._run_analysis_file(input_path)
        elif input_path.is_dir():
            self._run_analysis_folder(input_path)

    def _run_token_test(self, input_path: Path):
        if input_path.is_file():
            self._run_token_test_file(input_path)
        elif input_path.is_dir():
            self._run_token_test_folder(input_path)

    def _run_analysis_file(self, input_path: Path):
        input_path_str = str(input_path)
        output_path_str = str(input_path.with_suffix(".xml"))

        with CompilationEngine(input_path_str, output_path_str) as engine:
            engine.compile_class()

    def _run_token_test_file(self, input_path: Path):
        with input_path.open(mode="r") as input_file:
            input_text = input_file.read()

        tokenizer = JackTokenizer(input_text)
        xml_lines = []
        while tokenizer.has_more_tokens():
            tokenizer.advance()

            xml_line = ""
            match tokenizer.token_type():
                case TokenType.KEYWORD:
                    xml_line = f"  <keyword>{tokenizer.symbol()}</keyword>"
                case TokenType.SYMBOL:
                    xml_line = f"  <symbol>{self._escape(tokenizer.symbol())}</symbol>"
                case TokenType.INT_CONST:
                    xml_line = f"  <integerConstant>{tokenizer.int_val()}</integerConstant>"
                case TokenType.STRING_CONST:
                    xml_line = f"  <stringConstant>{tokenizer.string_val()}</stringConstant>"
                case TokenType.IDENTFIER:
                    xml_line = f"  <identifier>{tokenizer.identifier()}</identifier>"

            xml_lines.append(xml_line)

        xml_lines = [
            "<tokens>",
            *xml_lines,
            "</tokens>"
        ]

        out_path = input_path.with_suffix(".xml")
        with out_path.open(mode="w") as out_file:
            out_file.write("\n".join(xml_lines))
            out_file.write("\n")

    def _escape(self, text: str) -> str:
        return html.escape(text)

    def _run_analysis_folder(self, input_folder: Path):
        jack_files = input_folder.glob("*.jack")
        for jack_file in jack_files:
            self._run_analysis_file(jack_file)

    def _run_token_test_folder(self, input_folder: Path):
        jack_files = input_folder.glob("*.jack")
        for jack_file in jack_files:
            self._run_token_test_file(jack_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    parser.add_argument("--token-test", action="store_true")
    args = parser.parse_args()

    print(f"Start translating for '{args.input_path}'")

    analyzer = JackAnalyzer()
    analyzer.run(args.input_path, args.token_test)
    print("Completed")
