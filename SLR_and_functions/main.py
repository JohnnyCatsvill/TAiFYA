from SLR1 import SLR
from interfaces.slr_interfaces import FuncPart
from runner import runner


def main():
    try:
        f = {
            "add": FuncPart(lambda *args: args[0] + args[1], 2),
            "sub": FuncPart(lambda *args: args[0] - args[1], 2),
            "print": FuncPart(lambda *args: print(args[0]), 1),
        }

        RULES = [
            ["S", ["A + B $"], [f["add"], [], f["add"], []]],
            ["A", ["a - a"], [f["sub"], [], f["sub"]]],
            ["B", ["b - b"], [f["sub"], [], f["sub"]]],
        ]

        slr = SLR(RULES, show_slr=False, show_first=False, show_follow=False)
        runner(slr, lexer_list, slr.rules)

    except Exception as e:
        print(e.args)
        return "Не подходит"
    else:
        return "Подходит"


if __name__ == '__main__':
    main()
