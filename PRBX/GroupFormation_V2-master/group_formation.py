from utils import *
import os

def form_groups(csv_file_folder, group_num, uuid, algorithm_type):
    input_file_name = uuid + '_input.csv'
    input_file_path = os.path.join(csv_file_folder, input_file_name)
    out_put_file_name = uuid + '_output.csv'
    output_file_path = os.path.join(csv_file_folder, out_put_file_name)

    student_info = read_student_info(input_file_path, out_put_file_name)
    if not student_info:
        write_error_message(output_file_path, 'file has no content')
        return

    message = validate_format(student_info, group_num)
    if message:
        write_error_message(output_file_path, message)
        return

    id_to_characts = map_id_to_characts(student_info, output_file_path, algorithm_type)
    answer = run(id_to_characts, group_num, algorithm_type)

    write_groups_info(output_file_path, answer)

