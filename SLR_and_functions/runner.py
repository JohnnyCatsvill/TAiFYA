from SLR1 import SLR
from constants.constants_slr import RUNNER_ERROR, RUNNER_OK
from interfaces.slr_interfaces import Rule, WordType


class Token2:
    def __init__(self, value: any, token: str, row: int = 0, column: int = 0):
        self.value: any = value
        self.token: str = token
        self.row: int = row
        self.col: int = column


def runner(slr: SLR, lexer: list[Token2], rules: list[Rule], show_parse: bool = False):
    slr_table = slr.df
    starter_word = slr.starter_word
    ok_word = slr.ok_word

    nonterms = [i.left for i in rules]
    if any([i.token in nonterms for i in lexer]):
        raise Exception(RUNNER_ERROR, "ИНПУТ СТАК НЕ ВАЛИДЕН, в него затесался нетерминал")

    rules_length = {i + 1: len(v.right) - (i == 0 or v.right[0].type == WordType.EMPTY) for i, v in enumerate(rules)}
    indexes_to_words = {i + 1: Token2("X", v.left, 0, 0) for i, v in enumerate(rules)}

    input_stack = lexer[::-1]
    left_stack = []
    right_stack = [[starter_word]]

    if show_parse:
        print(f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

    while right_stack != [[starter_word], [ok_word]] or left_stack != [Token2("X", starter_word.str, 0, 0)]:
        if not input_stack:
            raise Exception(RUNNER_ERROR, "ИНПУТ СТАК ПУСТ, а нам из него еще данные брать хотелось")
        elif not (elem := input_stack[-1].token) in slr_table.df:
            raise Exception(RUNNER_ERROR, f"ИНПУТ СИМВОЛ ВНЕ ГРАММАТИКИ, {elem} отсутствует в SLR")
        elif not (elem := str(right_stack[-1])) in slr_table.df.index:
            raise Exception(RUNNER_ERROR, f"ИНПУТ СИМВОЛ ВНЕ ГРАММАТИКИ, {elem} отсутствует в SLR")
        elif not (next_move := slr_table.get(right_stack[-1], input_stack[-1].token)):
            raise Exception(RUNNER_ERROR, "НЕТ ДАЛЬНЕЙШЕГО ХОДА, наступили на пустую ячейку")
        else:
            if next_move[0].type == WordType.FOLD:
                for i in range(rules_length[next_move[0].row]):  # pop x times
                    left_stack.pop()
                    right_stack.pop()
                input_stack.append(indexes_to_words[next_move[0].row])
            else:
                left_stack.append(input_stack.pop())
                right_stack.append(next_move)

            if show_parse:
                print("\n" + f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

    return RUNNER_OK