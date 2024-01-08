# CompareFigures
比较两相图是否相同
## 安装依赖
```bash
pip install -r requirements.txt
```

## 使用方法

```python
from src.Comparator import Comparator
from pandarallel import pandarallel

from src.CompareResultEncoder import CompareResultEncoder
from src.Profile import Profile

pandarallel.initialize()

if __name__ == '__main__':
    profile = Profile(
        force_numeric_columns=['T', 'f(@Bcc#1)', 'f(@Bcc#2)'],
        phase_column='phase_name',
        threshold=0.05,
        allow_err_count=5,
        decimal_points={'T': 1, 'f(@Bcc#1)': 2, 'f(@Bcc#2)': 2}
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/Fe_1.dat", "./uploads/Fe_2.dat")
    print(CompareResultEncoder().encode(res))

```
或
```bash
python run.py
```
### 启用 API 模式访问
需要与 Compare-Figures-FE 搭配使用
```bash
flask --app api run --port 7777
```