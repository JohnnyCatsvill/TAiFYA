from l_and_s_exceptions.exceptions_enum import LAndSErrId


class LAndSException(Exception):
    def __init__(self, code: LAndSErrId, row: int, column: int):
        self.code: LAndSErrId = code
        self.row: int = row
        self.column: int = column

    def __str__(self):
        return f"LAndSException: at {self.row}/{self.column} exception of '{self.code.value}'"
