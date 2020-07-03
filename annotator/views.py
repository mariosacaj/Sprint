from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.

def index(request):
    context = {'year': 2018, 'article_list': ['m', 'l']}
    return render(request, 'annotator/index.html', context)

def index_try(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def upload_standard(request):
    pass

def upload_reference(request):
    pass

def loading(request):
    pass

def confirm_candidates(request):
    pass

def confirm_graphs(request):
    pass

def download(request):
    pass

from .forms import UploadFileForm

# Imaginary function to handle an uploaded file.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
