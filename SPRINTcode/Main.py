from SPRINTcode.Mapping.Routines import *
from SPRINTcode.Mapping.Functions.MatchVocab import get_vocab_list
from SPRINTcode.Conversion.Conversion import conversion
from SPRINTcode.Exceptions.Exceptions import *
import os

## INIT + START SERVER (ONCE FOR ALL) -- NOT INTERACTIVE
standardInput = os.getcwd() + '/data/standard/'
referenceInput = os.getcwd() + '/data/reference/'
output_path = os.getcwd() + '/data/output_map/'
java_path = os.getcwd() + '/data/javaclass/'
modelpath = os.getcwd() + '/data/model/GoogleNews-vectors-negative300.bin'
jaxb_path = 'jaxb-ri/bin/xjc.sh'
source_rw = 's_SumArray3.csv'
target_rw = 't_SumArray3.csv'
write_pathVecRaw = 'SumVecRaw.csv'
write_pathVecThr = 'SumVecThr.csv'
write_pathVecOrgRaw = 'SumVecOrgRaw.csv'
write_pathVecOrgThr = 'SumVecOrgThr.csv'
readpathCompound = 'SumVecOrgThr.csv'
writepathCompound = 'Sumst_MatchCount.csv'
URIToolFilePath = os.getcwd() + '/URIConverterTool.jar'
# model loaded in memory
model, vocab_list = get_vocab_list(modelpath)

###### USER SPECIFIC ###### -- NEW THREAD
## UPLOAD STANDARD AND REFERENCE AND SELECT FILES -- INTERACTIVE
# Standard and reference are uploaded

while True:
    # Assignment is user choice
    standard_file = 'StructuralModel-XSD/GeoInfra/Transportation.xsd'
    if (check_standard(standardInput + standard_file)):
        break

while True:
    # Assignment is user choice
    reference_file = 'it.owl'
    if (check_reference(referenceInput + reference_file)):
        break

## CONVERT STANDARD AND PRODUCE CANDIDATES -- NOT INTERACTIVE
# Produce java classes and retrieve their paths in the package tree of the standard
package_path: str = conversion(java_path, standardInput + standard_file, jaxb_path, URIConverterPath=URIToolFilePath)
package_path = java_path + package_path.replace('.', '/')

# Getting n number of matching words for source and target from model
dict_source, dict_target = extract_and_fetch_from_model(standardInput, standard_file, referenceInput, reference_file,
                                                        output_path, vocab_list,
                                                        model, source_rw, target_rw)

# Matching words from source to target with one another
produce_candidates(model, output_path, source_rw, target_rw, write_pathVecThr, write_pathVecOrgRaw, write_pathVecOrgThr,
                   write_pathVecRaw)

# counting pair match instances
count_and_spit_output(output_path, readpathCompound, writepathCompound)
candidates_dict = generate_candidates_dict(dict_source, dict_target, output_path, writepathCompound)

# tree similarity?

## CONFIRM CANDIDATES AND MANUALLY SELECT  OTHER POSSIBLE PAIRS -- INTERACTIVE
pass
# dict_confirmed = ...

## ANNOTATION -- NOT INTERACTIVE
(_, _, filenames) = next(os.walk(package_path))
filenames = [f for f in filenames if f[-5:] == '.java' and f != 'package-info.java' and f != 'ObjectFactory.java']
# for java_file in filenames:
#     annotation(package_path + java_file, dict_confirmed)
