import gensim
from gensim.models import KeyedVectors
from threading import Semaphore
#init vars
#init model

model_org = '/data/model/GoogleNews-vectors-negative300.bin'
model_path = '/data/model/model.bin'

model = gensim.models.KeyedVectors.load_word2vec_format(model_org, binary=True)
model.init_sims(replace=True)
model.save(model_path)


model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
model.most_similar('stuff')  # any word will do: just to page all in
Semaphore(0).acquire()  # just hang until process killed


# user specific
model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
# … plus whatever else you wanted to do with the model