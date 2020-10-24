# Loads Google Model in memory, so that other processes can use it without reloading
def on_starting(server=None):
    import os, sys
    import gensim
    from threading import Thread
    from Sprint.settings import MODEL_DIR, MODEL_NAME, model_org_name, DEBUG

    if not os.path.isdir(MODEL_DIR):
        os.mkdir(MODEL_DIR)

    model_path = MODEL_DIR + MODEL_NAME
    model_org = MODEL_DIR + model_org_name

    if not os.path.exists(model_path):
        sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Model loading...\n")
        if DEBUG:
            model = gensim.models.KeyedVectors.load_word2vec_format(model_org, binary=True, limit=50000)
        else:
            model = gensim.models.KeyedVectors.load_word2vec_format(model_org, binary=True)

        sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Save RAM friendly format of the model...\n")
        model.init_sims(replace=True)
        model.save(model_path)
        sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Saved! Finish loading...\n")

    t = Thread(target=load_model, args=[model_path])
    t.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
    t.start()


def load_model(model_path):
    from threading import Semaphore
    import sys
    from gensim.models import KeyedVectors

    sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Loading RAM friendly format of the model...\n")
    model = KeyedVectors.load(model_path, mmap='r')
    sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Model loaded!\n")

    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    model.most_similar('stuff')  # any word will do: just to page all in

    sys.stderr.write("[GOOGLE MODEL LOAD ROUTINE]: Model paged in memory. Finished model instantiation.\n")

    Semaphore(0).acquire()  # just hang until process killed

# def hung_model(model):
#     from threading import Semaphore
#     import sys
#
#     model.syn0norm = model.syn0  # prevent recalc of normed vectors
#     model.most_similar('stuff')  # any word will do: just to page all in
#
#     sys.stdout.write("Model paged in memory. Finished model instantiation.")
#
#     Semaphore(0).acquire()  # just hang until process killed
