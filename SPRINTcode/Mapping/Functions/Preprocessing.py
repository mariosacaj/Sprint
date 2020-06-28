import re
import xml.etree.ElementTree as ET


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

    return strlist


def getFileExtension(filename):
    owl='owl'
    xsd='xsd'
    xml='xml'
    ttl='ttl'
    ext=filename.split(".")[1]
    if (ext == owl):
        return owl
    elif(ext == xsd):
        return xsd
    elif(ext == xml):
        return xml
    elif(ext == ttl):
        return ttl


