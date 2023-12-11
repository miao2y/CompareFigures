import numpy as np
import pandas as pd


def read_data(f_name):
    # 打开文件并读取内容
    with open(f_name, 'r') as file:
        content = file.read()

    # 替换所有的制表符为逗号
    content = (content
               .replace('S\nK', 'S\tK')
               .replace('\t', ',')
               .replace('\n,,,,,,,,,,', '')
               )
    new_f_name = f_name + '.csv'
    # 将替换后的内容写入新文件
    with open(new_f_name, 'w') as file:
        file.write(content)
    return pd.read_csv(new_f_name)


if __name__ == '__main__':
    res = read_data("AlZn_1.dat")
    print(res.head())
