from Comparator import Comparator
from pandarallel import pandarallel
import json

from CompareResultEncoder import CompareResultEncoder

pandarallel.initialize()

if __name__ == '__main__':
    comparator = Comparator(numeric_columns=['T', 'f(@Bcc#1)', 'f(@Bcc#2)'], phase_column='phase_name')
    comparator.threshold = 0.05
    comparator.allow_err_count = 5
    comparator.decimal_points = {'T': 1, 'f(@Bcc#1)': 2, 'f(@Bcc#2)': 2}
    res = comparator.check("./uploads/Fe_1.dat", "./uploads/Fe_2.dat")
    print(CompareResultEncoder().encode(res))
