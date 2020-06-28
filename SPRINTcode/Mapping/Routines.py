from .Functions.MatchVocab import *
from .Functions.SimilarWordbyModel import *
from .Functions.TwoDMatrixOperations import *
from .Functions.MatchVocab import matchWordsModel
from .Functions.MatchPair import getValueThreshold
from typing import List, Any, Union
from .Functions.MatchPair import isMatchExistscomp
from .Functions.ReadWriteFiles import readTextFile, writeCsv
from .Functions.TwoDMatrixOperations import makeCompound2dArray
from collections import defaultdict


class Concept:
    def __init__(self, concept: str, score: int):
        self.type = None
        self.concept = concept
        self.score = score

    def get_concept(self):
        return self.concept

    def set_type(self, type_: str):
        self.type = type_

    def get_type(self):
        return self.type

    def get_score(self):
        return self.score


def extract_and_fetch_from_model(standardInput, standard_file, referenceInput, reference_file, output_path, vocab_list,
                                 model, source_rw, target_rw):
    # INPUT MUST BE XSD
    fileS = readFile_standard(standardInput, standard_file)
    # INPUT MUST BE OWL or TTL
    fileT = readFile_ontology(referenceInput, reference_file)
    # lista di stringhe
    print("Step 1: ------------------------>  Reading files has been done.")
    listS = splitToList(fileS)
    listT = splitToList(fileT)
    print("Step 2: ------------------------>  compound Lists has been created.")
    writeCsv(listS, output_path, 'SourceTerms.csv')
    writeCsv(listT, output_path, 'TargetTerms.csv')
    # mach to word2vec model vocab
    matchVocab_S = matchCompoundToVocab(listS, vocab_list)
    matchVocab_T = matchCompoundToVocab(listT, vocab_list)
    print("Step 3: ----------------------->  Matching and filter with model vocab list has been done.")
    writeCsv(matchVocab_S, output_path, 'SourceVocab.csv')
    writeCsv(matchVocab_T, output_path, 'TargetVocab.csv')
    modelMatch_S = getSimilarWordAvg(matchVocab_S, model, 3)
    modelMatch_T = getSimilarWordAvg(matchVocab_T, model, 3)
    print("Step 4: ----------------------->  Got Similar Words from model")
    writeCsv(modelMatch_S, output_path, source_rw)
    writeCsv(modelMatch_T, output_path, target_rw)
    print("Step 5: ----------------------->  Output files has been written")

    dict_source = {}
    dict_target = {}
    for idx, S in enumerate(listS):
        dict_source[repr(S)] = fileS[idx]
    for idx, T in enumerate(listT):
        dict_target[repr(T)] = fileT[idx]

    return dict_source, dict_target


def produce_candidates(model, output_path, source_rw, target_rw, write_pathVecThr, write_pathVecOrgRaw,
                       write_pathVecOrgThr, write_pathVecRaw):
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
    finalMatchPair, finalMatchPairThresh = getValueThreshold(matchPair)
    finalPairOrigin, finalpairOriginThresh = getValueThreshold(matchPairOrigin)
    print("Step 9: ----------------------->  Filtered threshold on vector value")
    writeCsv(finalMatchPair, output_path, write_pathVecRaw)
    writeCsv(finalMatchPairThresh, output_path, write_pathVecThr)
    writeCsv(finalPairOrigin, output_path, write_pathVecOrgRaw)
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
        descision, index = isMatchExistscomp(inner[0], inner[2], scores)
        if (descision):
            scores[index][2] = scores[index][2] + 1
        else:
            tmplist = [inner[0], inner[2], 1]
            scores.append(tmplist)
            tmplist = []
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

    # RESULT[NameIdStandard] = [RefConcept1, RefConcept2, RefConcept3]
    result = defaultdict(list)
    for key, value in dict_source.items():
        for candidate in list_of_tuples:
            if repr(candidate[0]) == key:
                result[value].append(Concept(dict_target[repr(candidate[1])], candidate[2]))
    return result
