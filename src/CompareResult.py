from typing import TypeVar, Generic, List
import json

T = TypeVar('T')


class CompareResult(Generic[T]):
    # 比较项目名
    item_name = None
    # 比较结果
    result = False
    # 错误细节
    detail: T = None

    def __init__(self, item_name):
        self.item_name = item_name

    def to_json(self):
        return json.dumps(self, default=lambda obj: obj.__dict__)
