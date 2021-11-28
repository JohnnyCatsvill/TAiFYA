from vac_exceptions.exceptions_enum import VACErrId


class VACException(Exception):
    def __init__(self, code: VACErrId, word: str = "", row: any = "", column: any = ""):
        self.code: VACErrId = code
        self.word: str = word

    def __eq__(self, other):
        return self.code == other.code

    def __str__(self):
        return f"VACException: on word '{self.word}' exception of '{self.code.value}'"
