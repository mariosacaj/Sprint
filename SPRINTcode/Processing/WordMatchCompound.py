from SPRINTcode.Functions.MatchVocab import *
from SPRINTcode.Functions.ReadWriteFiles import *
from SPRINTcode.Functions.SimilarWordbyModel import *
from SPRINTcode.Functions.TwoDMatrixOperations import *
from SPRINTcode.path import *
from SPRINTcode.Processing.modelload import model, vocab_list


class WordMatchComp:
 # INPUT MUST BE XSD
 fileS=readFile_standard(standardsInput, sourcefile)

 # INPUT MUST BE OWL or TTL
 fileT=readFile_ontology(standardsInput, targetfile)

 print("Step 1: ------------------------>  Reading files has been done.")

 listS=splitToList(fileS)
 listT=splitToList(fileT)
 print("Step 2: ------------------------>  compound Lists has been created.")

 writeCsv(listS, standardsOutput, 'SourceTerms.csv')
 writeCsv(listT, standardsOutput, 'TargetTerms.csv')

#mach to word2vec model vocab
 matchVocab_S=matchCompoundToVocab(listS,vocab_list)
 matchVocab_T=matchCompoundToVocab(listT,vocab_list)
 print("Step 3: ----------------------->  Matching and filter with model vocab list has been done.")


 writeCsv(matchVocab_S, standardsOutput, 'SourceVocab.csv')
 writeCsv(matchVocab_T, standardsOutput, 'TargetVocab.csv')

 modelMatch_S = getSimilarWordAvg(matchVocab_S,model,3)
 modelMatch_T = getSimilarWordAvg(matchVocab_T,model,3)
 print("Step 4: ----------------------->  Got Similar Words from model")

 writeCsv(modelMatch_S, standardsOutput,source_rw)
 writeCsv(modelMatch_T,  standardsOutput,target_rw)
 print("Step 5: ----------------------->  Output files has been written")