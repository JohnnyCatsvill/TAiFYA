import graphviz

from SLR1 import Rule, SLR
from SLR1 import WordType
from constants.constants_slr import *
from functions import f
from id_generator import get_id, generator
from lexer import Token
from slr_exceptions.slr_exception import SLRException, SLRRunnerException
from slr_exceptions.exceptions_enum import SLRErrId


def runner(slr: SLR, lexer: list[Token], rules: list[Rule], show_parse: bool = False):
    slr_table = slr.df
    starter_word = slr.starter_word
    ok_word = slr.ok_word

    # This could not be valid check, but i could be wrong
    # nonterms = [i.left for i in rules]
    # for i, v in enumerate(lexer):
    #     if v.token in nonterms:
    #         raise SLRException(SLRErrId.NONTERMINAL_IN_INPUT_STACK, v.word, v.row, v.column)

    rules_length = {i + 1: len(v.right) - (i == 0 or v.right[0].type == WordType.EMPTY) for i, v in enumerate(rules)}
    # indexes_to_words = {i + 1: Token("X", v.left, 0, 0, get_id()) for i, v in enumerate(rules)}

    input_stack = lexer[::-1]
    left_stack = []
    right_stack = [[starter_word]]

    function_args = {i: [] for i in f}

    dot = graphviz.Digraph(comment='The Round Table')

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
                fold_into = rules[next_move[0].row - 1]
                popped_left = []
                popped_right = []
                for i in range(rules_length[next_move[0].row]):  # pop x times
                    popped_left.append(left_stack.pop())
                    popped_right.append(right_stack.pop())

                popped_left = popped_left[::-1]
                popped_right = popped_right[::-1]
                result = dict()

                for zipped in zip(fold_into.right, popped_left):
                    r, l = zipped
                    for a in r.action:

                        function_args[a].append(l.values)
                        if a == "pass":
                            last_node = l.values.get("last_node", l.graphviz_id)
                            last_node_values = l.values.get("last_node_data", l.values)
                            if not result.get("last_node"):
                                result.update({"last_node": []})
                                result.update({"last_node_data": []})
                            result["last_node"].append(last_node)
                            result["last_node_data"].append(last_node_values)
                            result.update({"passing": True})

                        if len(function_args[a]) >= f[a].arg_length:
                            result.update(f[a].f(function_args[a]))


                new_token = Token("X", fold_into.left, 0, 0, next(generator), result)
                input_stack.append(new_token)

                if not result.get("passing"):
                    dot.node(str(new_token.graphviz_id), new_token.word + " as " + new_token.token)

                for i in popped_left:
                    node_name = ""
                    if i.values:
                        node_name = f"{i.word if i.word != 'X' else ''} {i.token}{' v=' + str(i.values.get('val')) if i.values.get('val') else ''}{' t=' + i.values.get('type') if i.values.get('type') else ''}"
                    else:
                        node_name = f"{i.word if i.word != 'X' else ''} {i.token}"

                    if not result.get("passing") and not i.values.get("passing"):
                        dot.node(str(i.graphviz_id), node_name)
                        dot.edge(str(i.graphviz_id), str(new_token.graphviz_id))
                    elif not result.get("passing") and i.values.get("passing"):
                        for node, value in zip(i.values.get("last_node"), i.values.get("last_node_data")):
                            dot.node(str(node), str(value.get("val")) + " " + str(value.get("type")) )
                            dot.edge(str(node), str(new_token.graphviz_id))

                function_args = {i: [] for i in f}
            else:
                token = input_stack.pop()
                left_stack.append(token)
                right_stack.append(next_move)

                for i in next_move:
                    for a in i.action2:
                        function_args[a].append(token.values)

                        if len(function_args[a]) >= f[a].arg_length:
                            result = f[a].f(function_args[a])

            if show_parse:
                print("\n" + f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

    # print(dot.source)
    dot.render('doctest-output/round-table.gv', view=True)
    return RUNNER_OK
