import sys
import argparse


# Parameters -model -stdIN -stdOUT -Source -Target
sourcefile = sys.argv[4]
targetfile = sys.argv[5]

standardsInput = sys.argv[2]
standardsOutput = sys.argv[3]
modelpath = sys.argv[1]


source_rw = 's_SumArray3.csv'
target_rw = 't_SumArray3.csv'


write_pathVecRaw= 'SumVecRaw.csv'
write_pathVecThr= 'SumVecThr.csv'
write_pathVecOrgRaw= 'SumVecOrgRaw.csv'
write_pathVecOrgThr= 'SumVecOrgThr.csv'

readpathCompound= 'SumVecOrgThr.csv'
writepathCompound= 'Sumst_MatchCount.csv'