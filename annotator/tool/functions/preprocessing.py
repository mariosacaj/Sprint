import re
from lxml import etree

from .extract_from_files import readQualifiedOWLClass, readQualifiedOWLProperty, \
    readQualifiedTurtle, readXsdFilecomplextype, readXsdFileElementAttribute, readXsdFile, get_ontology, xp, ET, rdflib


def get_xml_raw_vocab_list(xml_path, xml_name):
    xml_file = xml_path + xml_name
    tree = ET.parse(xml_file)
    root = tree.getroot()
    elem_list = [elem.tag for elem in root.iter()]
    return elem_list


def clean_split_elem_list(elem_list):
    cleaned_elem_list = []
    for elem in elem_list:
        cleaned_elem = re.sub('{.*?}', '', elem)
        splitted_elem = re.findall('[A-Z][^A-Z]*', cleaned_elem)
        for se in splitted_elem:
            cleaned_elem_list.append(se)
    return cleaned_elem_list


def getFileExtension(filename):
    owl='owl'
    xsd='xsd'
    xml='xml'
    ttl='ttl'
    ext=filename.split(".")[1]
    if (ext == owl):
        return owl
    elif (ext == xsd):
        return xsd
    elif (ext == xml):
        return xml
    elif (ext == ttl):
        return ttl


def file_type(path, filename):
    ext = None
    try:
        etree.parse(path + filename)
        try:
            xp.parse(path + filename)
            ext = 'xsd'
        except:
            ext = 'xml'
    except:
        try:
            rdflib.Graph().load(path + filename, format="ttl")
            ext = 'ttl'
        except:
            get_ontology(path + filename).load()
            ext = 'owl'

    if ext is None:
        raise ValueError('Unsupported file type')
    return ext


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
