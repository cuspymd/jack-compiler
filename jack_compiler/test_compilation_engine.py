import unittest
from pathlib import Path

from jack_compiler.compilation_engine import CompilationEngine


class TestCompilationEngine(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_compile_class_given_empty_class(self):
        self._test_compile_class("empty_class")

    def test_compile_class_given_class_var_dec(self):
        self._test_compile_class("class_var_dec")

    def test_compile_class_given_subroutine_dec(self):
        self._test_compile_class("subroutine_dec")

    def test_compile_class_given_var_dec(self):
        self._test_compile_class("var_dec")

    def test_compile_class_given_parameter_list(self):
        self._test_compile_class("parameter_list")

    def test_compile_class_given_let_statement(self):
        self._test_compile_class("let_statement")

    def _test_compile_class(self, test_name):
        with self._create_engine(test_name) as engine:
            engine.compile_class()

        self._verify_file(test_name)

    def _create_engine(self, test_name):
        input_path_str = f"test_data/compile/{test_name}.jack"
        output_path_str = f"test_data/compile/{test_name}.xml"

        return CompilationEngine(input_path_str, output_path_str)

    def _verify_file(self, test_name):
        output_path = Path("test_data/compile", f"{test_name}.xml")
        solution_name = f"solution_{output_path.stem}"
        solution_path = output_path.with_stem(solution_name)

        with output_path.open(mode="r") as output_file:
            output_text = output_file.read()

        with solution_path.open(mode="r") as solution_file:
            solution_text = solution_file.read()

        self.assertEqual(solution_text, output_text)
        output_path.unlink()
