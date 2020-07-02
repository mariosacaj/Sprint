import xml.dom.minidom as xp
from owlready2 import get_ontology
import rdflib


def check_standard(standard_path):
    try:
        xp.parse(standard_path)
        return True
    except:
        return False


def check_reference(reference_path):
    try:
        rdflib.Graph().load(reference_path, format="ttl")
        return 'ttl'
    except:
        try:
            get_ontology(reference_path).load()
            return 'owl'
        except:
            return ''
