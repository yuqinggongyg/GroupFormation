import csv
import numpy as np
from ga.utils import ga_normed_characts
from km.utils import km_normed_characts
from ga.run import run as ga_run
from km.run import run as km_run

ALGORITHM_TYPE = {'GENETIC_ALGORITHM': 'ga', 'K_MEANS': 'km'}

def write_groups_info(path, group_info):
    with open(path, 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile)
        # write title
        title = ['group/student']
        for i in range(len(group_info[0])):
            title.append("student " + str(i + 1))
        data_writer.writerow(title)
        # write data
        for i in range(len(group_info)):
            data = ["group " + str(i + 1)]
            for j in range(len(group_info[i])):
                data.append(group_info[i][j])
            data_writer.writerow(data)

def write_error_message(path, message):
    with open(path, 'w', newline='') as csvfile:
        data_writer = csv.writer(csvfile)
        data_writer.writerow(['error: ' + message])

def read_student_info(path, output_file_path):
    student_info = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        try:
            next(reader)    # skip the first line
        except:
            return student_info
        for row in reader:
            student_info.append(row)

    return student_info

def validate_format(student_info, group_num):
    if len(student_info) < 4:
        return 'total people number cannot be less than 4'

    if group_num < 2:
        return 'group number cannot be less than 2'

    if len(student_info) % group_num != 0:
        return 'group number is not divisble by total people number'

    cols = []
    for i in range(len(student_info)):
        row = student_info[i]
        if len(row) < 2:
            return 'there must be at least 1 characterstics and a unique ID'
        for j in range(len(row)):
            if len(cols) <= j:
                cols.append(set())
            if not row[j]:
                return 'there is a blank entry'
            if j != 0:
                try:
                    float(row[j])
                except:
                    return 'characterstics contains illegal number format'
            cols[j].add(row[j])

    if len(cols[0]) != len(student_info):
        return 'there are duplicate IDs'

    for i in range(len(cols)):
        if len(cols[i]) == 1:
            return 'there is a column where all characterstics is the same'

    return None

def map_id_to_characts(student_info, output_file_path, algorithm_type):
    dict = {}
    ids = [row[0] for row in student_info]
    characts = np.array(student_info)[:, 1:].astype(float)

    normed = None
    if algorithm_type == ALGORITHM_TYPE['GENETIC_ALGORITHM']:
        normed = ga_normed_characts(characts)
    elif algorithm_type == ALGORITHM_TYPE['K_MEANS']:
        normed = km_normed_characts(characts)
    else:
        normed = ga_normed_characts(characts)


    for idx, row in enumerate(normed):
        dict[ids[idx]] = row

    return dict

def run(id_to_characts, group_num, algorithm_type):
    if algorithm_type == ALGORITHM_TYPE['GENETIC_ALGORITHM']:
        return ga_run(id_to_characts, group_num)
    elif algorithm_type == ALGORITHM_TYPE['K_MEANS']:
        return km_run(id_to_characts, group_num)
    else:
        return ga_run(id_to_characts, group_num)
