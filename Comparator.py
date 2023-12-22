import numpy as np
import pandas as pd
from typing import List
from scipy.spatial.distance import cdist

from CompareResult import CompareResult
from CompareResultFactory import CompareResultFactory
from DatReader import DatReader
from PhaseNameChecker import PhaseNameChecker
from Profile import Profile
from ResultDetail.PhaseNameCompareResultDetail import PhaseNameCompareResultDetail
from utils import round_with_config


class Comparator:
    profile: Profile = None

    def __init__(self, profile):
        self.profile = profile

    # 检查两个图的相是否全部相同
    def check_phase(self, a, b) -> CompareResult:
        a_phases = PhaseNameChecker.remove_duplicate(
            list(map(lambda n: PhaseNameChecker.sort(n), a[self.profile.phase_column].unique().tolist())))
        b_phases = PhaseNameChecker.remove_duplicate(
            list(map(lambda n: PhaseNameChecker.sort(n), b[self.profile.phase_column].unique().tolist())))
        result_detail = PhaseNameCompareResultDetail()
        result_detail.result = set(a_phases) == set(b_phases)
        result_detail.message = "两相图相位不同"
        result_detail.a_phase_names_set = a_phases
        result_detail.b_phase_names_set = b_phases
        result_detail.a_missing_phase_names = list(set(b_phases) - set(a_phases))
        result_detail.b_missing_phase_names = list(set(a_phases) - set(b_phases))

        result = CompareResult("相比较")
        result.detail = result_detail
        result.result = result_detail.result
        return result

    # 由于两个相之间+的顺序可能不同
    # 所以需要对两个相进行排序（字典序）
    def prepossess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        data = data[self.profile.numeric_columns + [self.profile.phase_column]]
        data = data.fillna(0)
        data = round_with_config(data, self.profile.decimal_points)
        data = PhaseNameChecker.sort_df(data, self.profile.phase_column)
        return data

    def check(self, file_name1: str, file_name2: str) -> List[CompareResult]:

        result_list: List[CompareResult] = []

        # 读取数据
        data1 = DatReader(file_name1).data
        data2 = DatReader(file_name2).data

        data1 = self.prepossess_data(data1)
        data2 = self.prepossess_data(data2)

        numeric_columns = self.profile.numeric_columns

        phase_result = self.check_phase(data1, data2)
        result_list.append(phase_result)

        phase_names = phase_result.detail.a_phase_names_set + phase_result.detail.b_phase_names_set

        # 遍历每种相图
        for phase_name in list(phase_names):
            print("=============")
            print("phase_name:", phase_name)
            # print("data1.head()", data1.head())
            # print("data2.head()", data2.head())
            a_old = data1[data1[self.profile.phase_column] == phase_name]
            b_old = data2[data2[self.profile.phase_column] == phase_name]
            if a_old.shape[0] == 0:
                result_list.append(CompareResultFactory.create_distance_result(
                    success=False,
                    phase_name=phase_name,
                    message="由于 A 中相图" + phase_name + "不存在，无法进行距离比较",
                    b_wrong_indexes=b_old.index.tolist().copy(),
                ))
                continue
            if b_old.shape[0] == 0:
                result_list.append(CompareResultFactory.create_distance_result(
                    success=False,
                    phase_name=phase_name,
                    message="由于 B 中相图" + phase_name + "不存在，无法进行距离比较",
                    a_wrong_indexes=a_old.index.tolist().copy(),
                ))
                continue

            # 合并两个对象
            merged_df = pd.concat([a_old, b_old])

            # 计算合并后对象的均值
            mean_values = merged_df[numeric_columns].mean()
            std_values = merged_df[numeric_columns].std()
            max_values = merged_df[numeric_columns].max()
            min_values = merged_df[numeric_columns].min()

            a = ((a_old[numeric_columns] - min_values) / (max_values - min_values)).fillna(0)
            b = ((b_old[numeric_columns] - min_values) / (max_values - min_values)).fillna(0)

            # print(a, b)
            distance = cdist(a[numeric_columns], b[numeric_columns])
            a_min_distances = np.min(distance, axis=1)
            # print(phase_name, new_data)

            greater_count = np.sum(a_min_distances > self.profile.threshold)
            if greater_count > self.profile.allow_err_count:
                indices = np.where(a_min_distances > self.profile.threshold)[0]
                elements = a_min_distances[indices]

                result_list.append(CompareResultFactory.create_distance_result(
                    success=False,
                    phase_name=phase_name,
                    message="A -> B:" + phase_name + "距离校验失败，超出预设点数：" + str(
                        greater_count) + '/' + str(
                        self.profile.allow_err_count),
                    a_wrong_indexes=indices.tolist().copy(),
                ))
                continue

            # print(a, b)
            distance = cdist(b[numeric_columns], a[numeric_columns])

            b_greater_count = np.min(distance, axis=1)
            # print(phase_name, new_data)

            greater_count = np.sum(b_greater_count > self.profile.threshold)
            if greater_count > self.profile.allow_err_count:
                indices = np.where(b_greater_count > self.profile.threshold)[0]
                elements = b_greater_count[indices]

                result_list.append(CompareResultFactory.create_distance_result(
                    success=False,
                    phase_name=phase_name,
                    message="B -> A:" + phase_name + "距离校验失败，超出预设点数：" + str(
                        greater_count) + '/' + str(
                        self.profile.allow_err_count),
                    b_wrong_indexes=indices.tolist().copy(),
                ))
                continue

            result_list.append(CompareResultFactory.create_distance_result(
                success=True,
                phase_name=phase_name,
                message="距离校验成功，离群点数：" + str(greater_count) + '/' + str(self.profile.allow_err_count),
            ))

        return result_list
