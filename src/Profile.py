from typing import Dict, List


class Profile:
    # 距离阈值
    threshold: float = 0.05

    # 允许的离群点数
    allow_err_count: int = 5

    # 小数点截断
    decimal_points: Dict[str, int] = {}

    # 数值列名
    numeric_columns: List[str] = ['T', 'G']

    # 相列名
    phase_column: str = 'phase_name'

    def __init__(self, numeric_columns: List[str], phase_column: str, threshold: float, allow_err_count: int,
                 decimal_points: Dict[str, int]):
        self.threshold = threshold
        self.allow_err_count = allow_err_count
        self.decimal_points = decimal_points
        self.numeric_columns = numeric_columns
        self.phase_column = phase_column


