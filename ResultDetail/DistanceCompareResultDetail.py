from typing import List, Set
import pandas as pd
from ResultDetail.CompareResultDetail import CompareResultDetail


class DistanceCompareResultDetail(CompareResultDetail):
    phase_name: str = None

    # a 错误节点的索引
    a_wrong_indexes: List[int] = []

    # b 错误节点的索引
    b_wrong_indexes: List[int] = []

    a_wrong_rows: List[pd.DataFrame] = []

    b_wrong_rows: List[pd.DataFrame] = []
