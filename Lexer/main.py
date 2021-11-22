from lexer import *


def main():
    program_text = open("program_text.txt", "r").read()
    lex = Lexer(program_text, show_lex=True)


if __name__ == '__main__':
    main()
