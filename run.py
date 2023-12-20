import numpy as np
import pandas as pd
import read_data
from utils import check_phase
from scipy.spatial.distance import cdist


def round(data, decimal_points):
    if 'T' in decimal_points and decimal_points['T'] is not None:
        data['T'] = data['T'].round(decimal_points['T'])
    if 'x(Al)' in decimal_points and decimal_points['x(Al)'] is not None:
        data['x(Al)'] = data['x(Al)'].round(decimal_points['x(Al)'])
    if 'x(Zn)' in decimal_points and decimal_points['x(Zn)'] is not None:
        data['x(Zn)'] = data['x(Zn)'].round(decimal_points['x(Zn)'])
    return data


def check(fname1, fname2, threshold, allow_err_count, decimal_points={}):
    print(decimal_points)
    # 读取数据
    data1 = read_data.read_data(fname1)
    data2 = read_data.read_data(fname2)

    data1 = data1[['T', 'x(Al)', 'x(Zn)', 'phase_name']]
    data2 = data2[['T', 'x(Al)', 'x(Zn)', 'phase_name']]

    data1 = round(data1, decimal_points)
    data2 = round(data2, decimal_points)


    numeric_columns = ['T', 'x(Al)', 'x(Zn)']

    # 检查相类型是否相同
    if not check_phase(data1, data2):
        return False, "Phase not same"

    phase_names = data1['phase_name'].unique().tolist()

    # 遍历每种相图
    for phase_name in phase_names:
        a_old = data1[data1['phase_name'] == phase_name]
        b_old = data2[data2['phase_name'] == phase_name]
        # 合并两个对象
        merged_df = pd.concat([a_old, b_old])

        # 计算合并后对象的均值
        mean_values = merged_df[numeric_columns].mean()
        std_values = merged_df[numeric_columns].std()
        max_values = merged_df[numeric_columns].max()
        min_values = merged_df[numeric_columns].min()

        a = (a_old[numeric_columns] - min_values) / (max_values - min_values)
        b = (b_old[numeric_columns] - min_values) / (max_values - min_values)

        # print(a, b)
        distance = cdist(a[numeric_columns], b[numeric_columns])

        new_data = np.min(distance, axis=1)
        # print(phase_name, new_data)

        greater_count = np.sum(new_data > threshold)
        if greater_count > allow_err_count:
            indices = np.where(new_data > threshold)[0]
            elements = new_data[indices]
            print("A to B Test Failed!")
            print(a_old.to_numpy()[indices])
            print(indices, elements)
            return False, "Phase:" + phase_name + " not same"
        else:
            print(phase_name, "Passed, err_count: ", greater_count)
            print("===============")

        # print(a, b)
        distance = cdist(b[numeric_columns], a[numeric_columns])

        new_data = np.min(distance, axis=1)
        # print(phase_name, new_data)

        greater_count = np.sum(new_data > threshold)
        if greater_count > allow_err_count:
            indices = np.where(new_data > threshold)[0]
            elements = new_data[indices]
            print("B to A Test Failed!")
            print(b_old.to_numpy()[indices])
            print(indices, elements)
            return False, "Phase:" + phase_name + " not same"
        else:
            print(phase_name, "Passed, err_count: ", greater_count)
            print("===============")

        # if phase_name == 'FCC_A1+HCP_A3+FCC_A1':
        #     plt.scatter(a['x(Al)'], a['x(Zn)'])
        #     plt.show()
        #     plt.scatter(b['x(Al)'], b['x(Zn)'], )
        #     plt.show()

        # print(a, b)
        # err_count = 0
        # print("phase_name:", phase_name)
        # sum_distance = 0
        #
        # # a -> b
        # for index, point in enumerate(a.values):
        #     distance = np.linalg.norm(point - b.values, axis=1)
        #     # print("distance:", index, np.min(distance))
        #     if coord_threshold < np.min(distance):
        #         print(np.min(distance))
        #         sum_distance = sum_distance + np.min(distance)
        #         err_count = err_count + 1
        #
        # if err_count != 0:
        #     average_distance = sum_distance / err_count
        #     if average_distance > average_threshold:
        #         print(phase_name, "a->b超过阈值")
        #         print("average_distance:", average_distance)
        #         exit(1)
        #
        # err_count = 0
        # sum_distance = 0
        # # b -> a
        # for index, point in enumerate(b.values):
        #     distance = np.linalg.norm(point - a.values, axis=1)
        #     # print("distance:", index, np.min(distance))
        #     if coord_threshold < np.min(distance):
        #         print(point)
        #         print(distance)
        #         print(np.min(distance))
        #         sum_distance = sum_distance + np.min(distance)
        #         err_count = err_count + 1
        #         # print(point)
        # # print(data1[index:index + 1])
        # # print("超过阈值")
        # # count = count + 1
        # # exit(1)
        # # print("count:", count)
        # # if count > 0:
        # #     print("超过阈值")
        # #     exit(1)
        # if err_count != 0:
        #     average_distance = sum_distance / err_count
        #     if average_distance > average_threshold:
        #         print(phase_name, "b->a超过阈值")
        #         print("average_distance:", average_distance)
        #         exit(1)

    print("Same Figure")
    return True, "Same Figure"
