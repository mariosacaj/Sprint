from owlready2 import get_ontology
import rdflib


def readFile_ontology(reference_path, ext):
    if (ext == 'owl'):
        fileread = readQualifiedOWL(reference_path)
        return fileread
    elif (ext == 'ttl'):
        fileread = readQualifiedTurtle(reference_path)
        return fileread


def readQualifiedOWL(reference_path):
    onto = get_ontology(reference_path).load()
    clist1 = list(onto.classes())
    clist2 = list(onto.properties())
    strlist1 = [str(i) for i in clist1]
    strlist2 = [str(i) for i in clist2]
    final_term1 = [w.replace('.', ':') for w in strlist1]
    final_term2 = [w.replace('.', ':') for w in strlist2]
    final_term = final_term1 + final_term2
    finallist = list(dict.fromkeys(final_term))
    return finallist


def readQualifiedOWLClass(reference_path):
    onto = get_ontology(reference_path).load()
    clist = list(onto.classes())
    clist = [str(i) for i in clist]
    clist = [w.replace('.', ':') for w in clist]
    clist = list(dict.fromkeys(clist))
    return clist


def readQualifiedOWLProperty(reference_path):
    onto = get_ontology(reference_path).load()
    plist = list(onto.properties())
    plist = [str(i) for i in plist]
    plist = [w.replace('.', ':') for w in plist]
    plist = list(dict.fromkeys(plist))
    return plist


def readQualifiedTurtle(filepath):
    g = rdflib.Graph()
    g.load(filepath, format="ttl")
    term_list = []
    for s, p, o in g:
        term_list.append(s.n3(g.namespace_manager))
    newlist = sorted(set(term_list), key=lambda x: term_list.index(x))
    return newlist
