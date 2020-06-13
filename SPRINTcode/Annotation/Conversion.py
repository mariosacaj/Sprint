import subprocess
from SPRINTcode.path import *


class ConversionException(Exception):
    pass


def conversion(output_path, schema_path):
    process = subprocess.run(['../jaxb-ri/bin/xjc.sh', '-nv', '-d', output_path, schema_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    ### DEBUG, please remove
    stdout = process.stdout.split('\n')
    for line in stdout:
        print(line.strip())
    ### END DEBUG

    if process.returncode is not 0:
       raise ConversionException('Could Not Convert')

# DICT[entity_name_source] = confirmed_entity_name_target
def annotation(java_path, dict_s_t, elem_list_target, selected_pairs):
    with open(java_path, 'r+') as fd:
        contents = fd.readlines()
        for key, value in dict_s_t.items():
            for line in contents:
                if line.strip().startswith('public'):
                    if 'class' in line:
                        pass

        idx = 0
        str_ = 'new_string' + '\n'
        contents.insert(idx, str_)  # new_string should end in a newline



        fd.seek(0)  # readlines consumes the iterator, so we need to start over
        fd.writelines(contents)


if __name__ == '__main__':
    try:
        conversion(standardsInput, standardsInput + targetfile)
    except ConversionException as e:
        print(e)
