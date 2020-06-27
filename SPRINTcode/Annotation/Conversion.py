import subprocess
from SPRINTcode.path import *


class StandardError(Exception):
    pass


class AnnotationError(ValueError):
    pass


class ReferenceValue:
    def __init__(self, p_c, concept):
        self.P_C = p_c
        self.concept = concept

    def get_concept(self):
        return self.concept

    def get_type(self):
        return self.P_C


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
        raise StandardError('Could Not Convert')


# DICT[entity_name_source] = value
def annotation(java_path, dict_s_t, elem_list_target, selected_pairs):
    with open(java_path, 'r+') as fd:
        contents = fd.readlines()
        for key, value in dict_s_t.items():

            for idx, line in enumerate(contents):

                # FIND CONCEPT IN STANDARD
                val = '@XmlType(name = "' + key + '"' in line or '@XmlElement(name = "' + key + '"' in line or '@XmlAttribute(name = "' + key + '"' in line
                if val and not line.strip().startswith('*'):
                    white_space = line.rstrip()[:-len(line.strip())]

                    # FIND CLASS OR ATTRIBUTE
                    index = 0
                    for idy, ll in enumerate(contents[idx:]):
                        if ll.strip().startswith('public') or ll.strip().startswith('private') or ll.strip().startswith(
                                'protected'):
                            if 'class' in ll and value.get_type() == 'P':
                                raise AnnotationError('Class/property mismatch: ' + key)
                            if 'class' not in ll and value.get_type() == 'C':
                                raise AnnotationError('Class/property mismatch: ' + key)
                            index = idy
                            break

                    # ANNOTATE
                    if value.get_type() == 'C':
                        incipit = '@RdfsClass("'
                    else:
                        incipit = '@RdfProperty(propertyName="'
                    contents.insert(idx + index, white_space + incipit + value.get_concept() + '")\n')

                    break

        fd.seek(0)  # readlines consumes the iterator, so we need to start over
        fd.writelines(contents)


if __name__ == '__main__':
    try:
        conversion(standardsInput, standardsInput + targetfile)
    except StandardError as e:
        print(e)
