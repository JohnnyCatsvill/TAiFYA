from copy import deepcopy
from enum import Enum
from constants.constants_slr import *


class WordType(Enum):
    NONTERM = 0
    TERM = 1
    FOLD = 2
    END = 3
    EMPTY = 4
    OK_WORD = 5
    STARTER = 6


class Word:
    def __init__(self, word_type: WordType, word: str, row: int = 0, column: int = 0, e_fold: int = 0,
                 action: list[list[str]] = None):
        self.type: WordType = word_type
        self.str: str = word
        self.row: int = row
        self.col: int = column
        self.e_fold: int = e_fold
        self.action: list[list[str]] = action

    def __hash__(self):
        return hash((self.str, self.type, self.row, self.col, self.e_fold, self.action))

    def __repr__(self):
        row = ' ' + str(self.row) if self.row > 0 else ''
        column = ' ' + str(self.col) if self.col > 0 else ''
        e_fold = ' ' + str(self.e_fold) if self.e_fold > 0 else ''
        return f"{self.str}{row}{column}{e_fold}"

    def __eq__(self, other):
        return all([
            self.type == other.type,
            self.str == other.str,
            self.row == other.row,
            self.col == other.col,
            self.action == other.action,
        ])

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


def parse_all_rules(rules: list[list[str, list[str], list[list[str]]]]) -> list[Rule]:

    def parse_rule(rule: str, divider=" "):
        rule_list: list[str] = rule.split(divider)
        return rule_list

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

    set_of_nonterminals = set([rule_pack[0] for rule_pack in rules])
    set_of_control_symbols = {EMPTY_SYMBOL, END_SYMBOL}
    set_of_terminals = set([letter for rule_pack in rules for letter in parse_rule(rule_pack[1][0]) if
                            letter not in set_of_nonterminals and letter not in set_of_control_symbols])

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


class FuncPart:
    def __init__(self, function: callable, arg_length: int):
        self.f = function
        self.arg_length = arg_length
