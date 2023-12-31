import json

import numpy as np

from src.CompareResult import CompareResult
from src.ResultDetail.CompareResultDetail import CompareResultDetail


class CompareResultEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CompareResult):
            return obj.__dict__
        if isinstance(obj, CompareResultDetail):
            return obj.__dict__
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
