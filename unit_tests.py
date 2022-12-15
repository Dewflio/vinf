import unittest

from vinf_parser import VINF_Parser

test_file = "tests/test_dates.txt"
test_file_answers = "tests/test_dates_answers.txt"

class TestParser(unittest.TestCase):

    def test_parse_dates(self):
        p = VINF_Parser()
        results = []
        with open(test_file_answers, "r") as f:
            results = f.readlines()
        lines = []
        with open(test_file, "r") as f:
            lines = f.readlines()

        idx = 0
        for line in lines:
            result = str(p.process_date(line.strip()))
            self.assertEqual(result, results[idx].strip())
            idx += 1

t = TestParser()
t.test_parse_dates()


