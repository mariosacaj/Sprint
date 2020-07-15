from annotator.tool.JavaLoad import *
from annotator.tool.FileManager.ConceptType import standard_concept_type, reference_concept_type
from annotator.exceptions import *
import json
from annotator.tool.FileManager.ReadFiles import xsd2str as x2s
from annotator.tool.Mapping.Routines import Concept, rdflib, get_ontology, os, subprocess, produce_final_candidates, \
    prune_mismatch_type, xp

standardInput = '/standard/'
referenceInput = '/reference/'

output_dir = '/output_map/'
java_dir = '/javaclass/'
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


def owl2json(ref_path):
    os.chdir('tool')
    process = subprocess.run(['java', '-jar', 'owl2vowl.jar', '-echo', '-file', ref_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    os.chdir('..')
    if process.returncode is not 0:
        raise ReferenceError('Could Not Convert')

    st = process.stdout

    st = st[st.find("{"):st.rfind("}") + 1]

    return json.loads(st)


def xsd2str(std_path):
    return x2s(std_path)


def standard_init(tmp_folder, xsd_file):
    java_path = os.path.join(tmp_folder, java_dir)
    os.chdir('tool')

    # load Java Library for Java code manipulation
    URIToolFilePath = os.getcwd() + '/URIConverterTool.jar'
    java_man = instantiate_java_code_manipulator(java_path, URIToolFilePath)
    os.chdir('..')

    # Generate Java Code Model

    try:
        java_man.generateFromSchema(xsd_file)
    except:
        raise StandardError('Cannot create Java Code')

    ## create dicts for standard like this: dict[name] = 'C'/'P'/'' (as for 'Class', 'Property' and unknown)
    standard_dict = standard_concept_type(xsd_file)

    return java_man, standard_dict


def reference_init(tmp_folder, xsd_file, ont_file, standard_dict, model_path):
    from gensim.models import KeyedVectors
    # user specific
    model = KeyedVectors.load(model_path, mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    # … plus whatever else you wanted to do with the model

    vocab_list = list(model.vocab.keys())

    ext = check_reference(ont_file)

    reference_dict = reference_concept_type(ont_file, ext)

    ## candidates creation with mapping tool
    candidates_dict = produce_final_candidates(xsd_file, ont_file,
                                               os.path.join(tmp_folder, output_dir), vocab_list,
                                               model, source_rw, target_rw, write_pathVecOrgThr, writepathCompound, ext)

    candidates_dict = prune_mismatch_type(candidates_dict, standard_dict, reference_dict)
    return reference_dict, candidates_dict


def annotate_dict(java_man, dict_confirmed):
    ## ANNOTATION -- NOT INTERACTIVE
    for key, value in dict_confirmed.items():
        java_man.annotate(key, value)


def annotate(java_man, std_concept_str, ref_concept_str):
    java_man.annotate(std_concept_str, ref_concept_str)


def build(java_man):
    java_man.build()
