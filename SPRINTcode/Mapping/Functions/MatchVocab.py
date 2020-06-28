import gensim
import os


def get_vocab_list(model_path):
    # Load Google's pre-trained Word2Vec model.
    if 'Mario6868' in os.getcwd():
        model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True)
    else:
        model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=True, limit=100000)
    # vocab_dict = model.vocab.keys()
    vocab_list = list(model.vocab.keys())
    print("model has been loaded")
    return model, vocab_list


def isVocabIncluded(vocab_list, input_list):
    for voc in vocab_list:
        if voc == input_list:
            return True
    return False

def isWordIncluded(vocab_list, input_list):
    for voc in vocab_list:
        if voc == input_list:
            return voc


def matchCompoundToVocab(inputList, modelVocabList):
    output=[]
    for i in inputList:
        x= all(item in modelVocabList for item in i)
        if x:
            output.append(i)
    print("compound list has been matched to vocab list")
    return output

def matchSingleToVocab(inputlist, model_vocabList):
   tmp_wordlist = []
   model_wordlist = []
   for terms in inputlist:
          terms = terms.lower()
          tmp_wordlist.append(isWordIncluded(model_vocabList, terms))
          model_wordlist = list(filter(lambda x: x != None, tmp_wordlist))
   return model_wordlist

def matchWordsModel(sourcelist, targetlist,mmatch):
     rowIndexSr = -1
     rowIndexTr = -1
     wordsinner = []
     wordsouter = []
     wordsinnerorigin = []
     wordsouterorigin = []
     for sr in sourcelist:
         rowIndexSr = rowIndexSr + 1
         for s in sr:
              for tr in targetlist:
                 rowIndexTr = rowIndexTr + 1
                 for t in tr:
                     score = mmatch.n_similarity(t, s)
                     sr_tmp = [rowIndexSr, s, rowIndexTr, t, score]
                     sr_tmpOrigin = [sourcelist[rowIndexSr][0], s, targetlist[rowIndexTr][0], t, score]
                     wordsinner.append(sr_tmp)
                     wordsinnerorigin.append(sr_tmpOrigin)
              rowIndexTr = -1
     wordsouter.append(wordsinner)
     wordsouterorigin.append(wordsinnerorigin)
     print("comparing both standards using model")
     return wordsouter, wordsouterorigin