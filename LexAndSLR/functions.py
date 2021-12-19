from VarsAndConst import VarsAndConst
from constants.constants_lex import FLOAT_NAME, DEC_NAME, BIN_NAME, HEX_NAME, OCT_NAME


class FuncPart:
    def __init__(self, function: callable, arg_length: int):
        self.f = function
        self.arg_length = arg_length


var_list = VarsAndConst()


def type_cast(type1: str, type2: str):
    if FLOAT_NAME in [type1, type2]:
        return FLOAT_NAME
    elif DEC_NAME in [type1, type2]:
        return DEC_NAME
    elif type1 in [BIN_NAME, OCT_NAME, HEX_NAME] and type2 in [BIN_NAME, OCT_NAME, HEX_NAME]:
        return type1


def initiation(*args):
    id_type = args[0][0].get("val")
    new_id = args[0][1].get("val")
    var_list.add_record(new_id, id_type)
    return {"type": f" {new_id}=None"}  # {"val": "None", "type": id_type}


def assign(*args):
    id = args[0][0].get("val")
    val = args[0][1].get("val")
    type = args[0][1].get("type")
    var_list.update_record(id, type, val)
    return {"type": f" {id}={val}"}  # {"val": val, "type": type}


def get_id_val(*args):
    id = args[0][0].get("val")
    record = var_list.get_record(id)
    return {"val": record.value, "type": record.type}


def negate(*args):
    val = - args[0][0].get("val")
    type = args[0][0].get("type")
    return {"val": val, "type": type}


def add(*args):
    val1 = args[0][0].get("val")
    val2 = args[0][1].get("val")
    type1 = args[0][0].get("type")
    type2 = args[0][1].get("type")

    new_type = type_cast(type1, type2)
    if new_type:
        return {"val": val1 + val2, "type": new_type}


def sub(*args):
    val1 = args[0][0].get("val")
    val2 = args[0][1].get("val")
    type1 = args[0][0].get("type")
    type2 = args[0][1].get("type")

    new_type = type_cast(type1, type2)
    if new_type:
        return {"val": val1 - val2, "type": new_type}


def init_list(*args):
    val = args[0][0].get("val")
    type = args[0][0].get("type")
    return {"val": [val], "type": type}


def add_to_list(*args):
    list_val = args[0][1].get("val")
    list_type = args[0][1].get("type")
    val = args[0][0].get("val")
    type = args[0][0].get("type")
    new_type = type_cast(list_type, type)
    if new_type:
        return {"val": [val] + list_val, "type": new_type}


def block(*args):
    var_list.add_block()


def end_block(*args):
    var_list.remove_block()


f = {
    "pass": FuncPart(lambda arg: arg[0], 1),
    "add": FuncPart(add, 2),
    "sub": FuncPart(sub, 2),
    "init": FuncPart(initiation, 2),
    "assign": FuncPart(assign, 2),
    "get_id_val": FuncPart(get_id_val, 1),
    "negate": FuncPart(negate, 1),
    "init_list": FuncPart(init_list, 1),
    "add_to_list": FuncPart(add_to_list, 2),
    "block": FuncPart(block, 1),
    "end_block": FuncPart(end_block, 1),
}
