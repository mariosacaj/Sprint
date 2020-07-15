# from annotator.tool.Mapping.Routines import *
# import os
# from annotator.tool.JavaLoad import *
# from annotator.exceptions import *
#
# ## INIT + START SERVER (ONCE FOR ALL) -- NOT INTERACTIVE
# standardInput = os.getcwd() + '/data/standard/'
# referenceInput = os.getcwd() + '/data/reference/'
# output_path = os.getcwd() + '/data/output_map/'
# java_path = os.getcwd() + '/data/javaclass/'
# modelpath = os.getcwd() + '/data/model/GoogleNews-vectors-negative300.bin'
# jaxb_path = 'jaxb-ri/bin/xjc.sh'
# source_rw = 's_SumArray3.csv'
# target_rw = 't_SumArray3.csv'
# write_pathVecRaw = 'SumVecRaw.csv'
# write_pathVecThr = 'SumVecThr.csv'
# write_pathVecOrgRaw = 'SumVecOrgRaw.csv'
# write_pathVecOrgThr = 'SumVecOrgThr.csv'
# readpathCompound = 'SumVecOrgThr.csv'
# writepathCompound = 'Sumst_MatchCount.csv'
# URIToolFilePath = os.getcwd() + '/URIConverterTool.jar'
# # model loaded in memory
# model, vocab_list = get_vocab_list(modelpath)
#
# ###### USER SPECIFIC ###### -- NEW THREAD
# ## UPLOAD STANDARD AND REFERENCE AND SELECT FILES -- INTERACTIVE
#
# # load Java Library for Java code manipulation
# java_man = instantiate_java_code_manipulator(java_path, URIToolFilePath)
#
# # Standard and reference are uploaded
#
# # User choice
# while True:
#     # Assignment is user choice
#     standard_file = 'StructuralModel-XSD/GeoInfra/Transportation.xsd'
#     if check_standard(standardInput + standard_file):
#         break
#
# while True:
#     # Assignment is user choice
#     reference_file = 'it.owl'
#     ext = check_reference(referenceInput + reference_file)
#     if ext:
#         break
#
# ## CONVERT STANDARD AND PRODUCE CANDIDATES -- NOT INTERACTIVE
# # Generate Java Code Model
#
# try:
#     java_man.generateFromSchema(standardInput + standard_file)
# except:
#     raise StandardError('Cannot create Java Code')
#
# ## create dicts for both standard and reference like this: dict[name] = 'C'/'P'/'' (as for 'Class', 'Property' and unknown)
# standard_dict = standard_concept_type(standardInput + standard_file)
# reference_dict = reference_concept_type(referenceInput + reference_file, ext)
#
# ## candidates creation with mapping tool
# candidates_dict = produce_final_candidates(standardInput + standard_file, referenceInput + reference_file,
#                                            output_path, vocab_list,
#                                            model, source_rw, target_rw,
#                                            write_pathVecOrgThr,
#                                            writepathCompound, ext)
#
# candidates_dict = prune_mismatch_type(candidates_dict, standard_dict, reference_dict)
#
# # tree similarity? a class is similar to another one if they have many semantically similar properties...
#
# ## CONFIRM CANDIDATES AND MANUALLY SELECT  OTHER POSSIBLE PAIRS -- INTERACTIVE
# pass
# dict_confirmed = {}
# dict_confirmed['OnboardServiceCategoryId'] = 'st4rt:Service'
# dict_confirmed['ExternalId'] = 'st4rt:External'
# dict_confirmed['Vehicle'] = 'st4rt:Vehicle'
#
# ## ANNOTATION -- NOT INTERACTIVE
# for key, value in dict_confirmed.items():
#     java_man.annotate(key, value)
#
# java_man.build()
