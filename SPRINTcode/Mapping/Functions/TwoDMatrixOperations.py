import re
from owlready2 import *
from lxml import etree
import numpy as np
import rdflib
import xml.dom.minidom as xp

from .ReadWriteFiles import readXsdFile, readOntology, readTurtle, readXmlFile, readOntologyClass, readOntologyProperty, \
    readXsdFilecomplextype, readXsdFileElementAttribute


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

def makeCompoundList(inputList):
 splittedList=[re.split('[ ]',w) for w in inputList]
 return splittedList


def matchCompound(inputList, modelVocabList):
    output=[]
    for i in inputList:
        x= all(item in modelVocabList for item in i)
        if x:
            output.append(i)
    return output

def create2dMatrix(inputList):
 Output_array = np.asarray(inputList)
 return Output_array

def makeCompound2dArray(inputList):
    output_2dArray=[]
    for i in inputList:
        rs= eval(i)
        output_2dArray.append(rs)
    return output_2dArray

def checkUnderscore(i):
    flag= bool(re.search(r'[_]', i))
    return flag


def splitToList(inputList):
    final_list=[]
    split_space=[re.split('[_|\s]+', w) for w in inputList]
    for x in split_space:
        split_CamelCase=[re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in x]
        flatten_list=[x for sublist in split_CamelCase for x in sublist]
        final_list.append(flatten_list)
    print("Compound list has been created")
    return final_list

def readFile_ontology(path,filename):
    ext = None

    try:
        rdflib.Graph().load(path + filename, format="ttl")
        ext = 'ttl'
    except:
        try:
            get_ontology(path + filename).load()
            ext = 'owl'
        except:
            raise ValueError('Unsupported file type')

    if (ext == 'owl'):
        fileread = readOntology(path, filename)
        return fileread
    elif (ext== 'ttl'):
        fileread= readTurtle(path,filename)
        return fileread

def readFile_standard(path,filename):
    try:
        xp.parse(path + filename)
    except:
        raise ValueError('Unsupported file type')

    return readXsdFile(path, filename)

def readFile(path,filename):
    ext = file_type(path, filename)
    if (ext == 'xsd'):
        fileread = readXsdFile(path, filename)
        return fileread
    elif (ext == 'xml'):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == 'owl'):
        fileread = readOntology(path, filename)
        return fileread
    elif (ext== 'ttl'):
        fileread= readTurtle(path,filename)
        return fileread

def readClass(path,filename):
    owl = 'owl'
    xsd = 'xsd'
    ttl = 'ttl'
    xml = 'xml'
    ext = file_type(path, filename)
    if (ext == xsd):
        fileread = readXsdFilecomplextype(path, filename)
        return fileread
    elif (ext == xml):
        fileread = readXmlFile(path, filename)
        return fileread
    elif (ext == owl):
        fileread = readOntologyClass(path, filename)
        return fileread
    elif (ext== ttl):
        fileread= readTurtle(path,filename)
        return fileread

def readProperties(path, filename):
    owl = 'owl'
    xsd = 'xsd'
    ttl = 'ttl'
    xml = 'xml'
    ext = file_type(path, filename)
    if (ext == xsd):
        fileread = readXsdFileElementAttribute(path, filename)
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