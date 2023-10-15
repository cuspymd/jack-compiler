import html
import argparse
from pathlib import Path
from jack_compiler.jack_tokenizer import TokenType, JackTokenizer


class JackAnalyzer:
    def run(self, input_path_str: str):
        input_path = Path(input_path_str)
        if input_path.is_file():
            self._analyze_file(input_path)
        elif input_path.is_dir():
            self._analyze_folder(input_path)

    def _analyze_file(self, input_path: Path):
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

    def _analyze_folder(self, input_folder: Path):
        jack_files = input_folder.glob("*.jack")
        for jack_file in jack_files:
            self._analyze_file(jack_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path")
    args = parser.parse_args()

    print(f"Start translating for '{args.input_path}'")

    analyzer = JackAnalyzer()
    analyzer.run(args.input_path)
    print("Completed")
