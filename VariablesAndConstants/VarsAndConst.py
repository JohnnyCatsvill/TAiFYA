from dataclasses import dataclass
from typing import Union

from vac_exceptions.exceptions_enum import VACErrId
from vac_exceptions.vac_exception import VACException


@dataclass
class Record:
    name: str
    type: str
    value: any
    is_var: bool = True
    is_arr: bool = False
    arr_len: int = 0

    def __str__(self):
        return f"{'var' if self.is_var else 'const'} {self.type} {self.name} = {self.value}"


class VarsAndConst:
    def __init__(self):
        self.list: list[Record] = []
        self.blocks: list[int] = [0]

    def __repr__(self):
        output = str(self.blocks) + "\n"
        for i in self.list:
            output += str(i) + "\n"
        return output

    def add_block(self):
        self.blocks.append(len(self.list))

    def remove_block(self):
        while len(self.list) > self.blocks[-1]:
            self.list.pop()
        if len(self.blocks) > 1:
            self.blocks.pop()

    def add_record(self, name: str, type: str, value: any, var: bool = True):
        for i in self.list[self.blocks[-1]:]:
            if i.name == name:
                raise VACException(VACErrId.DOUBLE_ASSIGN_SAME_VAR, name)
        self.list.append(Record(name, type, value, var))

    def get_record(self, name: str) -> Union[Record, bool]:
        for i in self.list[::-1]:
            if i.name == name:
                return i
        return False

    def update_record(self, name: str, type: str, value: any, var: bool = True):  # проверка на конст
        for i, e in enumerate(self.list[::-1]):
            if e.name == name:
                if e.is_var and e.type == type:  # если переменная нашего типа
                    self.list[-i-1].value = value
                elif not e.is_var:
                    raise VACException(VACErrId.UPDATING_CONSTANT_VAR, name)
                else:
                    raise VACException(VACErrId.UNMATCHED_TYPES, name)
                return
