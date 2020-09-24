from .functions.match_vocab import matchCompoundToVocab, matchWordsModel
from .functions.match_pairs import getValueThreshold, isMatchExistscomp
from typing import List, Any, Union
from .functions.SimilarWordbyModel import getSimilarWordAvg
from .functions.extract_from_files import readTextFile, writeCsv, readFile_ontology, readFile_standard
from .functions.TwoDMatrixOperations import makeCompound2dArray, splitToList
from collections import defaultdict


def produce_final_candidates(xsd_file, ont_file,
                             output_path, vocab_list,
                             model, source_rw, target_rw, write_pathVecOrgThr, writepathCompound, ext, ns):
    # Getting n number of matching words for source and target from model
    dict_source, dict_target = extract_and_fetch_from_model(xsd_file,
                                                            ont_file,
                                                            output_path, vocab_list,
                                                            model, source_rw, target_rw, ext, ns)
    # Matching words from source to target with one another
    produce_candidates(model, output_path, source_rw, target_rw, write_pathVecOrgThr)
    # counting pair match instances
    count_and_spit_output(output_path, write_pathVecOrgThr, writepathCompound)
    candidates_dict = generate_candidates_dict(dict_source, dict_target, output_path, writepathCompound)
    return candidates_dict


def extract_and_fetch_from_model(standard_path, reference_path, output_path, vocab_list,
                                 model, source_rw, target_rw, ext, ns):
    # INPUT MUST BE XSD
    fileS = readFile_standard(standard_path)
    # INPUT MUST BE OWL or TTL
    fileT = readFile_ontology(reference_path, ext, ns)
    # lista di stringhe
    print("Step 1: ------------------------>  Reading files has been done.")
    listS = splitToList(fileS)

    # MUST DEQUALIFY fileT first
    deq_fileT = []
    for t in fileT:
        deq_fileT.append(t.split(':')[-1])

    listT = splitToList(deq_fileT)

    # print("Step 2: ------------------------>  compound Lists has been created.")
    # writeCsv(listS, output_path, 'SourceTerms.csv')
    # writeCsv(listT, output_path, 'TargetTerms.csv')
    # mach to word2vec model vocab
    matchVocab_S = matchCompoundToVocab(listS, vocab_list)
    matchVocab_T = matchCompoundToVocab(listT, vocab_list)
    # print("Step 3: ----------------------->  Matching and filter with model vocab list has been done.")
    # writeCsv(matchVocab_S, output_path, 'SourceVocab.csv')
    # writeCsv(matchVocab_T, output_path, 'TargetVocab.csv')
    modelMatch_S = getSimilarWordAvg(matchVocab_S, model, 3)
    modelMatch_T = getSimilarWordAvg(matchVocab_T, model, 3)
    # print("Step 4: ----------------------->  Got Similar Words from model")
    writeCsv(modelMatch_S, output_path, source_rw)
    writeCsv(modelMatch_T, output_path, target_rw)
    # print("Step 5: ----------------------->  Output files has been written")

    # CREATE DICT FOR SOURCE & TARGET
    # dict[['fare', 'url', 'travel']] = 'st4rt:fareUrlTravel'
    dict_source = {}
    dict_target = {}
    for idx, S in enumerate(listS):
        dict_source[repr(S)] = fileS[idx]
    for idx, T in enumerate(listT):
        dict_target[repr(T)] = fileT[idx]

    return dict_source, dict_target


def produce_candidates(model, output_path, source_rw, target_rw,
                       write_pathVecOrgThr):
    s_data = readTextFile(output_path, source_rw)
    t_data = readTextFile(output_path, target_rw)
    print("Step 6: ----------------------->  Model written files has been read")
    del t_data[-1]
    del s_data[-1]
    s_array = makeCompound2dArray(s_data)
    t_array = makeCompound2dArray(t_data)
    print("Step 7: ----------------------->  Made 2D Array.")
    # matching words/Compound words from source to target using model
    matchPair, matchPairOrigin = matchWordsModel(s_array, t_array, model)
    print("Step 8: ----------------------->  Matched words from source to target using model Match.")
    # finalMatchPair, finalMatchPairThresh = getValueThreshold(matchPair)
    finalPairOrigin, finalpairOriginThresh = getValueThreshold(matchPairOrigin)
    print("Step 9: ----------------------->  Filtered threshold on vector value")
    # writeCsv(finalMatchPair, output_path, write_pathVecRaw)
    # writeCsv(finalMatchPairThresh, output_path, write_pathVecThr)
    # writeCsv(finalPairOrigin, output_path, write_pathVecOrgRaw)
    writeCsv(finalpairOriginThresh, output_path, write_pathVecOrgThr)
    print("Step 10: ----------------------> Output files has been written.")


def count_and_spit_output(output_path, readpathCompound, writepathCompound):
    comFile = readTextFile(output_path, readpathCompound)
    del comFile[-1]
    comp2dArray = makeCompound2dArray(comFile)
    print("Step 11: ----------------------->  Read files with threshold")
    scores = []
    if len(scores) == 0:
        scores: List[List[Union[int, Any]]] = [[comp2dArray[0][0], comp2dArray[0][2], 0]]
    for inner in comp2dArray:
        decision, index = isMatchExistscomp(inner[0], inner[2], scores)
        if decision:
            scores[index][2] = scores[index][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scores.append(tmplist)

    print("Step 12: ----------------------->  Counting similar instances has been done.")
    writeCsv(scores, output_path, writepathCompound)
    print(" ----------------------> Writing Final Output,Ouput file is ", writepathCompound, )
    print("------------------------- Program has been finished. ----------------------------")

    # count = []
    # if len(count) == 0:
    #     count = testf[0]
    # tmplist = []
    # for i in testf:
    #     match0 = list(set(i[0]).symmetric_difference(count[0]))
    #     if len(match0) == 0:
    #         if count[2] > i[2]:
    #             tmplist.append(count[0])
    #         else:
    #             tmplist.append(i)
    # pass


def generate_candidates_dict(dict_source, dict_target, output_path, writepathCompound):
    getfile = readTextFile(output_path, writepathCompound)
    del getfile[-1]
    list_of_tuples = makeCompound2dArray(getfile)

    # RESULT[NameIdStandard] = [[RefCandidate1, score1], [RefCandidate2, score2], [RefCandidate3, score3]]
    result = defaultdict(list)
    for key, value in dict_source.items():
        for candidate in list_of_tuples:
            if repr(candidate[0]) == key:
                result[value].append([dict_target[repr(candidate[1])], candidate[2]])
    return result


def prune_mismatch_type(candidates_dict, standard_dict, reference_dict):
    # get rid of Class to Property and Property to Class matching
    for key, value in candidates_dict.items():
        new_value = []
        for ref_concept in value:
            std_type = standard_dict[key]
            ref_type = reference_dict[ref_concept[0]]
            if not (std_type != '' and ref_type != '' and std_type != ref_type):
                new_value.append(ref_concept)
        candidates_dict[key] = new_value
    return {k: v for k, v in candidates_dict.items() if v}

# def compute_graph_similarity(std_concept, ref_concept, std_tree, owl_ref_graph):
#     pass
