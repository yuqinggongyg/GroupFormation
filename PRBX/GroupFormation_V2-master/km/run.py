import numpy as np
from scipy import stats
import random
from math import sqrt

def run(id_to_characts, group_number):
    stu = len(id_to_characts)
    lst = []

    while stu > group_number:

        center = np.mean(np.array(list(id_to_characts.values())), axis=0)
        sorted_by_distance = sorted(id_to_characts.items(), key=lambda item: np.sqrt(np.sum(((item[1] - center) ** 2))))
        n_closest = sorted_by_distance[:group_number]
        n_closest_id = [i[0] for i in n_closest]
        lst.append(n_closest_id)

        id_to_characts = {i:id_to_characts[i] for i in id_to_characts if i not in n_closest_id}
        stu = stu - group_number

    left = list(id_to_characts.keys())
    lst.append(left)
    random.shuffle(lst)
    for sublist in lst:
        random.shuffle(sublist)

    res = []

    for i in range(len(lst[0])):
        res.append([item[i] for item in lst])

    print('km done')

    return res

