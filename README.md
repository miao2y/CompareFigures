# CompareFigures

比较两相图是否相同

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法
> 以下三种指定列的方式，同时设置只会有一个生效。
> 
> 优先级为：force_column_names > force_column_indexes > reg_list


### 手动指定列名

```python
from src.Comparator import Comparator
from pandarallel import pandarallel

from src.CompareResultEncoder import CompareResultEncoder
from src.Profile import Profile

pandarallel.initialize()

if __name__ == '__main__':
    profile = Profile(
        force_column_names=['T', 'f(@Bcc#1)', 'f(@Bcc#2)'],
        phase_column='phase_name',
        threshold=0.05,
        allow_err_count=5,
        decimal_points={'T': 1, 'f(@Bcc#1)': 2, 'f(@Bcc#2)': 2}
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/Fe_1.dat", "./uploads/Fe_2.dat")
    print(CompareResultEncoder().encode(res))

```

### 手动指定列索引

```python

from src.Comparator import Comparator
from pandarallel import pandarallel

from src.CompareResultEncoder import CompareResultEncoder
from src.Profile import Profile

pandarallel.initialize()

if __name__ == '__main__':
    profile = Profile(
        force_column_indexes=[0, 1],  # 选取第 0 列和第 1 列
        phase_column='phase_name',
        threshold=0.05,
        allow_err_count=5,
        decimal_point=3  # 满足条件的列会保留 3 位小数
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/AlZn_1.dat", "./uploads/AlZn_1.dat")
    print(CompareResultEncoder().encode(res))

```

### 使用正则表达式

```python

from src.Comparator import Comparator
from pandarallel import pandarallel

from src.CompareResultEncoder import CompareResultEncoder
from src.Profile import Profile

pandarallel.initialize()

if __name__ == '__main__':
    profile = Profile(
        reg_list=['^T$', '^[f|F]\(.*\)$'],  # 列名满足 T 和 f(*) 会被自动选中，详见正则表达式用法
        phase_column='phase_name',
        threshold=0.05,
        allow_err_count=5,
        decimal_point=3  # 满足条件的列会保留 3 位小数
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/AlZn_1.dat", "./uploads/AlZn_1.dat")
    print(CompareResultEncoder().encode(res))

```

## 运行样例

```bash
python run.py
```

### 启用 API 模式访问

需要与 Compare-Figures-FE 搭配使用

```bash
flask --app api  run --host=0.0.0.0  --port 7777
```