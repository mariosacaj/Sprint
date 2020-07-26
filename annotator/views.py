from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from annotator.forms import UploadFileForm
from annotator.api import *
import tempfile
import os
from annotator.exceptions import *
from Sprint.settings import PATH_FILES, MODEL_DIR, MODEL_NAME, URI_TOOL_PATH, OWL_TOOL_PATH
import shutil

SHARED_DICT = {}


def create_user_folder(request):
    ## create tmp folder for this session
    temp_dir = tempfile.mkdtemp(dir=PATH_FILES)
    request.session['tmp'] = temp_dir
    return temp_dir


def index(request):
    prune_shared_dict()
    try:
        var = request.session['tmp']
        t = SHARED_DICT[request.session.session_key]
    except:
        # Status
        request.session['std_up'] = False
        request.session['std_sel'] = False
        request.session['ref_up'] = False
        request.session['ref_sel'] = False
        request.session['done'] = False

        # file paths
        request.session['std'] = None
        request.session['ref'] = None
        request.session['tmp'] = create_user_folder(request)
        request.session['ext'] = None

        # Session objects
        session_dict = {}
        session_dict['annotator'] = None
        session_dict['standard_dict'] = None
        session_dict['candidates_dict'] = None
        session_dict['reference_dict'] = None
        SHARED_DICT[request.session.session_key] = session_dict
    return render(request, 'annotator/index.html')


def prune_shared_dict():
    deleande = []
    keys = get_keys()
    for key in SHARED_DICT.keys():
        if key not in keys:
            deleande.append(key)
    for key in deleande:
        SHARED_DICT.pop(key, 0)


def get_keys():
    from django.contrib.sessions.models import Session
    sessions = Session.objects.all()
    tmp_keys = []
    for session in sessions:
        session_data = session.get_decoded()
        try:
            tmp_keys.append(session_data.session_key)
        except:
            pass
    return tmp_keys


def index_try(request):
    c = dir_list(request.session['tmp'])
    return render(request, 'annotator/index_try.html',
                  {'subfiles': c})


def dir_list(root):
    from django.template import loader

    files = os.listdir(root)
    for mfile in files:
        t = os.path.join(root, mfile)
        if os.path.isdir(t):
            yield loader.render_to_string('annotator/p_folder.html',
                                          {'file': mfile,
                                           'subfiles': dir_list(os.path.join(root, t))})
            continue
        yield loader.render_to_string('annotator/p_file.html',
                                      {'file': mfile})


def upload_standard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if handle_file(request, 'standard'):
            request.session['std_up'] = True
            return HttpResponseRedirect('/standard_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form,
                                                     'var': 'standard'})


def standard_select(request):

    if not request.session['std_up']:
        return HttpResponseRedirect('/standard_upload/')
    if request.session['std_sel']:
        return standard_already_selected(request)

    if request.method == 'POST':
        std_dir = os.path.join(request.session['tmp'], standardInput)
        ## ASSIGNMENT IS USR CHOICE
        std_file = 'std.xsd'
        try:
            annotator, standard_dict = standard_init(request.session['tmp'], std_dir + std_file, URI_TOOL_PATH)
        except BaseException as e:
            return HttpResponse(e)
        request.session['std'] = std_dir + std_file
        session_dict = SHARED_DICT[request.session.session_key]
        session_dict['annotator'] = annotator
        session_dict['standard_dict'] = standard_dict
        SHARED_DICT[request.session.session_key] = session_dict
        request.session['std_sel'] = True
    else:
        return render(request, 'annotator/select.html')



def standard_already_selected(request):
    try:
        annotator, standard_dict = standard_init(request.session['tmp'], request.session['std'], URI_TOOL_PATH)
    except BaseException as e:
        return HttpResponse(e)
    session_dict = SHARED_DICT[request.session.session_key]
    session_dict['annotator'] = annotator
    session_dict['standard_dict'] = standard_dict
    SHARED_DICT[request.session.session_key] = session_dict
    return HttpResponseRedirect('/reference_upload/')


