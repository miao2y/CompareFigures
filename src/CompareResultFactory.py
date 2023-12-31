from typing import List

import pandas as pd

from src.CompareResult import CompareResult
from src.ResultDetail.DistanceCompareResultDetail import DistanceCompareResultDetail
from src.ResultDetail.FileNotMatchResultDetail import FileNotMatchResultDetail


class CompareResultFactory:
    @staticmethod
    def create_distance_result(success: bool, phase_name: str, message: str,
                               a_wrong_indexes: List[int] = None,
                               b_wrong_indexes: List[int] = None,
                               a_wrong_rows: List[pd.DataFrame] = None,
                               b_wrong_rows: List[pd.DataFrame] = None
                               ):
        # 处理默认值
        if a_wrong_indexes is None:
            a_wrong_indexes = []
        if b_wrong_indexes is None:
            b_wrong_indexes = []

        result_detail = DistanceCompareResultDetail()
        result_detail.result = success
        result_detail.phase_name = phase_name
        result_detail.message = message
        result_detail.a_wrong_indexes = a_wrong_indexes
        result_detail.b_wrong_indexes = b_wrong_indexes
        result_detail.a_wrong_rows = a_wrong_rows
        result_detail.b_wrong_rows = b_wrong_rows
        result = CompareResult("距离比较")
        result.detail = result_detail
        result.result = success
        return result

    @staticmethod
    def create_default_result(success: bool, message: str):
        result_detail = FileNotMatchResultDetail()
        result_detail.result = success
        result_detail.message = message
        result = CompareResult("文件检验")
        result.detail = result_detail
        result.result = success
        return result
