import re
import numpy as np


def makeCompoundList(inputList):
 splittedList=[re.split('[ ]',w) for w in inputList]
 return splittedList


def matchCompound(inputList, modelVocabList):
    output=[]
    for i in inputList:
        x= all(item in modelVocabList for item in i)
        if x:
            output.append(i)
    return output

def create2dMatrix(inputList):
 Output_array = np.asarray(inputList)
 return Output_array

def makeCompound2dArray(inputList):
    output_2dArray=[]
    for i in inputList:
        rs= eval(i)
        output_2dArray.append(rs)
    return output_2dArray

def checkUnderscore(i):
    flag= bool(re.search(r'[_]', i))
    return flag


def splitToList(inputList):
    final_list=[]
    split_space=[re.split('[_|\s]+', w) for w in inputList]
    for x in split_space:
        split_CamelCase=[re.sub('([A-Z][a-z]+)', r' \1', re.sub('([A-Z]+)', r' \1', i)).split() for i in x]
        flatten_list=[x for sublist in split_CamelCase for x in sublist]
        final_list.append(flatten_list)
    print("Compound list has been created")
    return final_list



