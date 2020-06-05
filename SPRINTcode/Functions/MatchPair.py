
#Function check for list match lists at postion 0, 2 //for compoundword
#val1, val2 are two lists
def isMatchExistscomp(val1, val2, listscore):
    index=-1
    for s in listscore:
        index = index + 1
        s1= s[0]
        s2= s[1]
        match0= list(set(s1).symmetric_difference(val1))
        match2= list(set(s2).symmetric_difference(val2))
        if(len(match0)==0 and len(match2)==0):
          return True, index
    return False,-1


#Function check for match for single words at position 0, 2
#input1 and input2 are words
def isMatchExistsSingle(input1, input2, listscore):
    index=0
    for s in listscore:
        if(s[0]== input1 and s[1]== input2):
            return True,index
        index=index+1
    return False,0


def getValueThreshold(inputlist):
    finallist=[]
    realorigin=[]
    for it in inputlist:
        for i in it:
            realorigin.append(i)
            if (i[4] > 0.5):
                finallist.append(i)
    return realorigin, finallist