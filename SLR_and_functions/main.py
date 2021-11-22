from SLR1 import SLR
from runner import runner, Token2, FuncPart


def main():
    # try:
        f = {
            "add": FuncPart(lambda arg: arg[0] + arg[1], 2),
            "sub": FuncPart(lambda arg: arg[0] - arg[1], 2),
            "print": FuncPart(lambda arg: print(arg[0]), 1),
        }

        RULES = [
            ["S", ["A + B $"], [["add"], [], ["add"], []]],
            ["A", ["a - a"], [["sub"], [], ["sub"]]],
            ["B", ["b - b"], [["sub"], [], ["sub"]]],
        ]

        lexer_list = [
            Token2(2, "a"),
            Token2("-", "-"),
            Token2(1, "a"),

            Token2("+", "+"),

            Token2(5, "b"),
            Token2("-", "-"),
            Token2(2, "b"),
            Token2("$", "$"),
        ]

        slr = SLR(RULES, show_slr=False, show_first=False, show_follow=False)
        print("ПОБЕДА" if runner(slr, lexer_list, slr.rules, f, True) else "ДА ЕБ ТВОЮ МАТЬ")

    # except Exception as e:
    #     print(e.args)
    #     return "Не подходит"
    # else:
    #     return "Подходит"


if __name__ == '__main__':
    main()
