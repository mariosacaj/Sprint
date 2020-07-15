from django.apps import AppConfig

class AnnotatorHelperConfig(AppConfig):
    name = 'annotator'

    def ready(self):
        from django.contrib.sessions.models import Session
        from threading import Thread
        from apscheduler.schedulers.background import BackgroundScheduler
        import os
        from Sprint.settings import PATH_FILES, MODEL_DIR, MODEL_NAME, model_org

        if not os.path.isdir(PATH_FILES):
            os.mkdir(PATH_FILES)

        if not os.path.isdir(MODEL_DIR):
            os.mkdir(MODEL_DIR)

        model_path = MODEL_DIR + MODEL_NAME

        t = Thread(target=load_model, args=(model_org, model_path))
        t.daemon = True  # This thread dies when main thread (only non-daemon thread) exits.
        t.start()

        scheduler = BackgroundScheduler()
        scheduler.add_job(delete_tmp_folders, trigger='interval', args=(Session, PATH_FILES), hours=6)
        scheduler.start()



def delete_tmp_folders(Session, path):
    sessions = Session.objects.all()
    from importlib import import_module
    from django.conf import settings
    import os, shutil

    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except:
        pass

    tmp_dirs = []
    for session in sessions:
        session_data = session.get_decoded()
        try:
            tmp_dirs.append(session_data['tmp'])
        except:
            pass

    dirList = os.listdir(path)

    for dir in dirList:
        if dir not in tmp_dirs:
            shutil.rmtree(dir)

    return



def load_model(model_org, model_path):
    import gensim
    from gensim.models import KeyedVectors
    from threading import Semaphore

    model = gensim.models.KeyedVectors.load_word2vec_format(model_org, binary=True)
    model.init_sims(replace=True)
    model.save(model_path)

    model = KeyedVectors.load('GoogleNews-vectors-gensim-normed.bin', mmap='r')
    model.syn0norm = model.syn0  # prevent recalc of normed vectors
    model.most_similar('stuff')  # any word will do: just to page all in

    Semaphore(0).acquire()  # just hang until process killed