from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from .forms import UploadFileForm
from annotator.tool.converter import owl2json, xsd2str
from annotator.tool.FileManager.CheckFile import *
import tempfile
import zipfile
import os
from annotator.exceptions import *

# Create your views here.
# Session State
# 1 -> 2 -> 3 -> ... ->  DONE
# flags
# std_sel, ref_sel
# data
# ref, std, tmp

def index(request):
    request.session['state'] = 'RESET'
    context = {'year': 2018, 'article_list': ['m', 'l']}
    return render(request, 'annotator/index.html', context)

def index_try(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_standard(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and handle_uploaded_file_std(request):
            request.session['state'] = 'UP_STD'
            if request.session['std_sel']:
                return HttpResponseRedirect('/reference_upload/')
            else:
                return HttpResponseRedirect('/standard_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form})

def upload_reference(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('')
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid() and handle_uploaded_file_ref(request):
            request.session['state'] = 'UP_REF'
            if request.session['ref_sel']:
                return HttpResponseRedirect('/compare/')
            else:
                return HttpResponseRedirect('/reference_select/')
    else:
        form = UploadFileForm()
    return render(request, 'annotator/upload.html', {'form': form})

def standard_select(request):
    pass

def reference_select(request):
    pass

def compare(request):
    pass

def download(request):
    pass

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
    ## create tmp folder for this session
    temp_dir = tempfile.mkdtemp()
    request.session['tmp'] = temp_dir
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




