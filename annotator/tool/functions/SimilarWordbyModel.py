
#finding similarity for list of words within model, number = topmost example 10, 20 etc
def getSimilarWordsAndVec(inputList, model, number):
 similarWordDict={}
 #for i in range(0,10):
 for i in range(0,len(inputList)):
    s= model.most_similar(inputList[i], topn=number)
    similarWordDict[inputList[i]]= (s)
 return similarWordDict


def  getSimilarWordsSingle(inputList, model, number):
 similarWordList=[]
 #for word in range(0,10):
 for word in range(0,len(inputList)):
     s = model.most_similar(inputList[word], topn=number)
     tmpl=[inputList[word]]
     for m_word in s :
       tmpl.append(m_word[0])
     similarWordList.append(tmpl)
 return similarWordList


def  getSimilarWordsCompound(inputList, model, number):
 similarWordList=[]
 #for word in range(0,10):
 for word in range(0,len(inputList)):
     s = model.most_similar(inputList[word], topn=number)
     tmpl=[inputList[word]]
     for m_word in s :
       tmpl.append([m_word[0]])
     similarWordList.append(tmpl)
 print("words has been matched to model vocablist")
 return similarWordList


def getSimilarWordSum(inputList,model,number):
 similarWordList=[]
 opveclist=[]
 for i in inputList:
    opvecf= 0
    opveclist.append(i)
    for x in i:
        opvec1= model.word_vec(x)
        opvecf= opvec1+opvecf
    opvector= model.similar_by_vector(opvecf,number)
    tmpl = [i]
    for m_word in opvector:
        tmpl.append([m_word[0]])
    similarWordList.append(tmpl)
 return similarWordList

def getSimilarWordAvg(inputList,model,number):
 similarWordList=[]
 opveclist=[]
 for i in inputList:
    opvecf= 0
    opveclist.append(i)
    for x in i:
        opvec1= model.word_vec(x)
        opvecf= opvec1+opvecf
    opvector= model.similar_by_vector((opvecf/len(i)),number)
    tmpl = [i]
    for m_word in opvector:
        tmpl.append([m_word[0]])
    similarWordList.append(tmpl)
 return similarWordList