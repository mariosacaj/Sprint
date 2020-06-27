from SPRINTcode.Mapping.Routines import *
from SPRINTcode.path import modelpath
from SPRINTcode.Functions.MatchVocab import get_vocab_list

##START SERVER
# Load google model and vocab list
# model_path= dockerread_writepath+modelname
model, vocab_list = get_vocab_list(modelpath)

## UPLOAD STANDARD AND REFERENCE AND SELECT FILES
from SPRINTcode.path import *

## CONVERT STANDARD AND PRODUCE CANDIDATES
# Getting n numner of matching words for source and taget from model
extract_and_fetch_from_model(standardInput, standard_file, referenceInput, reference_file, output_path, vocab_list,
                             model, source_rw, target_rw)

# Matching words from source to target with oneanother
produce_candidates(model, output_path, source_rw, target_rw, write_pathVecThr, write_pathVecOrgRaw, write_pathVecOrgThr,
                   write_pathVecRaw)

# counting pairmatch instances
count_and_spit_output(output_path, readpathCompound, writepathCompound)

## CONFIRM CANDIDATES AND MANUALLY SELECT POSSIBLE OTHER PAIRS
pass

## ANNOTATE
pass
