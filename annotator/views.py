from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest, Http404
from .forms import UploadFileForm
from annotator.api import *
import tempfile
import zipfile
import os
from annotator.exceptions import *
from Sprint.settings import PATH_FILES, MODEL_DIR, MODEL_NAME
import shutil




def index(request):
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

    # Session objects
    request.session['annotator'] = None
    request.session['standard_dict'] = None
    request.session['candidates_dict'] = None
    request.session['reference_dict'] = None

    context = {'year': 2018, 'article_list': ['m', 'l']}
    return render(request, 'annotator/index.html', context)

def index_try(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_standard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and handle_uploaded_file_std(request):
            request.session['std_up'] = True
            if request.session['std_sel']:
                return HttpResponseRedirect('/reference_upload/')
            else:
                return HttpResponseRedirect('/standard_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form})

def upload_reference(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('/standard_upload/')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and handle_uploaded_file_ref(request):
            request.session['ref_up'] = True
            if request.session['ref_sel']:
                return HttpResponseRedirect('/compare/')
            else:
                return HttpResponseRedirect('/reference_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form})

def standard_select(request):
    if not request.session['std_up']:
        return HttpResponseRedirect('/standard_upload/')
    std_dir = os.path.join(request.session['tmp'], '/standard/')
    if request.method == 'POST':
        ## ASSIGNMENT IS USR CHOICE
        std_file = 'std.xsd'
        try:
            annotator, standard_dict = standard_init(request.session['tmp'], std_dir + std_file)
        except BaseException as e:
            return HttpResponse(e)
        request.session['std'] = std_dir + std_file
        request.session['annotator'] = annotator
        request.session['standard_dict'] = standard_dict
        request.session['std_sel'] = True
    else:
        return render(request, 'annotator/select.html')


def reference_select(request):
    if not request.session['ref_up']:
        return HttpResponseRedirect('/reference_upload/')
    ref_dir = os.path.join(request.session['tmp'], '/reference/')
    if request.method == 'POST':
        ## ASSIGNMENT IS USR CHOICE
        ref_file = 'it.owl'

        try:
            reference_dict, candidates_dict = reference_init(request.session['tmp'], request.session['std'],
                                                             ref_dir + ref_file, request.session['standard_dict'],
                                                             MODEL_DIR + MODEL_NAME)
        except BaseException as e:
            return HttpResponse(e)

        request.session['ref_sel'] = True
        request.session['ref'] = ref_dir + ref_file
        request.session['candidates_dict'] = candidates_dict
        request.session['reference_dict'] = reference_dict
    else:
        return render(request, 'annotator/select.html')

def compare(request):
    if not request.session['ref_sel'] or not request.session['std_sel']:
        return HttpResponseBadRequest()
    request.session['done'] = True
    return render(request, 'annotator/compare.html')

def download(request):
    if not request.session['done']:
        return HttpResponseRedirect('/compare/')
    file_dir = os.path.join(request.session['tmp'], java_dir)
    if os.path.isdir(file_dir):
        return download_zip(file_dir, request)
    raise Http404

def download_zip(file_dir, request):
    zip_loc = file_dir
    zip_dest = request.session['tmp'] + 'zipped'
    shutil.make_archive(base_dir=zip_loc, root_dir=zip_loc, format='zip', base_name=zip_dest)
    with open(zip_dest, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(zip_dest)
        return response


def load_json(request):
    if not request.session['ref_sel']:
        return HttpResponseBadRequest()
    try:
        y = owl2json(request.session['ref'])
    except ReferenceError:
        return HttpResponseBadRequest()
    return JsonResponse(y)

def load_xsd(request):
    if not request.session['std_sel']:
        return HttpResponseBadRequest()
    try:
        y = xsd2str(request.session['std'])
    except StandardError:
        return HttpResponseBadRequest()
    return HttpResponse(y)


# def upload_file(request):
#     if request.method == 'POST':
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             handle_uploaded_file(request.FILES['file'])
#             return HttpResponseRedirect('/success/url/')
#     else:
#         form = UploadFileForm()
#     return render(request, 'upload.html', {'form': form})

def handle_uploaded_file_std(request):
    temp_dir = request.session['tmp']
    f = request.FILES['file']

    std_dir = os.path.join(temp_dir, '/standard/')

    # MIGHT BE USEFUL DON't DELETE
    # file_name = os.path.basename(f.name)
    # file_path = os.path.join(temp_dir, file_name)
    #
    #
    #
    # with open(file_path, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)

    # IS ZIP
    if zipfile.is_zipfile(f.name):
        with zipfile.ZipFile(f.name, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(std_dir)
        request.session['std_sel'] = False
        request.session['std'] = std_dir
        return True
    # IS SINGLE FILE
    elif check_standard(f.name):

        file_name = os.path.basename(f.name)
        file_path = os.path.join(std_dir, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        request.session['std_sel'] = True
        request.session['std'] = file_path
        return True
    else:
        return False


def create_user_folder(request):
    ## create tmp folder for this session
    temp_dir = tempfile.mkdtemp(dir=PATH_FILES)
    request.session['tmp'] = temp_dir
    return temp_dir


def handle_uploaded_file_ref(request):
    f = request.FILES['file']
    ref_dir = os.path.join(request.session['tmp'], '/reference/')

    # MIGHT BE USEFUL DON't DELETE
    # file_name = os.path.basename(f.name)
    # file_path = os.path.join(temp_dir, file_name)
    #
    #
    #
    # with open(file_path, 'wb+') as destination:
    #     for chunk in f.chunks():
    #         destination.write(chunk)

    # IS ZIP
    if zipfile.is_zipfile(f.name):
        with zipfile.ZipFile(f.name, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(ref_dir)
        request.session['ref_sel'] = False
        request.session['ref'] = ref_dir
        return True
    # IS SINGLE FILE
    elif check_reference(f.name):

        file_name = os.path.basename(f.name)
        file_path = os.path.join(ref_dir, file_name)

        with open(file_path, 'wb+') as destination:
            for chunk in f.chunks():
                destination.write(chunk)

        request.session['ref_sel'] = True
        request.session['ref'] = file_path
        return True
    else:
        return False




