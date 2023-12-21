from typing import List

from CompareResult import CompareResult
from ResultDetail.DistanceCompareResultDetail import DistanceCompareResultDetail


class CompareResultFactory:
    @staticmethod
    def create_distance_result(success, phase_name, message, a_wrong_indexes: List[int] = None,
                               b_wrong_indexes: List[int] = None):
        # 处理默认值
        if a_wrong_indexes is None:
            a_wrong_indexes = []
        if b_wrong_indexes is None:
            b_wrong_indexes = []

        result_detail = DistanceCompareResultDetail()
        result_detail.result = success
        result_detail.phase_name = phase_name
        result_detail.message = message
        result_detail.a_wrong_indexes = a_wrong_indexes.copy()
        result_detail.b_wrong_indexes = b_wrong_indexes.copy()
        result = CompareResult("距离比较")
        result.detail = result_detail
        result.result = success
        return result