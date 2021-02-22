import sys
import os
import subprocess
import json
import contextlib

import jpype

from Sprint.settings import MODEL_DIR, MODEL_NAME, OWL_TOOL_PATH

from annotator.exceptions import *
from annotator.java_helper import instantiate_java_code_manipulator, instantiate_ont_converter, startJVM

from .tool.functions.extract_from_files import xsd2str as x2s, get_ontology, rdflib, xp, standard_concept_type, \
    reference_concept_type
from .tool.routines import produce_final_candidates, prune_mismatch_type

# Directories
standard_dir = 'standard/'
reference_dir = 'reference/'
output_dir = 'output_map/'
java_dir = 'javaclass/'

# Intermediate files
source_rw = 's_SumArray3.csv'
target_rw = 't_SumArray3.csv'
write_pathVecOrgThr = 'SumVecOrgThr.csv'
writepathCompound = 'Sumst_MatchCount.csv'



def check_standard(standard_path):
    try:
        xp.parse(standard_path)
        return True
    except:
        return False


def check_reference(reference_path):
    try:
        with contextlib.redirect_stderr(None):
            rdflib.Graph().load(reference_path, format="ttl")
        return 'ttl'
    except:
        try:
            get_ontology(reference_path).load()
            return 'owl'
        except:
            return ''


def owl2json(ref_path, ext, ns):
    ont_file = ref_path

    # Translate to OWL if possible
    if ext == 'ttl':
        try:
            Converter = instantiate_ont_converter()
            Converter.convert(ont_file, ont_file + ".owl")
            ont_file = ont_file + ".owl"
        except jpype.JException as e:
            sys.stderr.write("TTL->OWL conversion error: " + str(e))

    process = subprocess.run(['java', '-jar', OWL_TOOL_PATH, '-echo', '-file', ont_file], stdout=subprocess.PIPE,
                             universal_newlines=True)

    if process.returncode is not 0:
        raise ReferenceError('Could Not Convert')

    st = process.stdout
    st = st[st.find("{"):st.rfind("}") + 1]
    response = json.loads(st)

    # During the OWL->VOWL conversion the
    # "namespace->prefix" bindings get messed up.
    # We insert back into the graph the correct
    # bindings.
    ns_b = {y: x for x, y in ns.items()}
    response['header']['prefixList'] = ns_b
    return response


def xsd2str(std_path):
    return x2s(std_path)


def standard_init(tmp_folder, xsd_file):
    # check if code model can be created
    startJVM()

    generate_code_model(tmp_folder, xsd_file)

    # create dict for standard like this: dict[term] = 'C'/'P'/'' (as for 'Class', 'Property' and unknown)
    standard_dict = standard_concept_type(xsd_file)

    return standard_dict


def generate_code_model(tmp_folder, xsd_file):
    java_path = os.path.join(tmp_folder, java_dir)
    if not os.path.exists(java_path):
        os.makedirs(java_path)
    # load Java Library for Java code manipulation
    java_man = instantiate_java_code_manipulator(java_path)
    # Generate Java Code Model
    try:
        java_man.generateFromSchema(xsd_file)
    except BaseException as e:
        sys.stderr.write(str(e))
        raise StandardError(
            'Cannot create Java Code: most probably XML dependencies are missing. Please upload the whole standard zip')
    return java_man


def reference_init(ont_file, ext):
    # create dict for ontology like this: dict[term] = 'C'/'P'/'' (as for 'Class', 'Property' and unknown)
    # create dict for ns like this: namespaces['http://www.it2rail.eu/ontology/shopping#'] = 'shopping'
    reference_dict, namespaces = reference_concept_type(ont_file, ext)
    return reference_dict, namespaces


def get_candidates(tmp_folder, xsd_file, ont_file, standard_dict, reference_dict, ext, ns):
    ####### WE ARE ABLE TO ACCESS THE GOOGLE MODEL WITH LITTLE LATENCY
    ####### BECAUSE THERE IS A BACKGROUND PROCESS THAT KEEPS IT IN MEMORY
    from gensim.models import KeyedVectors
    # user specific
    model = KeyedVectors.load(MODEL_DIR + MODEL_NAME, mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    #######

    vocab_list = list(model.vocab.keys())

    output_path = os.path.join(tmp_folder, output_dir)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ## candidates creation with mapping tool
    candidates_dict = produce_final_candidates(xsd_file, ont_file,
                                               output_path, vocab_list,
                                               model, source_rw, target_rw, write_pathVecOrgThr, writepathCompound, ext,
                                               ns)

    candidates_dict = prune_mismatch_type(candidates_dict, standard_dict, reference_dict)

    return candidates_dict


def annotate_dict_and_build(dict_confirmed: dict, tmp_folder: str, xsd_file: str, ns: dict):
    java_man = generate_code_model(tmp_folder, xsd_file)
    for key, value in dict_confirmed.items():
        if ":" not in value:
            java_man.annotate(key, "ontology:" + value)
        else:
            java_man.annotate(key, value)

    ns_final = []
    for k, v in ns.items():
        if v == '':
            ns_final.append("ontology")
        else:
            ns_final.append(v)
        ns_final.append(k)

    java_man.insertNamespaces(ns_final)
    java_man.build()


# Unused Code
def annotate_dict(java_man, dict_confirmed):
    ## ANNOTATION -- NOT INTERACTIVE
    for key, value in dict_confirmed.items():
        java_man.annotate(key, value)


def annotate(java_man, std_concept_str, ref_concept_str):
    java_man.annotate(std_concept_str, ref_concept_str)


def build(java_man):
    java_man.build()