def upload_reference(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('/standard_select/')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if handle_file(request, 'reference'):
            request.session['ref_up'] = True
            return HttpResponseRedirect('/reference_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form, 'var': 'reference'})


def reference_select(request):
    if not request.session['ref_up']:
        return HttpResponseRedirect('/reference_upload/')
    if request.session['ref_sel']:
        return reference_already_selected(request)

    if request.method == 'POST':
        ref_dir = os.path.join(request.session['tmp'], referenceInput)
        ## ASSIGNMENT IS USR CHOICE
        ref_file = 'it.owl'
        session_dict = SHARED_DICT[request.session.session_key]
        try:
            reference_dict, ext = reference_init(ref_dir + ref_file)
        except BaseException as e:
            return HttpResponseBadRequest(e)
        request.session['ext'] = ext
        request.session['ref_sel'] = True
        request.session['ref'] = ref_dir + ref_file
        session_dict['reference_dict'] = reference_dict
        SHARED_DICT[request.session.session_key] = session_dict
        return HttpResponseRedirect('/compare/')
    else:
        return render(request, 'annotator/select.html')



def reference_already_selected(request):
    session_dict = SHARED_DICT[request.session.session_key]
    try:
        reference_dict, ext = reference_init(request.session['ref'])
    except BaseException as e:
        return HttpResponseBadRequest(e)
    request.session['ext'] = ext
    session_dict['reference_dict'] = reference_dict
    SHARED_DICT[request.session.session_key] = session_dict

    return HttpResponseRedirect('/download/')


def compare(request):
    if not request.session['ref_sel'] or not request.session['std_sel']:
        return HttpResponseBadRequest()
    request.session['done'] = True
    return render(request, 'annotator/compare.html')


def download(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('/compare/')
    file_dir = os.path.join(request.session['tmp'], java_dir)

    session_dict = SHARED_DICT[request.session.session_key]
    annotator = session_dict['annotator']
    build(annotator)

    return send_zip(file_dir, request)


def send_zip(file_dir, request):
    fpath = shutil.make_archive(file_dir, 'zip', file_dir)
    with open(fpath, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fpath)
        return response


def annotate(request):
    if request.method == 'POST':
        pass


def get_associations(request):
    # JSON FORMAT {
    #              "standardName1": [
    #                                   ["ref1", 2],
    #                                   ["ref2", 3]
    #                               ],
    #
    #              "standardName2": [
    #                                   ["ref0", 2],
    #                                   ["ref3", 4]
    #                               ]
    #             }
    try:
        session_dict = SHARED_DICT[request.session.session_key]
        candidates_dict = get_candidates(request.session['tmp'], request.session['std'],
                                         request.session['ref'], session_dict['standard_dict'],
                                         MODEL_DIR + MODEL_NAME, session_dict['reference_dict'], request.session['ext'])
        session_dict['candidates_dict'] = candidates_dict
        SHARED_DICT[request.session.session_key] = session_dict
    except:
        return HttpResponseBadRequest()
    return JsonResponse(candidates_dict, safe=False)


def get_ontology(request):
    if not request.session['ref_sel']:
        return HttpResponseBadRequest()
    try:
        y = owl2json(request.session['ref'], OWL_TOOL_PATH)
    except ReferenceError:
        return HttpResponseBadRequest()
    return HttpResponse(y, content_type="application/json")


def get_xsd(request):
    if not request.session['std_sel']:
        return HttpResponseBadRequest()
    try:
        y = xsd2str(request.session['std'])
    except StandardError:
        return HttpResponseBadRequest()
    return HttpResponse(y, content_type="application/xml")


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(source, tmp):
    fd, filepath = tempfile.mkstemp(prefix=source.name, dir=tmp)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    return filepath


def handle_file(request, flag: str) -> bool:
    temp_dir = request.session['tmp']
    f = request.FILES['file']
    f = handle_uploaded_file(f, request.session['tmp'])

    return file_writedown_mng(f, flag, request, temp_dir)
