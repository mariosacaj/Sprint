import xml.dom.minidom as xp

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
