import unittest
import os
from pathlib import Path

from jack_compiler.jack_analyzer import JackAnalyzer


class TestJackAnalyzer(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def test_token_given_file(self):
        analyzer = JackAnalyzer()
        analyzer.run("test_data/token/token.jack", True)
        self._verify_token("token.jack")

    def test_token_given_folder(self):
        analyzer = JackAnalyzer()
        analyzer.run("test_data/token", True)
        self._verify_token("token.jack")
        self._verify_token("token2.jack")

    def _verify_token(self, file_name: str):
        test_name = Path(file_name).stem

        out_file_path = f"test_data/token/{test_name}.xml"
        with open(out_file_path, "r") as out_file:
            out_xml = out_file.read()

        with open(f"test_data/token/solution_{test_name}.xml", "r") as solution_file:
            solution_xml = solution_file.read()

        self.assertEqual(solution_xml, out_xml)
        os.remove(out_file_path)
