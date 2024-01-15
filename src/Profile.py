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

    # 手动指定数值列名
    _force_column_names: List[str] = []

    # 手动指定数值列索引
    _force_column_indexes: List[int] = []

    # 所有列名
    _all_column_names: List[str] = []

    def __init__(self, phase_column: str, threshold: float, allow_err_count: int,
                 decimal_points: Dict[str, int] = {}, decimal_point: int = 4,
                 force_column_names: List[str] = [],
                 force_column_indexes: List[int] = [],
                 reg_list: List[str] = []):
        self.threshold = threshold
        self.allow_err_count = allow_err_count
        self._decimal_points = decimal_points
        self._reg_list = reg_list
        self.phase_column = phase_column
        self._decimal_point = decimal_point
        self._force_column_names = force_column_names
        self._force_column_indexes = force_column_indexes

    @property
    def numeric_columns(self):
        headers = self._all_column_names
        select_headers = []

        # 如果设置过强制数值列，就用强制数值列匹配
        if self._force_column_names:
            # 可以直接返回
            return self._force_column_names

        # 如果设置过列索引，就用列索引匹配
        if len(self._force_column_indexes) > 0:
            for index in self._force_column_indexes:
                select_headers.append(headers[index])

        # 如果设置过正则表达式，就用正则表达式匹配
        if len(self._reg_list) > 0:
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

    def set_all_column_names(self, columns: List[str]):
        self._all_column_names = columns
