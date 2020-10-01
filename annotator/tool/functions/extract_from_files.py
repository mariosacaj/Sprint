import numpy as np
import csv
import xml.dom.minidom as xp
import rdflib
import re
import xml.etree.ElementTree as ET
from owlready2 import get_ontology
from lxml import etree


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


def readcsv(filepath):
    datafile = open(filepath, 'r')
    datareader = csv.reader(datafile)
    data = []
    for row in datareader:
        data.append(row)
    return data


def readTextFile(filePath, name):
    file = open(filePath + name, 'r')
    outputList = file.read().split('\n')
    print("file has been read", name)
    return outputList


def readXmlFile(xml_path, xml_name):
    cleaned_elem_list = []
    xml_file = xml_path + xml_name
    tree = ET.parse(xml_file)
    root = tree.getroot()

    elem_list = [elem.tag for elem in root.iter()]
    for elem in elem_list:
        cleaned_elem = re.sub('{.*?}', '', elem)
        splitted_elem = re.findall('[A-Z][^A-Z]*', cleaned_elem)
        for se in splitted_elem:
            cleaned_elem_list.append(se)
    finaList = list(dict.fromkeys(cleaned_elem_list))

    return finaList


def owl_fix_namespaces_inconsistencies(clist, ns_bindings):
    strlist = []
    for c in clist:
        base_iri = c.iri[-len(c.name):]
        try:
            prefix = ns_bindings[base_iri]
        except KeyError:
            prefixList = base_iri.split("/")[-2:]
            if prefixList[1] == '':
                prefix = prefixList[0]
            else:
                prefix = prefixList[1][:-1]

        if prefix == '':
            strlist.append(c.name)
        else:
            strlist.append(prefix + ':' + c.name)

    return strlist


def end_replace(original, to_be_replaced, replacement):
    for i in range(len(original) - len(to_be_replaced)):
        if original[-i - len(to_be_replaced):-i] == to_be_replaced:
            str = original
            str[-i - len(to_be_replaced):-i] = replacement
            return str
    return original

def get_namespaces(filepath):
    g = rdflib.Graph()
    g.parse(filepath)
    ns_bindings = {}
    for i in list(g.namespaces()):
        # Ex: ns_bindings['http://www.it2rail.eu/ontology/shopping#'] = 'shopping'
        ns_bindings[super(rdflib.term.URIRef, i[1]).__repr__()[1:-1]] = i[0]
    return ns_bindings


def clean_split_elem_list(elem_list):
    cleaned_elem_list = []
    for elem in elem_list:
        cleaned_elem = re.sub('{.*?}', '', elem)
        splitted_elem = re.findall('[A-Z][^A-Z]*', cleaned_elem)
        for se in splitted_elem:
            cleaned_elem_list.append(se)
    return cleaned_elem_list


def readOntology(filepath, filename):
    onto = get_ontology(filepath + filename).load()
    clist1 = list(onto.classes())
    clist2 = list(onto.properties())
    strlist1 = [str(i) for i in clist1]
    strlist2 = [str(i) for i in clist2]
    final_term1 = [re.split('[.]', w)[-1] for w in strlist1]
    final_term2 = [re.split('[.]', w)[-1] for w in strlist2]
    final_term = final_term1 + final_term2
    finallist = list(dict.fromkeys(final_term))
    return finallist


def readOntologyClass(filepath, filename):
    onto = get_ontology(filepath + filename).load()
    clist1 = list(onto.classes())
    strlist1 = [str(i) for i in clist1]
    final_term1 = [re.split('[.]', w)[-1] for w in strlist1]
    finallist = list(dict.fromkeys(final_term1))
    return finallist


def readOntologyProperty(filepath, filename):
    onto = get_ontology(filepath + filename).load()
    clist2 = list(onto.properties())
    strlist2 = [str(i) for i in clist2]
    final_term2 = [re.split('[.]', w)[-1] for w in strlist2]
    finallist = list(dict.fromkeys(final_term2))
    return finallist


def readTurtle(filepath, filename):
    g = rdflib.Graph()
    g.load(filepath + filename, format="ttl")
    flist = []
    mlist = []
    for s, p, o in g:
        term = re.findall(r'#(\w+)', s)
        flist.append(term)
        mlist = []
        for i in flist:
            for m in i:
                mlist.append(m)
    newlist = sorted(set(mlist), key=lambda x: mlist.index(x))
    return newlist


def writeArray(inputArray, Opfilename):
    with open(Opfilename, "w+") as my_csv:
        csvWriter = csv.writer(my_csv)
        csvWriter.writerows(inputArray)
        print("file has been written to", Opfilename)


def writeCsv(inputArray, Opfilepath, name):
    np.savetxt(Opfilepath + name, inputArray, fmt='%s', delimiter=",")
    print("file has been saved in", name)


def writeList(inputList, outputFilename):
    with open(outputFilename, "w") as tmpvar:
        for key in inputList:
            tmpvar.write("%s\n" % key)
    print("file has been written to file: ", outputFilename)


# writing dictionary and save to text file
def writeDictionary(inputDictionary, outputFilename):
    with open(outputFilename, "w") as tmpvar:
        for key, value in inputDictionary.items():
            tmpvar.write('%s:%s\n' % (key, value))


