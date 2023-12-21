from ResultDetail.CompareResultDetail import CompareResultDetail
from typing import List, Set


class PhaseNameCompareResultDetail(CompareResultDetail):
    # a 与 b 各自缺少的相名
    a_missing_phase_names: List[str] = []
    b_missing_phase_names: List[str] = []

    # 比较对象 a 与 b 各自的相名称集合
    a_phase_names_set: Set[str] = None
    b_phase_names_set: Set[str] = None
