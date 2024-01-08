from typing import List

import pandas as pd
import re


class DatReader:
    file_name: str = None
    data: pd.DataFrame = None

    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.read(file_name)

    def read(self, file_name: str) -> pd.DataFrame:
        # 打开文件并读取内容
        with open(file_name, 'r') as file:
            content = file.read()

        content = re.sub(r'\n[A-Z]\t.*', '', content)
        # 替换所有的制表符为逗号
        content = (content
                   # .replace('\nK\t', '\tK\t')
                   # .replace('\nC\t', '\tC\t')
                   .replace('\t', ',')
                   )
        # content = re.sub(r'\nK,.*', r'', content)
        content = re.sub(r'\n,+\n', r'\n', content)

        new_f_name = file_name + '.csv'
        print(new_f_name)
        # 将替换后的内容写入新文件
        with open(new_f_name, 'w') as file:
            file.write(content)

        return pd.read_csv(new_f_name)

    def get_headers(self) -> List[str]:
        return self.data.columns.tolist()
