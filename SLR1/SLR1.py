from TablePrinter import *
from constants import *
from enum import Enum
from copy import deepcopy


class WordType(Enum):
    NONTERM = 0
    TERM = 1
    FOLD = 2
    END = 3
    EMPTY = 4
    OK_WORD = 5
    STARTER = 6


class Word:
    def __init__(self, word_type: WordType, word: str, row: int, column: int = 0, e_fold: int = 0,
                 action: callable = None):
        self.type: WordType = word_type
        self.str: str = word
        self.row: int = row
        self.col: int = column
        self.e_fold: int = e_fold
        self.action: callable = action

    def __hash__(self):
        return hash((self.str, self.type, self.row, self.col, self.e_fold, self.action))

    def __repr__(self):
        column = ' ' + str(self.col) if self.col > 0 else ''
        e_fold = ' ' + str(self.e_fold) if self.e_fold > 0 else ''
        return f"{self.str} {self.row}{column}{e_fold}"

    def __eq__(self, other):
        return all([
            self.type == other.type,
            self.str == other.str,
            self.row == other.row,
            self.col == other.col,
            self.action == other.action,
        ])

    @staticmethod
    def get_type(word: str, nonterms: set[str], terms: set[str]):
        if word in nonterms:
            return WordType.NONTERM
        elif word in terms:
            return WordType.TERM
        elif word == EMPTY_SYMBOL:
            return WordType.EMPTY
        elif word == END_SYMBOL:
            return WordType.END
        else:
            raise "Unknown word type"

    def add_e_fold(self, e_fold: int):
        output: Word = deepcopy(self)
        output.e_fold = e_fold
        return output


FirstTable = dict[str, list[Word]]
FollowTable = dict[Word, list[Word]]


class Rule:
    def __init__(self, left: str, right: list[Word]):
        self.left: str = left
        self.right: list[Word] = right

    def __repr__(self):
        return f"{self.left}->{[i.str for i in self.right]}"


def parse_all_rules(rules: list[list[str, list[str], list[callable]]]) -> list[Rule]:
    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
    set_of_control_symbols = {EMPTY_SYMBOL, END_SYMBOL}
    set_of_terminals = set([letter for rule_pack in rules for letter in parse_rule(rule_pack[1][0]) if
                            letter not in set_of_nonterminals and letter not in set_of_control_symbols])

    def get_type(word_str):
        if word_str in set_of_nonterminals:
            return WordType.NONTERM
        elif word_str in set_of_terminals:
            return WordType.TERM
        elif word_str == EMPTY_SYMBOL:
            return WordType.EMPTY
        elif word_str == END_SYMBOL:
            return WordType.END
        else:
            raise "Unknown word type"

    list_of_rules = []
    for rule_index in range(len(rules)):
        rule = rules[rule_index]
        left = rule[0]
        right = rule[1][0]
        actions = [] if len(rule) < 3 else rule[2]

        parsed_right = right.split(RULE_DIVIDER)
        while len(actions) < len(parsed_right):
            actions.append(None)

        output_right = []
        for word_index in range(len(parsed_right)):
            word_letters = parsed_right[word_index]
            word = Word(get_type(word_letters),
                        word_letters,
                        rule_index + 1,
                        word_index + 1,
                        action=actions[word_index])
            output_right.append(word)

        list_of_rules.append(Rule(left, output_right))
    return list_of_rules


def parse_rule(rule: str, divider=" "):
    rule_list: list[str] = rule.split(divider)
    return rule_list


