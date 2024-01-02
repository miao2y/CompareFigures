from typing import Dict, List
from pandas import DataFrame

from src.DatReader import DatReader
import re


class Profile:
    # 距离阈值
    threshold: float = 0.05

    # 允许的离群点数
    allow_err_count: int = 5

    # 小数点截断
    _decimal_points: Dict[str, int] = {}
    _decimal_point: int = 4

    # 相列名
    phase_column: str = 'phase_name'

    _reg_list: List[str] = ['T', 'G']

    _force_numeric_columns: List[str] = []

    reader: DatReader = None

    def __init__(self, phase_column: str, threshold: float, allow_err_count: int,
                 decimal_points: Dict[str, int] = {}, decimal_point: int = 4, force_numeric_columns: List[str] = [],
                 reg_list: List[str] = []):
        self.threshold = threshold
        self.allow_err_count = allow_err_count
        self._decimal_points = decimal_points
        self._reg_list = reg_list
        self.phase_column = phase_column
        self._decimal_point = decimal_point
        self._force_numeric_columns = force_numeric_columns

    @property
    def numeric_columns(self):
        if self._force_numeric_columns:
            return self._force_numeric_columns
        headers = self.reader.get_headers()
        select_headers = []
        for column_reg in self._reg_list:
            for header in headers:
                is_match = re.match(column_reg, header)
                if is_match:
                    select_headers.append(header)
        return list(set(select_headers))

    @property
    def decimal_points(self):
        if self._decimal_points:
            return self._decimal_points
        numeric_columns = self.numeric_columns
        # 每一列都是self.numeric_columns, 内容都是self._decimal_points
        return dict(zip(numeric_columns, [self._decimal_point] * len(numeric_columns)))
