from typing import List, Set

from ResultDetail.CompareResultDetail import CompareResultDetail


class DistanceCompareResultDetail(CompareResultDetail):
    phase_name: str = None

    # a 错误节点的索引
    a_wrong_indexes: List[int] = []

    # b 错误节点的索引
    b_wrong_indexes: List[int] = []