def add_to_table(table, thing):
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
                        changed += add_to_table(first_table[rule.left], right_word.add_e_fold(e_fold))

                        if right_word.type == WordType.NONTERM and right_word.str in first_table:
                            for i in first_table[right_word.str]:
                                changed += add_to_table(first_table[rule.left], i)

                        if right_word.str in e_nonterms:
                            e_fold = e_nonterms[right_word.str]
                        else:
                            break

        return first_table

    @staticmethod
    def follow(rules: list[Rule]):

        # nonterms = set([rule.left for rule in rules])
        # terms = set([letter.str for rule in rules for letter in rule.right if
        #              letter.type not in [WordType.NONTERM, WordType.EMPTY]])
        e_nonterms = {rules[i].left: i + 1 for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}

        first_table = SLR.first(rules)
        follow_table: FollowTable = dict()

        for rule_index in range(len(rules)):
            rule = rules[rule_index]
            for word_index in range(len(rule.right)):
                word = rule.right[word_index]
                follow_table[word] = []  # new

        follow_table[Word(WordType.STARTER, rules[0].left, 0, 0)] = []

        last_table = {"not_empty": "not_empty"}
        while follow_table != last_table:
            last_table = deepcopy(follow_table)

            typed_follow_word = follow_table[
                Word(WordType.STARTER, rules[0].left, 0, 0)]

            parsed_rule = rules[0].right
            next_letter = parsed_rule[0]

            if next_letter.type in [WordType.TERM, WordType.END]:
                add_to_table(typed_follow_word, next_letter)
            elif next_letter.type == WordType.NONTERM:
                add_to_table(typed_follow_word, next_letter)

                for i in first_table[next_letter.str]:
                    add_to_table(typed_follow_word, i)

                if next_letter in follow_table:
                    if next_letter.str in e_nonterms:
                        for i in follow_table[next_letter]:
                            add_to_table(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))

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
                            add_to_table(typed_follow_word, next_letter)

                        elif next_letter.type == WordType.NONTERM:
                            add_to_table(typed_follow_word, next_letter)

                            for i in first_table[next_letter.str]:
                                add_to_table(typed_follow_word, i)

                            if next_letter in follow_table:
                                if next_letter.str in e_nonterms:
                                    for i in follow_table[next_letter]:
                                        add_to_table(typed_follow_word, i.add_e_fold(e_nonterms[next_letter.str]))

                    elif word.type != WordType.EMPTY:
                        for i in follow_table:
                            if i.str == cur_nonterm:
                                for j in follow_table[i]:
                                    add_to_table(typed_follow_word, j)

        items_to_delete = []
        for i, j in follow_table.items():
            if i.type in [WordType.EMPTY, WordType.END]:
                items_to_delete.append(i)

        for i in items_to_delete:
            follow_table.pop(i)

        return follow_table

    @staticmethod
    def slr(rules: list[Rule]):
        follow_table = SLR.follow(rules)

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
                                if Word(WordType.OK_WORD, "OK", 0) not in thing_to_append[1]:
                                    thing_to_append[1].append(Word(WordType.OK_WORD, "OK", 0))

                        else:
                            if Word(WordType.FOLD, "R", left.row) not in thing_to_append[i]:
                                thing_to_append[i].append(Word(WordType.FOLD, "R", left.row))

            slr_table.append(thing_to_append)

        for row in slr_table[1:]:
            for col_index in range(1, len(row)):
                cell = row[col_index]
                new_cell = []
                for word_index in range(len(cell)):
                    if cell[word_index].e_fold > 0:
                        if Word(WordType.FOLD, "R", cell[word_index].e_fold) not in new_cell:
                            new_cell.append(Word(WordType.FOLD, "R", cell[word_index].e_fold))
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
                                                add_to_table(thing_to_append[cells_num], cell_items)

                            slr_table.append(thing_to_append)

        return slr_table

    @staticmethod
    def check_if_it_slr(slr_table: list[list[list[Word]]]):
        for row_num in range(1, len(slr_table)):
            row = slr_table[row_num]
            for cell in row[1:]:
                if len(cell) >= 2:
                    move = False
                    fold = False

                    for cell_elem in cell:
                        if cell_elem.type == WordType.FOLD:
                            if not fold:
                                fold = True
                            else:
                                raise Exception(f"Non SLR Grammar \n \n {cell} in {row_num}th pos {row[0]} nonterm")
                        else:
                            move = True

                    if move and fold:
                        raise Exception(f"Non SLR Grammar \n \n {cell} in {row_num}th pos {row[0]} nonterm")

    @staticmethod
    def runner(slr_table: list[list[list[Word]]], input: list[str], rules: list[Rule], show: bool = False):

        dict_of_rule_length = {i + 1: len(rules[i].right) - (i == 0 or rules[i].right[0].type == WordType.EMPTY) for i in range(len(rules))}
        dict_of_rule_letters = {i + 1: rules[i].left for i in range(len(rules))}

        input_stack = input[::-1]
        nonterms = [i.left for i in rules]
        if any([i in nonterms for i in input]):
            if show:
                print("в входные данные затесался нетерминал")
            return RUNNER_FAIL

        left_stack = []
        right_stack = [[Word(WordType.STARTER, rules[0].left, 0, 0)]]

        if show:
            print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)

        while right_stack[-1] != [Word(WordType.OK_WORD, "OK", 0)]:
            for row in slr_table:
                if row[0] == right_stack[-1]:
                    cell_num = 0
                    for cell_num in range(1, len(slr_table[0])):
                        if not input_stack:
                            if show:
                                print("НЕ ПОДХОДИТ, пустой инпут стак, а конца так и не видно")
                            return RUNNER_FAIL

                        if slr_table[0][cell_num] == input_stack[-1]:
                            if not row[cell_num]:
                                if show:
                                    print("НЕ ПОДХОДИТ, наступили на ячейку где нет следующего хода")
                                return RUNNER_FAIL
                            else:

                                if len(row[cell_num]) > 1:
                                    left_stack.append(input_stack.pop())
                                    right_stack.append(row[cell_num])
                                else:
                                    if row[cell_num][0].type == WordType.FOLD:

                                        for i in range(dict_of_rule_length[row[cell_num][0].row]):
                                            left_stack.pop()
                                            right_stack.pop()
                                        input_stack.append(dict_of_rule_letters[row[cell_num][0].row])
                                    else:
                                        left_stack.append(input_stack.pop())
                                        right_stack.append(row[cell_num])
                            cell_num -= 1
                            break
                    if cell_num + 1 == len(slr_table[0]):
                        if show:
                            print("НЕ ПОДХОДИТ")
                        return RUNNER_FAIL
                    break
            if show:
                print()
                print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)

        if left_stack == [rules[0].left]:
            if show:
                print("ПОДХОДИТ")
            return RUNNER_OK
        else:
            if show:
                print(f"НЕ ПОДХОДИТ, в стаке валяются лишние символы -> {left_stack[1:]}")
            return RUNNER_FAIL

    def __init__(self, rules, show_slr: bool = False, show_first: bool = False, show_follow: bool = False):
        self.rules = rules

        self.first = SLR.first(rules)
        if show_first:
            print(self.first)

        self.follow = SLR.follow(rules)
        if show_follow:
            print(self.follow)

        self.slr = SLR.slr(rules)
        if show_slr:
            pretty_2d_table(self.slr)
        SLR.check_if_it_slr(self.slr)

    def run(self, input_text: list[str], show_parsing: bool = False):
        return self.runner(self.slr, input_text, self.rules, show_parsing)
