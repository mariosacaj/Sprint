from gensim.models import KeyedVectors
# user specific
model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
model.syn0norm = model.syn0  # prevent recalc of normed vectors
# … plus whatever else you wanted to do with the model