import numpy as np

def ga_normed_characts(characts):
    return (characts - characts.min(0)) / characts.ptp(0)

# TM
def calculate_total_mean(id_to_characts):
    values = np.array(list(id_to_characts.values()))

    return np.mean(values, axis = 0)

# IM
def calculate_individual_mean(id_to_characts, groups):
    individual_all_characts = np.array([np.array([id_to_characts[id] for id in group]) for group in groups])

    return np.mean(individual_all_characts, axis = 1)

def calculate_square_difference(total_mean, individual_mean):
    return np.sum(np.square(individual_mean - total_mean))
