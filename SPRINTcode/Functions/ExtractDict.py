def extractWords(inputDictionary):
 value0_model=[]
 for key, value in inputDictionary.items():
        value0_model.append(key)
        for i in value:
            value0_model.append(i[0])
 return value0_model


def extractWordsinDict(inputDictionary):
 value0_Dic={}
 for key,val in inputDictionary.items():
     value0_Dic[key]=val[0]
 return value0_Dic