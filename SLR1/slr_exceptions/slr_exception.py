from slr_exceptions.exceptions_enum import SLRErrId


class SLRException(Exception):
    def __init__(self, code: SLRErrId, word: str = "", row: any = "", column: any = ""):
        self.code: SLRErrId = code
        self.word: str = word
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.code == other.code

    def __str__(self):
        return f"LexerException: at {self.row}/{self.column} on word '{self.word}' exception of '{self.code.value}'"


class SLRRunnerException(Exception):
    def __init__(self, code: SLRErrId, word: str = "", row: any = "", column: any = ""):
        self.code: SLRErrId = code
        self.word: str = word
        self.row = row
        self.column = column

    def __str__(self):
        endl = "\n"
        return f"""SLRRunnerException:
    code: '{self.code}'
    details: '{self.code.value}'{f"{endl}    at: {self.row}/{self.column}" if self.row != "" or self.column != "" else ""}{f"{endl}    on word: '{self.word}'" if self.word != "" else ""}"""

    def __eq__(self, other):
        return self.code == other.code
