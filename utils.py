def check_phase(a, b):
    return set(a['phase_name'].unique().tolist()) == set(b['phase_name'].unique().tolist())
