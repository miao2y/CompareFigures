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
        decimal_point=3
    )
    comparator = Comparator(profile=profile)
    res = comparator.check("./uploads/AlZn_1.dat", "./uploads/AlZn_1.dat")
    print(CompareResultEncoder().encode(res))
