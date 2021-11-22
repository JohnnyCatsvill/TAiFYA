
class Record:
    def __init__(self, name: str, type: str, value: any, var: bool = True):
        self.name: str = name
        self.type: str = type
        self.value: any = value
        self.var: bool = var

    def __repr__(self):
        return f"{'var' if self.var else 'const'} {self.type} {self.name} = {self.value}"


class VarsAndConst:
    def __init__(self):
        self.list: list[Record] = []
        self.blocks: list[int] = []

    def __repr__(self):
        output = str(self.blocks) + "\n"
        for i in self.list:
            output += str(i) + "\n"
        return output

    def add_block(self):
        self.blocks.append(len(self.list))

    def remove_block(self):
        if len(self.blocks) > 0:
            while len(self.list) > self.blocks[-1]:
                self.list.pop()
            self.blocks.pop()

    def add_record(self, name: str, type: str, value: any, var: bool = True):
        self.list.append(Record(name, type, value, var))

    def get_record(self, name: str) -> Record:
        for i in self.list[::-1]:
            if i.name == name:
                return i

    def update_record(self, name: str, type: str, value: any, var: bool = True):
        for i, e in enumerate(self.list[::-1]):
            if e.name == name:
                self.list[-i-1] = Record(name, type, value, var)
