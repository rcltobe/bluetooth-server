import unittest
from typing import List

from app.infra.spreadsheet.models.spreadsheet_entity import SpreadSheetEntity


class TestSpreadSheetEntity(unittest.TestCase):

    def test_validate(self):
        test_cases = [
            ValidateTestCase(attr_size=4, values=["1", "2", "3", "4"], expected=True, message="十分"),
            ValidateTestCase(attr_size=4, values=["1", "2", "3"], expected=False, message="値が足りない"),
            ValidateTestCase(attr_size=4, values=["1", "2", "3", "4", "5"], expected=True, message="必要な値は得られる"),
            ValidateTestCase(attr_size=4, values=["1", "2", "", "4"], expected=False, message="値が空"),
            ValidateTestCase(attr_size=2, values=["", "", "1", "2"], expected=False, message="適切な場所に値が無い")

        ]
        for case in test_cases:
            result = SpreadSheetEntity.validate(case.attr_size, case.values)
            self.assertEqual(case.expected, result, case.message)


class ValidateTestCase:
    def __init__(self, attr_size: int, values: List[str], expected: bool, message: str):
        self.attr_size = attr_size
        self.values = values
        self.expected = expected
        self.message = message
