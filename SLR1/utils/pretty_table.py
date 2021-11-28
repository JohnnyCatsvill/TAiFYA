from tabulate import tabulate  # украшательства
import copy


def pretty_2d_table(list_2d, symbols_to_delete=""):
    to_print = copy.deepcopy(list_2d)
    for i in range(len(to_print)):
        for j in range(len(to_print[i])):
            if not to_print[i][j]:
                to_print[i][j] = ""
            else:
                cell = str(to_print[i][j])
                for k in symbols_to_delete:
                    cell = cell.replace(k, "")
                to_print[i][j] = cell

    print(tabulate(to_print, stralign="center", tablefmt="fancy_grid"))  # шедевр
    print()