# Reading from dictionary
def readDictionary(inputFileName):
    output_Dic = {}
    with open(inputFileName) as raw_data:
        for item in raw_data:
            if ':' in item:
                key, value = item.rstrip("\n").split(':', 1)
                output_Dic[key] = value
            else:
                pass  # deal with bad lines of text here'
        return output_Dic


def readDictionary2(inputFilename):
    data = {}
    translation = {39: None}
    with open(inputFilename) as raw_data:
        for item in raw_data:
            if ':' in item:
                key, value = item.strip('\n').split(':', 1)
                data[key] = value.replace('"', '').replace("'", '')
            else:
                pass  # deal with bad lines of text here'
        finaldic = (str(data).translate(translation))
    return finaldic


def readFile(path, filename):
    ext = file_type(path, filename)
    if (ext == 'xsd'):
        fileread = readXsdFile(path + filename)
        return fileread
    elif (ext == 'xml'):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == 'owl'):
        fileread = readOntology(path, filename)
        return fileread
    elif (ext == 'ttl'):
        fileread = readTurtle(path, filename)
        return fileread


def readClass(path, filename):
    owl = 'owl'
    xsd = 'xsd'
    ttl = 'ttl'
    xml = 'xml'
    ext = file_type(path, filename)
    if (ext == xsd):
        fileread = readXsdFilecomplextype(path + filename)
        return fileread
    elif (ext == xml):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == owl):
        fileread = readOntologyClass(path, filename)
        return fileread
    elif (ext == ttl):
        fileread = readTurtle(path, filename)
        return fileread


def readProperties(path, filename):
    owl = 'owl'
    xsd = 'xsd'
    ttl = 'ttl'
    xml = 'xml'
    ext = file_type(path, filename)
    if (ext == xsd):
        fileread = readXsdFileElementAttribute(path + filename)
        return fileread
    elif (ext == xml):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == owl):
        fileread = readOntologyProperty(path, filename)
        return fileread
    elif (ext == ttl):
        fileread = readTurtle(path, filename)
        return fileread


def readFile_ontology(reference_path, ext, ns):
    if ext == 'owl':
        fileread = readQualifiedOWL(reference_path, ns)
        return fileread
    elif ext == 'ttl':
        fileread = readQualifiedTurtle(reference_path, ns)
        return fileread


def readQualifiedOWL(reference_path, namespaces):
    onto = get_ontology(reference_path).load()
    clist1 = list(onto.classes())
    clist2 = list(onto.properties())
    final_term = owl_fix_namespaces_inconsistencies(clist1 + clist2, namespaces)
    finallist = list(dict.fromkeys(final_term))
    return finallist


def readQualifiedOWLClass(reference_path, namespaces):
    onto = get_ontology(reference_path).load()
    clist = list(onto.classes())
    clist = owl_fix_namespaces_inconsistencies(clist, namespaces)
    clist = list(dict.fromkeys(clist))
    return clist


def readQualifiedOWLProperty(reference_path, namespaces):
    onto = get_ontology(reference_path).load()
    plist = list(onto.properties())
    plist = owl_fix_namespaces_inconsistencies(plist, namespaces)
    plist = list(dict.fromkeys(plist))
    return plist


def readQualifiedTurtle(filepath, namespaces):
    g = rdflib.Graph()
    g.load(filepath, format="ttl")
    term_list = []
    for s, p, o in g:
        term_list.append(s.n3(g.namespace_manager))
    newlist = sorted(set(term_list), key=lambda x: term_list.index(x))
    return newlist


def xsd2str(standard_path):
    return xp.parse(standard_path).toxml()


def readFile_standard(standard_path):
    return readXsdFile(standard_path)


def readXsdFilecomplextype(standard_path):
    docread = xp.parse(standard_path)
    getElement5 = getElementandAttribute(docread, 'xsd:complexType')
    listofElements = list(filter(lambda x: x != '', getElement5))
    finallist = list(dict.fromkeys(listofElements))
    return finallist


def readXsdFileElementAttribute(standard_path):
    docread = xp.parse(standard_path)
    getElement1 = getElementandAttribute(docread, 'xsd:element')
    getElement2 = getElementandAttribute(docread, 'xsd:attribute')
    getElement1.extend(getElement2)
    listofElements = list(filter(lambda x: x != '', getElement1))
    finallist = list(dict.fromkeys(listofElements))
    return finallist


def getElementandAttribute(doc, attr):
    readElement = doc.getElementsByTagName(attr)
    listElement = []
    for m in readElement:
        f = m.getAttribute('name')
        listElement.append(f)
    return listElement


def readXsdFile(standard_path):
    docread = xp.parse(standard_path)
    getElement1 = getElementandAttribute(docread, 'xs:element')
    getElement2 = getElementandAttribute(docread, 'xsd:element')
    getElement3 = getElementandAttribute(docread, 'xs:attribute')
    getElement4 = getElementandAttribute(docread, 'xsd:attribute')
    getElement5 = getElementandAttribute(docread, 'xsd:complexType')
    getElement1.extend(getElement2 + getElement3 + getElement4 + getElement5)
    listofElements = list(filter(lambda x: x != '', getElement1))
    finallist = list(dict.fromkeys(listofElements))
    return finallist
