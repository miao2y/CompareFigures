from typing import List
from pandas import DataFrame


class PhaseNameChecker:
    def __init__(self):
        pass

    @staticmethod
    def trim(phase_name: str):
        return phase_name.replace(' ', '')

    @staticmethod
    def sort(phase_name: str) -> str:
        factors = PhaseNameChecker.trim(phase_name).split('+')
        factors.sort()
        return '+'.join(factors)

    @staticmethod
    def sort_df(data: DataFrame, phase_name_col: str) -> DataFrame:
        print(data.head())
        data[[phase_name_col]] = data[[phase_name_col]].map(lambda n: PhaseNameChecker.sort(n))
        print(data.head())
        return data

    @staticmethod
    def remove_duplicate(phase_names: List[str]):
        return list(set(phase_names))
