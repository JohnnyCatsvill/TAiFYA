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


class Word:
    def __init__(self, word_type: WordType, word: str, row: int, column: int = 0, e_fold: int = 0,
                 action: callable = None):
        self.type: WordType = word_type
        self.str: str = word
        self.row: int = row
        self.col: int = column
        self.e_fold: int = e_fold
        self.action: callable = action

    def __repr__(self):
        return f"{self.str} {self.row}{' ' + str(self.col) if self.col > 0 else ''}{' ' + str(self.e_fold) if self.e_fold > 0 else ''}"

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
    set_of_terminals = set([letter for rule_pack in rules for letter in ParseRule(rule_pack[1][0]) if
                            letter not in set_of_nonterminals and letter not in set_of_control_symbols])

    def get_type(word):
        if word in set_of_nonterminals:
            return WordType.NONTERM
        elif word in set_of_terminals:
            return WordType.TERM
        elif word == EMPTY_SYMBOL:
            return WordType.EMPTY
        elif word == END_SYMBOL:
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
            word = Word(get_type(word_letters), word_letters, rule_index+1, word_index+1, action=actions[word_index])
            output_right.append(word)

        list_of_rules.append(Rule(left, output_right))
    return list_of_rules


def ParseRule(rule: str, divider=" "):
    rule_list: list[str] = rule.split(divider)
    return rule_list


def AddToTable(table, thing):
    if thing not in table:
        table.append(thing)
        return True
    else:
        return False


