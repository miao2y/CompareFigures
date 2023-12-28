from typing import Dict


def check_phase(a, b):
    return set(a['phase_name'].unique().tolist()) == set(b['phase_name'].unique().tolist())


def round_with_config(data, decimal_points: Dict[str, int]):
    for column in decimal_points:
        if column in decimal_points and decimal_points[column] is not None:
            data[column] = data[column].round(decimal_points[column])
    return data
