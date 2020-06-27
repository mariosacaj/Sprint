from SPRINTcode.Processing.WordMatchCompound import WordMatchComp
from SPRINTcode.Processing.MatchVectorCompound import MatchVectorComp
from SPRINTcode.Processing.CountMatchCompound import CountMatchcomp

## UPLOAD STANDARD AND REFERENCE AND SELECT FILES
pass

## CONVERT STANDARD AND PRODUCE CANDIDATES
# Getting n numner of matching words for source and taget from model
compoundWordMatch = WordMatchComp()

# Matching words from source to target with oneanother
compoundPairMatch = MatchVectorComp()

# counting pairmatch instances
compoudPaiCount = CountMatchcomp()

## CONFIRM CANDIDATES AND MANUALLY SELECT POSSIBLE OTHER PAIRS
pass

## ANNOTATE
pass
