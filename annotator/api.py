import shutil
import sys
import zipfile
import os
import subprocess
import json

import jpype

from annotator.exceptions import *

from .tool.java_helper import instantiate_java_code_manipulator, instantiate_ont_converter, startJVM
from .tool.functions.preprocessing import standard_concept_type, reference_concept_type
from .tool.functions.extract_from_files import xsd2str as x2s, get_ontology, rdflib, xp
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
        rdflib.Graph().load(reference_path, format="ttl")
        return 'ttl'
    except:
        try:
            get_ontology(reference_path).load()
            return 'owl'
        except:
            return ''


def owl2json(ref_path, owl_tool):
    process = subprocess.run(['java', '-jar', owl_tool, '-echo', '-file', ref_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)

    if process.returncode is not 0:
        raise ReferenceError('Could Not Convert')

    st = process.stdout

    st = st[st.find("{"):st.rfind("}") + 1]

    return json.loads(st)


def xsd2str(std_path):
    return x2s(std_path)


def standard_init(tmp_folder, xsd_file, uri_tool, ont_tool):
    # check if code model can be created
    startJVM(uri_tool, ont_tool)

    generate_code_model(tmp_folder, xsd_file)

    # create dicts for standard like this: dict[name] = 'C'/'P'/'' (as for 'Class', 'Property' and unknown)
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
    except:
        raise StandardError('Cannot create Java Code')
    return java_man


def reference_init(ont_file, ext):
    new_ont_file = ont_file
    new_ext = ext
    # Translate to OWL if possible
    if ext == 'ttl':
        try:
            Converter = instantiate_ont_converter()
            Converter.convert(ont_file, ont_file + ".owl")
            new_ont_file = ont_file + ".owl"
            new_ext = "owl"
        except jpype.JException as e:
            sys.stderr.write(str(e))
    reference_dict = reference_concept_type(new_ont_file, new_ext)
    return reference_dict, new_ext, new_ont_file


def get_candidates(tmp_folder, xsd_file, ont_file, standard_dict, model_path, reference_dict, ext):
    from gensim.models import KeyedVectors
    # user specific
    model = KeyedVectors.load(model_path, mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    # … plus whatever else you wanted to do with the model
    vocab_list = list(model.vocab.keys())

    output_path = os.path.join(tmp_folder, output_dir)

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    ## candidates creation with mapping tool
    candidates_dict = produce_final_candidates(xsd_file, ont_file,
                                               output_path, vocab_list,
                                               model, source_rw, target_rw, write_pathVecOrgThr, writepathCompound, ext)

    candidates_dict = prune_mismatch_type(candidates_dict, standard_dict, reference_dict)

    return candidates_dict


def annotate_dict_and_build(dict_confirmed, tmp_folder, xsd_file):
    java_man = generate_code_model(tmp_folder, xsd_file)
    for key, value in dict_confirmed.items():
        java_man.annotate(key, value)
    java_man.build()


def annotate_dict(java_man, dict_confirmed):
    ## ANNOTATION -- NOT INTERACTIVE
    for key, value in dict_confirmed.items():
        java_man.annotate(key, value)


def annotate(java_man, std_concept_str, ref_concept_str):
    java_man.annotate(std_concept_str, ref_concept_str)


def build(java_man):
    java_man.build()


def file_writedown_mng(f, flag, request, temp_dir):
    if flag == 'standard':
        input = standard_dir
        path = 'std'
        sel = 'std_sel'
        fun = check_standard
    else:
        input = reference_dir
        path = 'ref'
        sel = 'ref_sel'
        fun = check_reference
    input = os.path.join(temp_dir, input)
    if os.path.exists(input):
        shutil.rmtree(input)
    os.makedirs(input)
    # IS ZIP
    if zipfile.is_zipfile(f):
        with zipfile.ZipFile(f, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(input)
        request.session[sel] = False
        request.session[path] = input
        os.remove(f)
        return True
    # IS SINGLE FILE
    elif fun(f):
        file_name = os.path.basename(f)
        file_path = os.path.join(input, file_name)

        shutil.copy(f, file_path)
        request.session[sel] = True
        request.session[path] = file_path
        os.remove(f)
        return True
    else:
        os.remove(f)
        return False
