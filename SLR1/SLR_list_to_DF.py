import pandas as pd
from interfaces.slr_interfaces import Word


class DF:

    def __init__(self, table: list[list[list[Word]]]):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        self.df = pd.DataFrame([i[1:] for i in table], columns=table[0][1:], index=[str(i[0]) for i in table])

    def get(self, row: list[Word], col: str) -> list[Word]:
        return self.df.loc[str(row)][col]

    def __repr__(self):
        return str(self.df)

