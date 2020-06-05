from typing import List, Any, Union

from SPRINTcode.Functions.MatchPair import isMatchExistscomp
from SPRINTcode.Functions.ReadWriteFiles import readTextFile, writeCsv
from SPRINTcode.Functions.TwoDMatrixOperations import makeCompound2dArray
from SPRINTcode.path import *

class CountMatchcomp:

 read_writepath =standardsOutput
 comFile= readTextFile(read_writepath,readpathCompound)
 del comFile[-1]
 comp2dArray=makeCompound2dArray(comFile)
 print("Step 11: ----------------------->  Read files with threshold")


 scores=[]
 if len(scores)==0:
    scores: List[List[Union[int, Any]]]=[[comp2dArray[0][0],comp2dArray[0][2],0]]

 for inner in comp2dArray:
    descision, index = isMatchExistscomp(inner[0], inner[2], scores)
    if (descision):
        scores[index][2] = scores[index][2] + 1
    else:
         tmplist = [inner[0], inner[2], 1]
         scores.append(tmplist)
         tmplist = []

 print("Step 12: ----------------------->  Counting similar instances has been done.")
 writeCsv(scores, read_writepath,writepathCompound)
 print(" ----------------------> Writing Final Output,Ouput file is ",writepathCompound,)
 print("------------------------- Program has been finished. ----------------------------")

 getfile= readTextFile(read_writepath, 'Sumst_MatchCount.csv')
 del getfile[-1]
 testf = makeCompound2dArray(getfile)
 count=[]
 if len(count)==0:
     count= testf[0]

 tmplist=[]
 for i in testf:
     match0 = list(set(i[0]).symmetric_difference(count[0]))
     if len(match0)==0:
         if count[2]>i[2]:
             tmplist.append(count[0])
         else:
             tmplist.append(i)

def Nmaxelements(list1, N):
    final_listmax = []
    final_listele = []
    for i in range(0, N):
        max1 = 0
        tmpl=[]
        for j in range(len(list1)):
            if list1[j][2] > max1:
                max1 = list1[j][2]
                tmpl= list1[j]
                ind=j
        list1.pop(ind)
        final_listmax.append(max1)
        final_listele.append(tmpl)
    return final_listmax