from django.apps import AppConfig

class AnnotatorHelperConfig(AppConfig):
    name = 'annotator'

    def ready(self):
        from django.contrib.sessions.models import Session
        import datetime
        from apscheduler.schedulers.background import BackgroundScheduler
        import os
        from Sprint.settings import PATH_FILES

        if not os.path.isdir(PATH_FILES):
            os.mkdir(PATH_FILES)
        import sys, socket

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(("127.0.0.1", 47200))
        except socket.error:
            sys.stderr.write("[DELETE SESSION FILES SCHEDULER]: Scheduler already started, DO NOTHING\n")
        else:
            scheduler = BackgroundScheduler()
            scheduler.add_job(delete_tmp_folders, trigger='interval', args=(Session, PATH_FILES), minutes=30,
                              id='delete',
                              replace_existing=True, next_run_time=datetime.datetime.now())
            scheduler.start()
            sys.stderr.write("[DELETE SESSION FILES SCHEDULER]: Scheduler started\n")


def delete_tmp_folders(Session, path):
    import os, shutil, sys
    from importlib import import_module
    from django.conf import settings

    engine = import_module(settings.SESSION_ENGINE)
    try:
        engine.SessionStore.clear_expired()
    except NotImplementedError:
        sys.stderr.write("Session engine '%s' doesn't support clearing "
                         "expired sessions.\n" % settings.SESSION_ENGINE)

    sessions = Session.objects.all()

    tmp_dirs = []
    for session in sessions:
        session_data = session.get_decoded()
        try:
            tmp_dirs.append(session_data['tmp'])
        except KeyError:
            pass

    dirList = [os.path.join(path, x) for x in os.listdir(path) if os.path.isdir(os.path.join(path, x))]

    for dir_ in dirList:
        if dir_ not in tmp_dirs:
            sys.stderr.write("[DELETE SESSION FILES SCHEDULER]: deleting dir " + dir_ + "\n")
            shutil.rmtree(dir_)

    return
