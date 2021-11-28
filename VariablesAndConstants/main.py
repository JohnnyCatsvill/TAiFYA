from VarsAndConst import *


def main():
    try:
        data = VarsAndConst()
        print(data)
        print("////////////////////////////////////")

        data.add_block()
        print(data)
        print("////////////////////////////////////")

        data.add_record("a", "int", 3)
        data.add_record("b", "int", 4)
        data.add_record("c", "int", 5)
        # data.add_record("a", "str", "asd")  # исправить проверить

        print(data)
        print("////////////////////////////////////")

        data.add_block()
        data.add_record("a", "str", "buba")
        print(data)
        print("////////////////////////////////////")

        print(data.get_record("a"))
        print(data.get_record("b"))
        print("////////////////////////////////////")

        data.update_record("a", "str", "ububu")
        print(data)
        print("////////////////////////////////////")

        data.remove_block()
        print(data)
        print("////////////////////////////////////")

        data.remove_block()
        print(data)
        print("////////////////////////////////////")

        data.remove_block()  # if it were empty
        print(data)
        print("////////////////////////////////////")
    except VACException as e:
        print(e)
    return "OK"


if __name__ == '__main__':
    main()