class SLR:

    @staticmethod
    def other_first(rules: list[Rule]):
        nonterms = set([rule.left for rule in rules])
        control_symbols = {EMPTY_SYMBOL, END_SYMBOL}
        terms = set([letter.str for rule in rules for letter in rule.right if letter.type == WordType.TERM])
        e_nonterms = {rules[i].left: str(i + 1) for i in range(len(rules)) if rules[i].right[0].type == WordType.EMPTY}

        first_table = {i: [] for i in nonterms}
        empty_table = {i: [] for i in nonterms}  # first через e символы
        recurse_table = {i: [] for i in nonterms}  # first через собственный символ
        # ПРИМЕР: H->S, S->(S), S->e; тут S имеет first )23 ,
        # но H не может воспользоваться этим first

        typed_first_table: FirstTable = {i: [] for i in nonterms}
        typed_empty_table: FirstTable = {i: [] for i in nonterms}
        typed_recurse_table: FirstTable = {i: [] for i in nonterms}

        changed = True
        while changed:
            changed = False

            for rule_index in range(len(rules)):
                rule = rules[rule_index]
                first_right = deepcopy(rule.right[0])
                left = rule.left

                there_are_empty_nonterminal = True
                empty_nonterminal_entrance = 1
                some_rule_adder = ""
                while there_are_empty_nonterminal:
                    there_are_empty_nonterminal = False
                    if first_right.type in [WordType.TERM, WordType.NONTERM]:
                        changed = changed or AddToTable(first_table[left],
                                                        first_right.str + " " + str(rule_index + 1) + " " + str(
                                                            empty_nonterminal_entrance) + some_rule_adder)

                        not_null_e_fold = some_rule_adder or "0"  # new and v this one too
                        AddToTable(typed_first_table[left], first_right.add_e_fold(int(not_null_e_fold.split(" ")[-1])))

                        if first_right.type == WordType.NONTERM and first_right.str in first_table:
                            for i in first_table[first_right.str]:
                                changed = changed or AddToTable(first_table[left], i)

                            for i in typed_first_table[first_right.str]:  # new
                                AddToTable(typed_first_table[left], i)     #

                            if first_right.str in e_nonterms:
                                there_are_empty_nonterminal = True
                                some_rule_adder += " " + e_nonterms[first_right.str]
                                first_right = deepcopy(rule.right[empty_nonterminal_entrance])
                                empty_nonterminal_entrance += 1

                    elif first_right.type == WordType.EMPTY:
                        afterlooking_symbols = {left}
                        afterlooking_symbols_changed = True

                        while afterlooking_symbols_changed:
                            afterlooking_symbols_changed = False

                            for new_rule_index in range(len(rules)):
                                new_rule = rules[new_rule_index]
                                new_left = new_rule.left

                                for word_index in range(len(new_rule.right)):
                                    word = new_rule.right[word_index]

                                    if word.str in afterlooking_symbols:
                                        if word_index + 1 < len(new_rule.right):
                                            next_word = new_rule.right[word_index + 1]

                                            if new_left != left:
                                                changed = changed or AddToTable(empty_table[left],
                                                                                next_word.str + " " + str(
                                                                                new_rule_index + 1) + " " + str(
                                                                                word_index + 2) + " " + str(
                                                                                rule_index + 1))

                                                AddToTable(typed_empty_table[left], next_word.add_e_fold(rule_index + 1))

                                            else:
                                                changed = changed or AddToTable(recurse_table[left],
                                                                                next_word.str + " " + str(
                                                                                new_rule_index + 1) + " " + str(
                                                                                word_index + 2) + " " + str(
                                                                                rule_index + 1))

                                                AddToTable(typed_recurse_table[left], next_word.add_e_fold(rule_index + 1))

                                            if next_word.str in first_table:
                                                for i in first_table[next_word.str]:
                                                    changed = changed or AddToTable(empty_table[left],
                                                                                    i + " " + str(rule_index + 1))

                                                for i in typed_first_table[next_word.str]:
                                                    AddToTable(typed_empty_table[left], i.add_e_fold(rule_index + 1))


                                        else:
                                            afterlooking_symbols_changed = new_rule.left not in afterlooking_symbols
                                            afterlooking_symbols.add(new_rule.left)
                                            # afterlooking_symbols_changed = True

        print([typed_first_table, typed_empty_table, typed_recurse_table])
        return [first_table, empty_table, recurse_table]

    def First(self, rules):
        set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
        set_of_control_symbols = {EMPTY_SYMBOL, END_SYMBOL}
        set_of_terminals = set([letter for rule_pack in rules for letter in ParseRule(rule_pack[1][0]) if
                                letter not in set_of_nonterminals and letter not in set_of_control_symbols])
        set_of_empty_nonterminals = {rules[rule_pack_num][0]: str(rule_pack_num + 1) for rule_pack_num in
                                     range(len(rules)) if rules[rule_pack_num][1][0] == EMPTY_SYMBOL}

        first_table = {i: [] for i in set_of_nonterminals}
        empty_table = {i: [] for i in set_of_nonterminals}  # first через e символы
        recurse_table = {i: [] for i in
                         set_of_nonterminals}  # first через собственный символ ПРИМЕР: H->S, S->(S), S->e; тут S имеет first )23 , но H не может воспользоваться этим first

        typed_first_table: FirstTable = {i: [] for i in set_of_nonterminals}
        typed_empty_table: FirstTable = {i: [] for i in set_of_nonterminals}
        typed_recurse_table: FirstTable = {i: [] for i in set_of_nonterminals}

        table_was_changed = True
        while table_was_changed:
            table_was_changed = False

            for rule_pack_num in range(len(rules)):
                rule_pack = rules[rule_pack_num]
                first_letter = ParseRule(rule_pack[1][0])[0]
                cur_nonterm = rule_pack[0]

                there_are_empty_nonterminal = True
                empty_nonterminal_entrance = 1
                some_rule_adder = ""
                while there_are_empty_nonterminal:
                    there_are_empty_nonterminal = False
                    if first_letter in set_of_nonterminals | set_of_terminals:
                        table_was_changed = table_was_changed or AddToTable(first_table[cur_nonterm],
                                                                            first_letter + " " + str(
                                                                                rule_pack_num + 1) + " " + str(
                                                                                empty_nonterminal_entrance) + some_rule_adder)

                        if first_letter in set_of_nonterminals:
                            if first_letter in first_table:
                                for i in first_table[first_letter]:
                                    table_was_changed = table_was_changed or AddToTable(first_table[cur_nonterm], i)

                                if first_letter in set_of_empty_nonterminals:
                                    there_are_empty_nonterminal = True
                                    some_rule_adder = some_rule_adder + " " + set_of_empty_nonterminals[first_letter]
                                    first_letter = ParseRule(rule_pack[1][0])[empty_nonterminal_entrance]
                                    empty_nonterminal_entrance = empty_nonterminal_entrance + 1

                    elif first_letter == EMPTY_SYMBOL:
                        afterlooking_symbols = {cur_nonterm}
                        afterlooking_symbols_changed = True

                        while afterlooking_symbols_changed:
                            afterlooking_symbols_changed = False

                            for new_rule_pack_num in range(len(rules)):
                                new_rule_pack = rules[new_rule_pack_num]
                                new_cur_nonterm = new_rule_pack[0]
                                parsed_rule = ParseRule(new_rule_pack[1][0])

                                for letter_num in range(len(parsed_rule)):
                                    letter = parsed_rule[letter_num]

                                    if letter in afterlooking_symbols:
                                        if letter_num + 1 < len(parsed_rule):
                                            next_letter = parsed_rule[letter_num + 1]

                                            if new_cur_nonterm != cur_nonterm:
                                                table_was_changed = table_was_changed or AddToTable(
                                                    empty_table[cur_nonterm],
                                                    next_letter + " " + str(new_rule_pack_num + 1) + " " + str(
                                                        letter_num + 2) + " " + str(rule_pack_num + 1))

                                            else:
                                                table_was_changed = table_was_changed or AddToTable(
                                                    recurse_table[cur_nonterm],
                                                    next_letter + " " + str(new_rule_pack_num + 1) + " " + str(
                                                        letter_num + 2) + " " + str(rule_pack_num + 1))

                                            if next_letter in first_table:
                                                for i in first_table[next_letter]:
                                                    table_was_changed = table_was_changed or AddToTable(
                                                        empty_table[cur_nonterm], i + " " + str(rule_pack_num + 1))


                                        else:
                                            afterlooking_symbols_changed = new_rule_pack[0] not in afterlooking_symbols
                                            afterlooking_symbols.add(new_rule_pack[0])
                                            # afterlooking_symbols_changed = True

        # print([typed_first_table, typed_empty_table, typed_recurse_table])
        return [first_table, empty_table, recurse_table]

    def Follow(self, rules):
        _first_tables_ = self.First(rules)
        first_table = _first_tables_[0]
        empty_table = _first_tables_[1]
        recurse_table = _first_tables_[2]

        set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
        set_of_empty_nonterminals = {rules[rule_pack_num][0]: str(rule_pack_num + 1) for rule_pack_num in
                                     range(len(rules)) if rules[rule_pack_num][1][0] == EMPTY_SYMBOL}
        set_of_control_symbols = {EMPTY_SYMBOL}
        set_of_terminals = set([letter for rule_pack in rules for letter in ParseRule(rule_pack[1][0]) if
                                letter not in set_of_nonterminals and letter not in set_of_control_symbols])

        follow_table = dict()
        for rule_pack_num in range(len(rules)):
            for letter_num in range(len(ParseRule(rules[rule_pack_num][1][0]))):
                letter = ParseRule(rules[rule_pack_num][1][0])[letter_num]
                follow_table[letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 1)] = []
        last_table = {"why": "i dont understand!!!, <sobs>"}
        follow_table[rules[0][0]] = []

        while follow_table != last_table:
            last_table = copy.deepcopy(follow_table)

            first_nonterm = rules[0][0]
            follow_letter = follow_table[first_nonterm]

            parsed_rule = ParseRule(rules[0][1][0])
            next_letter = parsed_rule[0]

            # first_first_symbol = ParseRule(rules[0][1][0])[0]

            if next_letter in set_of_terminals:
                AddToTable(follow_letter, next_letter + " 1 1")
            elif next_letter in set_of_nonterminals:
                AddToTable(follow_letter, next_letter + " 1 1")
                for i in first_table[next_letter]:
                    AddToTable(follow_letter, i)
                if next_letter + " 1 1" in follow_table:
                    if next_letter in set_of_empty_nonterminals:
                        for i in follow_table[next_letter + " 1 1"]:
                            AddToTable(follow_letter, i + " " + set_of_empty_nonterminals[next_letter])

            for rule_pack_num in range(len(rules)):
                rule_pack = rules[rule_pack_num]
                cur_nonterm = rule_pack[0]
                parsed_rule = ParseRule(rule_pack[1][0])

                for letter_num in range(len(parsed_rule)):
                    letter = parsed_rule[letter_num]
                    follow_letter = follow_table[letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 1)]
                    # if letter in set_of_nonterminals:
                    if letter_num + 1 < len(parsed_rule):
                        next_letter = parsed_rule[letter_num + 1]

                        if next_letter in set_of_terminals:
                            AddToTable(follow_letter,
                                       next_letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 2))

                        elif next_letter in set_of_nonterminals:
                            AddToTable(follow_letter,
                                       next_letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 2))

                            for i in first_table[next_letter]:
                                AddToTable(follow_letter, i)

                            if next_letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 2) in follow_table:
                                if next_letter in set_of_empty_nonterminals:
                                    for i in follow_table[
                                        next_letter + " " + str(rule_pack_num + 1) + " " + str(letter_num + 2)]:
                                        AddToTable(follow_letter, i + " " + set_of_empty_nonterminals[next_letter])

                    elif letter != EMPTY_SYMBOL:
                        for i in follow_table:
                            splits = i.split(" ")
                            if splits[0] == cur_nonterm:
                                for j in follow_table[i]:
                                    AddToTable(follow_letter, j)

        items_to_delete = []
        for i, j in follow_table.items():
            if ParseRule(i)[0] == EMPTY_SYMBOL or ParseRule(i)[0] == END_SYMBOL:
                items_to_delete.append(i)

        for i in items_to_delete:
            follow_table.pop(i)

        return follow_table

    def SLR_Table(self, rules):
        follow_table = self.Follow(rules)
        # print(follow_table)

        set_of_control_symbols = {EMPTY_SYMBOL, END_SYMBOL}

        set_of_nonterminals = []
        for rule_pack in rules:
            if rule_pack[0] not in set_of_nonterminals:
                set_of_nonterminals.append(rule_pack[0])

        set_of_terminals = []
        for rule_pack in rules:
            for letter in ParseRule(rule_pack[1][0]):
                if letter not in set_of_nonterminals and letter not in set_of_control_symbols and letter not in set_of_terminals:
                    set_of_terminals.append(letter)

        slr_table = [[i for i in [""] + set_of_nonterminals + list(set_of_terminals) + [END_SYMBOL]]]

        for letter, follow in follow_table.items():
            thing_to_append = [[] for i in slr_table[0][1:]]
            thing_to_append.insert(0, letter)
            # print(thing_to_append)
            for i in range(1, len(slr_table[0])):
                for j in range(len(follow)):
                    j_letter = follow[j]
                    if slr_table[0][i] == ParseRule(j_letter)[0]:

                        if len(ParseRule(letter)) == 1 or len(
                                ParseRule(rules[int(ParseRule(letter)[1]) - 1][1][0])) > int(ParseRule(letter)[2]) + (
                                1 if ParseRule(letter)[1] == "1" else 0):
                            if j_letter not in thing_to_append[i]:
                                # if ParseRule(j_letter)[0] != END_SYMBOL:
                                thing_to_append[i].append(j_letter)
                            # else:
                            #    thing_to_append[i].append("R" + ParseRule(j_letter)[1])
                            if len(ParseRule(letter)) == 1:
                                if "OK" not in thing_to_append[1]:
                                    thing_to_append[1].append("OK")

                        else:
                            if "R " + ParseRule(letter)[1] not in thing_to_append[i]:
                                thing_to_append[i].append("R " + ParseRule(letter)[1])

            # print(thing_to_append)
            slr_table.append(thing_to_append)

        for row in slr_table[1:]:
            for cell_num in range(1, len(row)):
                cell = row[cell_num]
                new_cell = []
                for letter_num in range(len(cell)):
                    if len(ParseRule(cell[letter_num])) > 3:
                        if "R " + ParseRule(cell[letter_num])[-1] not in new_cell:
                            new_cell.append("R " + ParseRule(cell[letter_num])[-1])
                    else:
                        new_cell.append(cell[letter_num])
                        # cell[letter_num] = "R" + ParseRule(cell[letter_num])[-1]

                row[cell_num] = new_cell

        something_changed = True

        while something_changed:
            something_changed = False
            for row in slr_table[1:]:
                for cell in row[1:]:
                    if len(cell) > 1:
                        # print(cell)
                        new_row_name = ", ".join(cell)

                        need_to_do = True

                        for i in slr_table:
                            if new_row_name == i[0]:
                                need_to_do = False

                        if need_to_do:
                            something_changed = True
                            thing_to_append = [[] for i in slr_table[0][1:]]
                            thing_to_append.insert(0, new_row_name)

                            for needed_rows in cell:
                                for rows in slr_table:
                                    if rows[0] == needed_rows:
                                        for cells_num in range(1, len(rows)):
                                            for cell_items in rows[cells_num]:
                                                AddToTable(thing_to_append[cells_num], cell_items)
                                                # thing_to_append[cells_num].append(cell_items)

                            slr_table.append(thing_to_append)

                # for letter_num in range(len(cell)):
                #    if len(ParseRule(cell[letter_num])) > 3:
                #        cell[letter_num] = "R" + ParseRule(cell[letter_num])[-1]

        # Print_2D_Table(slr_table)
        # print(slr_table)
        return slr_table

    def CheckIfItSLR(self, slr_table):
        for row_num in range(1, len(slr_table)):
            row = slr_table[row_num]
            for cell in row[1:]:
                if len(cell) >= 2:
                    sdvig = False
                    svertka = False

                    for cell_elem in cell:
                        if len(ParseRule(cell_elem)) == 2:
                            if svertka == False:
                                svertka = True
                            else:
                                raise Exception(
                                    "Non SLR Grammar \n \n {} in {}th pos {} nonterm".format(cell, row_num, row[0]))
                        else:
                            sdvig = True

                    if sdvig and svertka:
                        raise Exception("Non SLR Grammar \n \n {} in {}th pos {} nonterm".format(cell, row_num, row[0]))

    def Runner(self, slr_table, input, rules):

        EMPTY_SYMBOL = "e"
        dict_of_rule_length = {
            i + 1: len(ParseRule(rules[i][1][0])) - (1 if i == 0 or ParseRule(rules[i][1][0])[0] == EMPTY_SYMBOL else 0)
            for i in range(len(rules))}
        dict_of_rule_letters = {i + 1: rules[i][0] for i in range(len(rules))}

        input_stack = [i for i in input.split(" ")[::-1]]
        left_stack = []
        right_stack = [rules[0][0]]

        print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)

        while right_stack[-1] != "OK":
            for row in slr_table:
                if row[0] == right_stack[-1]:
                    cell_num = 0
                    for cell_num in range(1, len(slr_table[0])):
                        if slr_table[0][cell_num] == input_stack[-1]:
                            if row[cell_num] == []:
                                print("НЕ ПОДХОДИТ, И ДА КРАШИМСЯ")
                                exit(0)
                            else:

                                if len(row[cell_num]) > 1:
                                    parsed_multiple = ", ".join(row[cell_num])
                                    left_stack.append(input_stack.pop())
                                    right_stack.append(parsed_multiple)
                                else:
                                    if len(ParseRule(row[cell_num][0])) == 2:

                                        for i in range(dict_of_rule_length[int(ParseRule(row[cell_num][0])[1])]):
                                            left_stack.pop()
                                            right_stack.pop()
                                        input_stack.append(dict_of_rule_letters[int(ParseRule(row[cell_num][0])[1])])
                                    else:
                                        left_stack.append(input_stack.pop())
                                        right_stack.append(row[cell_num][0])
                            cell_num = cell_num - 1
                            break
                    if cell_num + 1 == len(slr_table[0]):
                        print("НЕ ПОДХОДИТ, И ДА КРАШИМСЯ")
                        exit(0)
                    break
            print()
            print("разбор  INPUT-", input_stack, "  RIGHT-", right_stack, "  LEFT-", left_stack)

        if left_stack == [rules[0][0]]:
            print("ПОДХОДИТ")
        else:
            print("НЕ ПОДХОДИТ")

    def __init__(self, rules, show_slr: bool = False, show_first: bool = False, show_follow: bool = False):
        self.rules = rules

        self.first = self.First(rules)
        if show_first:
            print(self.first)

        self.follow = self.Follow(rules)
        if show_follow:
            print(self.follow)

        self.slr = self.SLR_Table(rules)
        if show_slr:
            pretty_2d_table(self.slr)
        self.CheckIfItSLR(self.slr)

    def run(self, input_text: str, show_parsing: bool = False):
        self.Runner(self.slr, input_text, self.rules)
