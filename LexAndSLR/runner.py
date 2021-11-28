from SLR1 import Rule, SLR
from SLR1 import WordType
from constants.constants_slr import *
from lexer import Token
from slr_exceptions.slr_exception import SLRException, SLRRunnerException
from slr_exceptions.exceptions_enum import SLRErrId


def runner(slr: SLR, lexer: list[Token], rules: list[Rule], show_parse: bool = False):
    slr_table = slr.df
    starter_word = slr.starter_word
    ok_word = slr.ok_word

    nonterms = [i.left for i in rules]
    for i, v in enumerate(lexer):
        if v.token in nonterms:
            raise SLRException(SLRErrId.NONTERMINAL_IN_INPUT_STACK, v.word, v.row, v.column)

    rules_length = {i + 1: len(v.right) - (i == 0 or v.right[0].type == WordType.EMPTY) for i, v in enumerate(rules)}
    indexes_to_words = {i + 1: Token("X", v.left, 0, 0) for i, v in enumerate(rules)}

    input_stack = lexer[::-1]
    left_stack = []
    right_stack = [[starter_word]]

    if show_parse:
        print(f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

    while right_stack != [[starter_word], [ok_word]] or left_stack != [Token("X", starter_word.str, 0, 0)]:
        if not input_stack:
            raise SLRRunnerException(SLRErrId.EMPTY_INPUT_STACK)
        elif not (elemToken := input_stack[-1]).token in slr_table.df:
            raise SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN, elemToken.word, elemToken.row, elemToken.column)
        elif not (elemIndex := str(right_stack[-1])) in slr_table.df.index:
            raise SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_WORD, elemIndex, elemToken.row, elemToken.column)
        elif not (next_move := slr_table.get(right_stack[-1], input_stack[-1].token)):
            raise SLRRunnerException(SLRErrId.NOWHERE_TO_MOVE_NEXT, str(next_move), elemIndex, elemToken.token)
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

# def runner(slr_table: list[list[list[Word]]],
#            lexer: list[Token],
#            rules: list[Rule],
#            show: bool = False):
#
#     dict_of_rule_length = {i + 1: len(rules[i].right) - (i == 0 or rules[i].right[0].type == WordType.EMPTY) for i in range(len(rules))}
#     dict_of_rule_letters = {i + 1: Token("X", rules[i].left, 0, 0) for i in range(len(rules))}
#
#     input_stack = lexer[::-1]
#     nonterms = [i.left for i in rules]
#     if any([i in nonterms for i in lexer]):
#         if show:
#             print("в входные данные затесался нетерминал")
#         return RUNNER_FAIL
#
#     left_stack = []
#     right_stack = [[Word(WordType.STARTER, rules[0].left, 0, 0)]]
#
#     if show:
#         print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)
#
#     while right_stack[-1] != [Word(WordType.OK_WORD, "OK", 0)]:
#         for row in slr_table:
#             if row[0] == right_stack[-1]:
#                 cell_num = 0
#                 for cell_num in range(1, len(slr_table[0])):
#                     if not input_stack:
#                         if show:
#                             print("НЕ ПОДХОДИТ, пустой инпут стак, а конца так и не видно")
#                         return RUNNER_FAIL
#
#                     if slr_table[0][cell_num] == input_stack[-1].token:
#                         if not row[cell_num]:
#                             if show:
#                                 print("НЕ ПОДХОДИТ, наступили на ячейку где нет следующего хода")
#                             return RUNNER_FAIL
#                         else:
#
#                             if len(row[cell_num]) > 1:
#                                 left_stack.append(input_stack.pop())
#                                 right_stack.append(row[cell_num])
#                             else:
#                                 if row[cell_num][0].type == WordType.FOLD:
#
#                                     for i in range(dict_of_rule_length[row[cell_num][0].row]):
#                                         left_stack.pop()
#                                         right_stack.pop()
#                                     input_stack.append(dict_of_rule_letters[row[cell_num][0].row])
#                                 else:
#                                     left_stack.append(input_stack.pop())
#                                     right_stack.append(row[cell_num])
#                         cell_num -= 1
#                         break
#                 if cell_num + 1 == len(slr_table[0]):
#                     if show:
#                         print("НЕ ПОДХОДИТ")
#                     return RUNNER_FAIL
#                 break
#         if show:
#             print()
#             print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)
#
#     last = [Token("X", rules[0].left, 0, 0)]
#     if len(left_stack) == len(last) and left_stack[0].token == last[0].token and left_stack[0].word == last[0].word:
#         if show:
#             print("ПОДХОДИТ")
#         return RUNNER_OK
#     else:
#         if show:
#             print(f"НЕ ПОДХОДИТ, в стаке валяются лишние символы -> {left_stack[1:]}")
#         return RUNNER_FAIL
