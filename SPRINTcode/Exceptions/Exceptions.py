import xml.dom.minidom as xp
from owlready2 import get_ontology
import rdflib


class StandardError(Exception):
    pass


class AnnotationError(Exception):
    pass


class ReferenceError(Exception):
    pass


def check_standard(standardFilename):
    try:
        xp.parse(standardFilename)
        return True
    except:
        return False


def check_reference(referenceFilename):
    try:
        rdflib.Graph().load(referenceFilename, format="ttl")
        return True
    except:
        try:
            get_ontology(referenceFilename).load()
            return True
        except:
            return False
