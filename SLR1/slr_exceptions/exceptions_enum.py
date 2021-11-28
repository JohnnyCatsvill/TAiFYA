from enum import Enum


class SLRErrId(Enum):
    DOUBLE_FOLD_IN_ONE_CELL = "got an cell ins slr table where are multiple folds leads to uncertain behaviour"
    MOVE_AND_FOLD_IN_ONE_CELL = "got an cell with folds and moves in slr table that leads to uncertain behaviour"

    # runner exceptions
    NONTERMINAL_IN_INPUT_STACK = "got an nonterminal in input stack, think it should be an error"
    EMPTY_INPUT_STACK = "got an empty input stack when we try to get a value from it"
    NON_GRAMMAR_SYMBOL_TOKEN = "got a token that we cannot find in our resulting slr table"
    NON_GRAMMAR_SYMBOL_WORD = "got a move that we cannot find in our resulting slr tale"
    NOWHERE_TO_MOVE_NEXT = "no further moves in our slr table with current given input"

