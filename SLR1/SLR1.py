from utils.SLR_list_to_DF import DF
from utils.pretty_table import pretty_2d_table
from interfaces.slr_interfaces import *
from slr_exceptions.exceptions_enum import SLRErrId
from slr_exceptions.slr_exception import SLRException, SLRRunnerException


def list_append(table: list[any], thing: any):
    if thing not in table:
        table.append(thing)
        return True
    else:
        return False


class SLR:

    @staticmethod
    def first(rules: list[Rule]):
        nonterms = set([rule.left for rule in rules])
        first_table: FirstTable = {i: [] for i in nonterms}

        # e_nonterms, show if nonterm has empty symbol, S->AB$ A->e A->a B->b, there A could be skipped through rule 2
        e_nonterms = {rules[i].left: i + 1 for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}

        changed = True  # run while no changes left
        while changed:
            changed = False

            for rule in rules:
                e_fold = 0
                for right_word in rule.right:
                    if right_word.type in [WordType.TERM, WordType.NONTERM, WordType.END]:
                        changed += list_append(first_table[rule.left], right_word.add_e_fold(e_fold))

                        if right_word.type == WordType.NONTERM and right_word.str in first_table:
                            for i in first_table[right_word.str]:
                                changed += list_append(first_table[rule.left], i)

                        if right_word.str in e_nonterms:
                            e_fold = e_nonterms[right_word.str]
                        else:
                            break

        return first_table

    def follow(self, rules: list[Rule]):

        e_nonterms = {rules[i].left: i + 1 for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}

        first_table = SLR.first(rules)
        follow_table: FollowTable = dict()

        for rule_index in range(len(rules)):
            rule = rules[rule_index]
            for word_index in range(len(rule.right)):
                word = rule.right[word_index]
                follow_table[word] = []  # new

        follow_table[self.starter_word] = []

        last_table = {"not_empty": "not_empty"}
        while follow_table != last_table:
            last_table = deepcopy(follow_table)

            typed_follow_word = follow_table[self.starter_word]

            parsed_rule = rules[0].right
            next_letter = parsed_rule[0]

            if next_letter.type in [WordType.TERM, WordType.END]:
                list_append(typed_follow_word, next_letter)
            elif next_letter.type == WordType.NONTERM:
                list_append(typed_follow_word, next_letter)

                for i in first_table[next_letter.str]:
                    list_append(typed_follow_word, i)

                if next_letter in follow_table:
                    if next_letter.str in e_nonterms:
                        for i in follow_table[next_letter]:
                            list_append(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))

            for rule_index in range(len(rules)):
                rule = rules[rule_index]
                cur_nonterm = rule.left
                parsed_rule = deepcopy(rule.right)

                for word_index in range(len(parsed_rule)):
                    word = parsed_rule[word_index]
                    typed_follow_word = follow_table[word]

                    if word_index + 1 < len(parsed_rule):
                        next_letter = parsed_rule[word_index + 1]

                        if next_letter.type in [WordType.TERM, WordType.END]:
                            list_append(typed_follow_word, next_letter)

                        elif next_letter.type == WordType.NONTERM:
                            list_append(typed_follow_word, next_letter)

                            for i in first_table[next_letter.str]:
                                list_append(typed_follow_word, i)

                            if next_letter in follow_table:
                                if next_letter.str in e_nonterms:
                                    for i in follow_table[next_letter]:
                                        list_append(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))

                    elif word.type != WordType.EMPTY:
                        for i in follow_table:
                            if i.str == cur_nonterm:
                                for j in follow_table[i]:
                                    list_append(typed_follow_word, j)

        items_to_delete = []
        for i, j in follow_table.items():
            if i.type in [WordType.EMPTY, WordType.END]:
                items_to_delete.append(i)

        for i in items_to_delete:
            follow_table.pop(i)

        return follow_table

    def slr(self, rules: list[Rule]):
        follow_table = self.follow

        nonterms = []
        for rule in rules:
            if rule.left not in nonterms:
                nonterms.append(rule.left)

        terms = []
        for rule in rules:
            for word in rule.right:
                if word.type == WordType.TERM and word.str not in terms:
                    terms.append(word.str)

        slr_table = [[i for i in [""] + list(nonterms) + list(terms) + [END_SYMBOL]]]

        for left, right in follow_table.items():
            thing_to_append = [[] for i in slr_table[0][1:]]
            thing_to_append.insert(0, [left])

            for i in range(1, len(slr_table[0])):
                for j in range(len(right)):
                    word = right[j]
                    if slr_table[0][i] == word.str:

                        if left.type == WordType.STARTER or len(rules[left.row - 1].right) > int(
                                left.col) + (1 if left.row == 1 else 0):
                            if word not in thing_to_append[i]:
                                thing_to_append[i].append(word)

                            if left.row == 0:
                                if self.ok_word not in thing_to_append[1]:
                                    thing_to_append[1].append(self.ok_word)

                        else:
                            fold_word = Word(WordType.FOLD, "R", left.row)
                            if fold_word not in thing_to_append[i]:
                                thing_to_append[i].append(fold_word)

            slr_table.append(thing_to_append)

        for row in slr_table[1:]:
            for col_index in range(1, len(row)):
                cell = row[col_index]
                new_cell = []
                for word_index in range(len(cell)):
                    if cell[word_index].e_fold > 0:
                        fold_word = Word(WordType.FOLD, "R", cell[word_index].e_fold)
                        if fold_word not in new_cell:
                            new_cell.append(fold_word)
                    else:
                        new_cell.append(cell[word_index])

                row[col_index] = new_cell

        something_changed = True
        while something_changed:
            something_changed = False
            for row in slr_table[1:]:
                for cell in row[1:]:
                    if len(cell) > 1:
                        # new_row_name = ", ".join(cell)

                        need_to_do = True

                        for i in slr_table[1:]:
                            if cell == i[0]:
                                need_to_do = False

                        if need_to_do:
                            something_changed = True
                            thing_to_append = [[] for i in slr_table[0][1:]]
                            thing_to_append.insert(0, cell)

                            for needed_rows in cell:
                                for rows in slr_table[1:]:
                                    if rows[0] == [needed_rows]:
                                        for cells_num in range(1, len(rows)):
                                            for cell_items in rows[cells_num]:
                                                list_append(thing_to_append[cells_num], cell_items)

                            slr_table.append(thing_to_append)

        return slr_table

    @staticmethod
    def check_if_it_slr(slr_table: list[list[list[Word]]]):
        for row_num in range(1, len(slr_table)):
            row = slr_table[row_num]
            for cell_num, cell in enumerate(row[1:]):
                if len(cell) >= 2:
                    move = False
                    fold = False

                    for cell_elem in cell:
                        if cell_elem.type == WordType.FOLD:
                            if not fold:
                                fold = True
                            else:
                                raise SLRException(SLRErrId.DOUBLE_FOLD_IN_ONE_CELL, str(cell), str(row[0]),
                                                   str(slr_table[0][cell_num]))
                        else:
                            move = True

                    if move and fold:
                        raise SLRException(SLRErrId.MOVE_AND_FOLD_IN_ONE_CELL, str(cell), str(row[0]),
                                           str(slr_table[0][cell_num]))

    def runner_for_list_of_strings(self, slr_table: DF, input: list[str], rules: list[Rule], show_parse: bool = False):

        nonterms = [i.left for i in rules]
        for i, v in enumerate(input):
            if v in nonterms:
                raise SLRRunnerException(SLRErrId.NONTERMINAL_IN_INPUT_STACK, v, 0, i)

        rules_length = {i + 1: len(v.right) - (i == 0 or v.right[0].type == WordType.EMPTY) for i, v in
                        enumerate(rules)}
        word_by_indexes = {i + 1: v.left for i, v in enumerate(rules)}

        input_stack = input[::-1]
        left_stack = []
        right_stack = [[self.starter_word]]

        if show_parse:
            print(f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

        while right_stack != [[self.starter_word], [self.ok_word]] or left_stack != [self.starter_word.str]:
            if not input_stack:
                raise SLRRunnerException(SLRErrId.EMPTY_INPUT_STACK)
            elif not (elemToken := input_stack[-1]) in slr_table.df:
                raise SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_TOKEN, elemToken)
            elif not (elemIndex := str(right_stack[-1])) in slr_table.df.index:
                raise SLRRunnerException(SLRErrId.NON_GRAMMAR_SYMBOL_WORD, elemIndex)
            elif not (next_move := slr_table.get(right_stack[-1], input_stack[-1])):
                raise SLRRunnerException(SLRErrId.NOWHERE_TO_MOVE_NEXT, str(next_move), elemIndex, elemToken)
            else:
                if next_move[0].type == WordType.FOLD:
                    for i in range(rules_length[next_move[0].row]):
                        left_stack.pop()
                        right_stack.pop()
                    input_stack.append(word_by_indexes[next_move[0].row])
                else:
                    left_stack.append(input_stack.pop())
                    right_stack.append(next_move)

            if show_parse:
                print("\n" + f"разбор  INPUT-{input_stack}  RIGHT-{right_stack}  LEFT-{left_stack}")

        return RUNNER_OK

    def __init__(self,
                 rules: list[list[str, list[str], list[callable]]],
                 show_slr: bool = False,
                 show_first: bool = False,
                 show_follow: bool = False):

        self.rules = parse_all_rules(rules)

        self.starter_word = Word(WordType.STARTER, self.rules[0].left)
        self.ok_word = Word(WordType.OK_WORD, "OK")

        self.first = SLR.first(self.rules)
        if show_first:
            print(self.first)

        self.follow = self.follow(self.rules)
        if show_follow:
            print(self.follow)

        self.slr = self.slr(self.rules)
        self.df = DF(self.slr)
        if show_slr:
            pretty_2d_table(self.slr)

        SLR.check_if_it_slr(self.slr)

    def run(self, input_text: list[str], show_err: bool = False, show_parsing: bool = False):
        try:
            self.runner_for_list_of_strings(self.df, input_text, self.rules, show_parsing)
        except (SLRException, SLRRunnerException) as e:
            if show_err:
                print(e)
            return e
        return RUNNER_OK
