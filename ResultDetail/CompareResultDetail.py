from abc import ABC


class CompareResultDetail(ABC):
    # 判断结果
    result = False

    message: str = ""
