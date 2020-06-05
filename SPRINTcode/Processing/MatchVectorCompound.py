from SPRINTcode.Functions.MatchVocab import get_vocab_list
from SPRINTcode.Functions.ReadWriteFiles import readTextFile, writeCsv
from SPRINTcode.Functions.TwoDMatrixOperations import makeCompound2dArray
from SPRINTcode.Functions.MatchVocab import matchWordsModel
from SPRINTcode.Functions.MatchPair import getValueThreshold
from SPRINTcode.path import *
from SPRINTcode.Processing.modelload import model, vocab_list

class MatchVectorComp:

 s_data= readTextFile(standardsOutput,source_rw)
 t_data= readTextFile(standardsOutput,target_rw)
 print("Step 6: ----------------------->  Model written files has been read")

 del t_data[-1]
 del s_data[-1]

 s_array=makeCompound2dArray(s_data)
 t_array=makeCompound2dArray(t_data)
 print("Step 7: ----------------------->  Made 2D Array.")

 #matching words/Compound words from source to target using model
 matchPair, matchPairOrigin=matchWordsModel(s_array,t_array,model)
 print("Step 8: ----------------------->  Matched words from source to taget using model Match.")

 finalMatchPair, finalMatchPairThresh= getValueThreshold(matchPair)
 finalPairOrigin, finalpairOriginThresh=getValueThreshold(matchPairOrigin)
 print("Step 9: ----------------------->  Filtered threshold on vector value")


 writeCsv(finalMatchPair, standardsOutput ,write_pathVecRaw)
 writeCsv(finalMatchPairThresh, standardsOutput ,write_pathVecThr)
 writeCsv(finalPairOrigin, standardsOutput,write_pathVecOrgRaw)
 writeCsv(finalpairOriginThresh, standardsOutput ,write_pathVecOrgThr)
 print("Step 10: ----------------------> Output files has been written.")
