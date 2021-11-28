from constants.constants_slr import RUNNER_OK
from lexer import Lexer
from lexer import Token
from SLR1 import SLR
from lexer_exceptions.lexer_exception import LexerException
from runner import runner
from rules import RULES
from slr_exceptions.slr_exception import SLRException, SLRRunnerException


def main():
    try:
        text = open("program.txt", "r").read()

        lex = Lexer(text, show_lex=False, log_states=False, show_spaces=False)
        slr = SLR(RULES, show_slr=False, show_first=False, show_follow=False)

        lexer_list = [i for i in lex.list if i.token not in ["new_line", "Comment"]]
        lexer_list.append(Token("true_end", "$", -1, -1))

        runner(slr, lexer_list, slr.rules)

    except (LexerException, SLRException, SLRRunnerException) as e:
        print(e)
        return e
    return RUNNER_OK


if __name__ == "__main__":
    print(main())
