class FuncPart:
    def __init__(self, function: callable, arg_length: int):
        self.f = function
        self.arg_length = arg_length


f = {
    "add": FuncPart(lambda arg: {"val": arg[0]["val"] + arg[1]["val"]}, 2),
    "sub": FuncPart(lambda arg: {"val": arg[0]["val"] - arg[1]["val"]}, 2),
    "print": FuncPart(lambda arg: print(arg[0]), 1),
    "pass": FuncPart(lambda arg: {"val": arg[0].get("val"), "type": arg[0].get("type")}, 1),
}
