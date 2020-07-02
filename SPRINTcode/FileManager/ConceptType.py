from SPRINTcode.FileManager.QualifiedReadFiles import *
from SPRINTcode.FileManager.ReadFiles import *


def standard_concept_type(standard_path):
    dict_standard_type = {}
    iterator = [(readXsdFile(standard_path), ''), (readXsdFilecomplextype(standard_path), 'C'),
                (readXsdFileElementAttribute(standard_path), 'P')]
    for it in iterator:
        for concept in it[0]:
            dict_standard_type[concept] = it[1]
    return dict_standard_type


def reference_concept_type(reference_path, ext):
    if ext == 'owl':
        return qualified_concept_type_owl(reference_path)
    else:
        return qualified_concept_type_ttl(reference_path)


def qualified_concept_type_ttl(reference_path):
    dict_reference_type = {}
    for concept in readQualifiedTurtle(reference_path):
        dict_reference_type[concept] = ''
    return dict_reference_type


def qualified_concept_type_owl(reference_path):
    dict_reference_type = {}
    for concept in readQualifiedOWLClass(reference_path):
        dict_reference_type[concept] = 'C'
    for concept in readQualifiedOWLProperty(reference_path):
        dict_reference_type[concept] = 'P'
    return dict_reference_type
