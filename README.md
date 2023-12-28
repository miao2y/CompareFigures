# CompareFigures
比较两相图是否相同

## 使用方法
```python
from Comparator import Comparator
from pandarallel import pandarallel
import json

from CompareResultEncoder import CompareResultEncoder
from Profile import Profile

pandarallel.initialize()

if __name__ == '__main__':
    profile = Profile(
        numeric_columns=['T', 'f(@Bcc#1)', 'f(@Bcc#2)'],
        phase_column='phase_name',
        threshold=0.05,
        allow_err_count=5,
        decimal_points={'T': 1, 'f(@Bcc#1)': 2, 'f(@Bcc#2)': 2}
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/Fe_1.dat", "./uploads/Fe_2.dat")
    print(CompareResultEncoder().encode(res))
```
