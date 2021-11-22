from constants_lex import *


class Token:
    def __init__(self, word: str, token: str, row: int, column: int):
        self.word: str = word
        self.token: str = token
        self.row: int = row
        self.column: int = column

    def __repr__(self):
        word = self.word.ljust(PRINT_WORD_LENGTH)  # align data
        row = str(self.row).ljust(PRINT_WORD_ROW)
        col = str(self.column).ljust(PRINT_WORD_COLUMN)
        return f"row: {row} col: {col}  word: {word}  token: {self.token}"

    def __eq__(self, other):
        return self.token == other.token and self.word == other.word and self.row == other.row and self.column == other.row


class Lexer:

    def __init__(self, program_text, log_states: bool = False, show_spaces: bool = False, show_lex: bool = False):
        self.__text = program_text + "\n"
        self.list: list[Token] = []
        self.__run(log_states, show_spaces)
        if show_lex:
            self.show()

    def __run(self, show_states=False, show_spaces=False):

        def state_error(symbol, word, row, column):
            if symbol in STOP_POINTS:
                self.list.append(Token(word[0], ERROR_NAME, row, column))
                word[0] = ""
                raise Exception("Lexer's unexpected symbol", f"{self.list[-1]}")
                # return state_start(symbol, word, row, column)
            else:
                return state_error

        def state_unary_stop_symbol(symbol, word, row, column):
            if dictionary.get(word[0], False):
                if word[0] == " " and not show_spaces:
                    pass
                else:
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
            word[0] = ""
            return state_start(symbol, word, row, column)

        def state_undefined_stop_symbol(symbol, word, row, column):
            if symbol == "=":
                return state_dual_stop_symbol
            else:
                if dictionary.get(word[0], False):
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_dual_stop_symbol(symbol, word, row, column):
            if dictionary.get(word[0], False):
                self.list.append(Token(word[0], dictionary[word[0]], row, column))
            word[0] = ""
            return state_start(symbol, word, row, column)

        def state_slash_symbol(symbol, word, row, column):
            if symbol == "/":
                return state_comment
            elif symbol == "*":
                return state_multi_comment
            else:
                if dictionary.get(word[0], False):
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_comment(symbol, word, row, column):
            if symbol == "\n":
                self.list.append(Token(word[0], COMMENT_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)
            else:
                return state_comment

        def state_multi_comment(symbol, word, row, column):
            if symbol == "*":
                return state_multi_comment_exit
            else:
                return state_multi_comment

        def state_multi_comment_exit(symbol, word, row, column):
            if symbol == "/":
                self.list.append(Token(word[0], COMMENT_NAME, row, column))
                word[0] = ""
                return state_start
            else:
                return state_multi_comment

        def state_identifier(symbol, word, row, column):
            if symbol in LETTERS + NUMBERS + "_":
                return state_identifier
            else:
                if dictionary.get(word[0], False):
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
                else:
                    self.list.append(Token(word[0], ID_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_hex_number(symbol, word, row, column):
            if symbol in HEX:
                return state_hex_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], HEX_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_bin_number(symbol, word, row, column):
            if symbol in BIN:
                return state_bin_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], BIN_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_oct_number(symbol, word, row, column):
            if symbol in OCT:
                return state_oct_number
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], OCT_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_float
            elif symbol in "eE":
                return state_float_exponent
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], FLOAT_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_undefined_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_float
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column)
            else:
                return state_error(symbol, word, row, column)

        def state_float_exponent(symbol, word, row, column):
            if symbol in "+-":
                return state_float_exponent_sign
            else:
                return state_error

        def state_float_exponent_sign(symbol, word, row, column):
            if symbol in "123456789":
                return state_float_exponent_numbers
            elif symbol in "0":
                return state_float_exponent_zero
            else:
                return state_error

        def state_float_exponent_numbers(symbol, word, row, column):
            if symbol in "0123456789":
                return state_float_exponent_numbers
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], FLOAT_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_float_exponent_zero(symbol, word, row, column):
            if symbol in LETTERS + NUMBERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], FLOAT_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_any_number(symbol, word, row, column):
            if symbol == HEX_START:
                return state_hex_number
            elif symbol == BIN_START:
                return state_bin_number
            elif symbol in OCT:
                return state_oct_number
            elif symbol == POINT:
                return state_float
            elif symbol in NUMBERS + LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], DEC_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_int_or_float(symbol, word, row, column):
            if symbol in NUMBERS:
                return state_int_or_float
            elif symbol == POINT:
                return state_float
            elif symbol in LETTERS:
                return state_error(symbol, word, row, column)
            else:
                self.list.append(Token(word[0], DEC_NAME, row, column))
                word[0] = ""
                return state_start(symbol, word, row, column)

        def state_and_not_sure(symbol, word, row, column):
            if symbol == "&":
                return state_and
            else:
                if dictionary.get(word[0], False):
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
                word[0] = ""
                return state_error(symbol, word, row, column)

        def state_and(symbol, word, row, column):
            if dictionary.get(word[0], False):
                self.list.append(Token(word[0], dictionary[word[0]], row, column))
            word[0] = ""
            return state_start(symbol, word, row, column)

        def state_or_not_sure(symbol, word, row, column):
            if symbol == "|":
                return state_or
            else:
                if dictionary.get(word[0], False):
                    self.list.append(Token(word[0], dictionary[word[0]], row, column))
                word[0] = ""
                return state_error(symbol, word, row, column)

        def state_or(symbol, word, row, column):
            if dictionary.get(word[0], False):
                self.list.append(Token(word[0], dictionary[word[0]], row, column))
            word[0] = ""
            return state_start(symbol, word, row, column)

        def state_start(symbol, word, row, column):
            if symbol in LETTERS:
                return state_identifier
            elif symbol == "/":
                return state_slash_symbol
            elif symbol in "<>!=":
                return state_undefined_stop_symbol
            elif symbol in "(){}[];+-*%, \n":
                return state_unary_stop_symbol
            elif symbol in "123456789":
                return state_int_or_float
            elif symbol == "0":
                return state_any_number
            elif symbol == ".":
                return state_undefined_float
            elif symbol == "&":
                return state_and_not_sure
            elif symbol == "|":
                return state_or_not_sure
            else:
                return state_error

        def actual_run(first_state=state_start):

            state = first_state

            last_symbol = ""
            word = [""]  # passing an argument by reference, not some shitty stuff
            row = 1
            column = 0
            for i in self.__text:
                state = state(i, word, row, column)

                if show_states:
                    print(state, i)

                if last_symbol == "\n":
                    row += 1
                    column = 1
                else:
                    column += 1

                word[0] += i
                last_symbol = i

        def check_for_type_length_limit():
            for elem in self.list:
                if elem.token in MAX_LENGTH_OF_TYPES:
                    if len(elem.word) > MAX_LENGTH_OF_TYPES[elem.token]:
                        elem.token = ERROR_NAME

        actual_run()
        check_for_type_length_limit()

    def show(self):
        for i in self.list:
            word = i.word.replace("\n", "\\n")  # to not see line brakes
            word = word.ljust(PRINT_WORD_LENGTH)  # align data
            row = str(i.row).ljust(PRINT_WORD_ROW)
            col = str(i.column).ljust(PRINT_WORD_COLUMN)
            print(f"row: {row} col: {col}  word: {word}  token: {i.token}")
