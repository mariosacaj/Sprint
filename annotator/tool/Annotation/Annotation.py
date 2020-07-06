from annotator.exceptions import AnnotationError


# DICT[entity_name_source] = value
def annotation(java_path, dict_confirmed):
    with open(java_path, 'r+') as fd:
        contents = fd.readlines()
        for key, value in dict_confirmed.items():
            for idx, line in enumerate(contents):
                if not line.strip().startswith('*'):
                    # FIND CONCEPT IN STANDARD
                    found = '@XmlType(name = "' + key + '"' in line or '@XmlElement(name = "' + key + '"' in line or '@XmlAttribute(name = "' + key + '"' in line
                    if found:
                        white_space = line.rstrip()[:-len(line.strip())]

                        # FIND CLASS OR ATTRIBUTE
                        index = 0
                        for idy, ll in enumerate(contents[idx:]):
                            if ll.strip().startswith('public') or ll.strip().startswith(
                                    'private') or ll.strip().startswith(
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
