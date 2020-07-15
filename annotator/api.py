from annotator.tool.JavaLoad import *
from annotator.tool.FileManager.ConceptType import standard_concept_type, reference_concept_type
from annotator.tool.FileManager.CheckFile import check_reference
import os
import subprocess
from annotator.exceptions import *
import json
from annotator.tool.FileManager.ReadFiles import xsd2str as x2s
from annotator.tool.Mapping.Routines import produce_final_candidates, prune_mismatch_type

standardInput = '/standard/'
referenceInput = '/reference/'
output_path = '/output_map/'
java_dir = '/javaclass/'
source_rw = 's_SumArray3.csv'
target_rw = 't_SumArray3.csv'
write_pathVecRaw = 'SumVecRaw.csv'
write_pathVecThr = 'SumVecThr.csv'
write_pathVecOrgRaw = 'SumVecOrgRaw.csv'
write_pathVecOrgThr = 'SumVecOrgThr.csv'
readpathCompound = 'SumVecOrgThr.csv'
writepathCompound = 'Sumst_MatchCount.csv'


def owl2json(ref_path):
    os.chdir('tool')
    process = subprocess.run(['java', '-jar', 'owl2vowl.jar','-echo', '-file', ref_path],
                             stdout=subprocess.PIPE,
                             universal_newlines=True)
    os.chdir('..')
    if process.returncode is not 0:
        raise ReferenceError('Could Not Convert')

    st = process.stdout

    st = st[st.find("{"):st.rfind("}")+1]

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

def reference_init(tmp_folder, ont_file):
    ext = check_reference(ont_file)
    reference_dict = reference_concept_type(ont_file, ext)

    ## candidates creation with mapping tool
    candidates_dict = produce_final_candidates(standardInput, standard_file, referenceInput,
                                               reference_file,
                                               output_path, vocab_list,
                                               model, source_rw, target_rw, write_pathVecThr, write_pathVecOrgRaw,
                                               write_pathVecOrgThr,
                                               write_pathVecRaw, readpathCompound, writepathCompound, ext)

    candidates_dict = prune_mismatch_type(candidates_dict, standard_dict, reference_dict)
    return reference_dict


