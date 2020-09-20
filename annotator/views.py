import shutil
import json
import os
import sys
import tempfile
import zipfile

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from Sprint.settings import PATH_FILES, MODEL_DIR, MODEL_NAME, URI_TOOL_PATH, OWL_TOOL_PATH, ONT_TOOL_PATH
from annotator.api import standard_init, reference_init, annotate_dict_and_build, owl2json, standard_dir, \
    reference_dir, java_dir, check_standard, check_reference, xsd2str, get_candidates
from annotator.exceptions import *


# index() -> upload_standard() (-> standard_select() if zip uploaded)
# -> upload_reference() (-> reference_select() if zip uploaded) -> compare() -> download()

def is_hidden(p):
    return p.startswith('.') or p.startswith('__') or p.endswith('.ini')


def index(request):
    try:
        # tmp_ is never created in the proj so this always throws an Exception.
        # Kept is needed in the future
        request.session['tmp_']
    except KeyError:
        # Initialize

        # Status
        request.session['std_up'] = False
        request.session['std_sel'] = False
        request.session['std_zip'] = False
        request.session['ref_up'] = False
        request.session['ref_sel'] = False
        request.session['ref_zip'] = False
        request.session['done'] = False
        request.session['reference_dict'] = None
        request.session['standard_dict'] = None
        request.session['candidates_dict'] = None

        # file paths
        request.session['std'] = None
        request.session['ref'] = None
        request.session['tmp'] = create_user_folder(request)
        request.session['ext'] = None

        # Redirect Info
        request.session["msg_r"] = "Redirecting..."
        request.session["url_r"] = reverse("index")

    return render(request, 'annotator/index.html')


def create_user_folder(request):
    # create tmp folder for this session
    temp_dir = tempfile.mkdtemp(dir=PATH_FILES)
    request.session['tmp'] = temp_dir
    return temp_dir


def upload_standard(request):
    if request.method == 'POST':
        try:
            handle_file(request, 'standard')
            if not request.session['std_zip']:
                process_standard(request, request.session['std'])
            request.session['std_up'] = True
        except StandardError as e:
            return redirect_wait(request, e, "standard")
        except BaseException as r:
            return redirect_wait(request, "ERROR: " + str(r), "index")
    else:
        return render(request, 'annotator/upload.html', {'var': 'standard'})
    return HttpResponseRedirect('/standard_select/')


def standard_select(request):
    if not request.session['std_up']:
        return HttpResponseRedirect('/standard_upload/')
    if not request.session['std_sel']:
        if request.method == 'POST':
            try:
                # Bind relative file path coming from front-end with the
                # missing part (result is actual place in server's filesystem)
                path = request.POST["pathToFile"]
                std_dir_abs = os.path.join(request.session['tmp'], standard_dir)
                std_file = os.path.join(std_dir_abs, path)
                process_standard(request, std_file)
            except StandardError as e:
                # Reload
                return redirect_wait(request, e, "standard_select")
            except KeyError:
                return HttpResponseBadRequest()
            except BaseException as r:
                # Redirect to Home page
                return redirect_wait(request, "ERROR: " + str(r), "index")
        else:
            # Folder which contains the extracted .zip file
            std_dir_abs = os.path.join(request.session['tmp'], standard_dir)

            # Get content of folder and subfolders in the JSON format
            tree_structure = path_to_dict(std_dir_abs)

            # Ask user for actual file inside zip folder
            return render(request, 'annotator/select.html',
                          {'var': 'standard', 'tree': json.dumps(tree_structure), 'root_path': std_dir_abs})
    return HttpResponseRedirect('/reference_upload/')


def process_standard(request, std_file):
    if not check_standard(std_file):
        raise StandardError("File not well formatted")
    # Check if Java classes can be generated with JAXB libraries, produce a dictionary
    # that binds standard concepts with their type ("C" for classes, "P" for properties)
    standard_dict = standard_init(request.session['tmp'], std_file, URI_TOOL_PATH, ONT_TOOL_PATH)
    # Path to file
    request.session['std'] = std_file
    request.session['standard_dict'] = standard_dict
    # File is valid and has been selected
    request.session['std_sel'] = True


# Same as for standard
def upload_reference(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('/standard_select/')
    if request.method == 'POST':
        try:
            handle_file(request, 'reference')
            if not request.session['ref_zip']:
                process_reference(request, request.session['ref'])
            request.session['ref_up'] = True
        except ReferenceError as e:
            return redirect_wait(request, e, "reference")
        except BaseException as r:
            return redirect_wait(request, "ERROR: " + str(r), "index")
    else:
        return render(request, 'annotator/upload.html', {'var': 'reference'})
    return HttpResponseRedirect('/reference_select/')


# Same as for standard
def reference_select(request):
    if not request.session['ref_up']:
        return HttpResponseRedirect('/reference_upload/')
    if not request.session['ref_sel']:
        if request.method == 'POST':
            try:
                path = request.POST['pathToFile']
                ref_dir_abs = os.path.join(request.session['tmp'], reference_dir)
                ref_file = os.path.join(ref_dir_abs, path)
                process_reference(request, ref_file)
            except ReferenceError as e:
                return redirect_wait(request, e, "reference_select")
            except KeyError:
                return HttpResponseBadRequest()
            except BaseException as r:
                return redirect_wait(request, "ERROR: " + str(r), "index")
        else:
            ref_dir_abs = os.path.join(request.session['tmp'], reference_dir)
            tree_structure = path_to_dict(ref_dir_abs)

            return render(request, 'annotator/select.html',
                          {'var': 'reference', 'tree': json.dumps(tree_structure), 'root_path': ref_dir_abs})
    return HttpResponseRedirect('/compare/')


def process_reference(request, ref_file):
    ext = check_reference(ref_file)
    if ext == '':
        raise ReferenceError("File not well formatted")
    # check reference, if it is TTL and can be converted in OWL format do it,
    # then produce a dictionary that binds each reference concept with its type
    # ("C" for classes and "P" for properties)
    reference_dict, new_ext, new_ref_file = reference_init(ref_file, ext)
    # Ext is actual format not filename extension
    request.session['ext'] = new_ext
    request.session['ref_sel'] = True
    request.session['ref'] = new_ref_file
    request.session['reference_dict'] = reference_dict


# helper function for std/ref select
def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "folder"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path) if not is_hidden(x)]
    else:
        d['type'] = "file"
    return d


# Renders the most important page where STD/REF associations are made
def compare(request):
    if not request.session['ref_sel'] or not request.session['std_sel']:
        return HttpResponseBadRequest()
    request.session['done'] = True
    return render(request, 'annotator/compare.html')


# Post the associations and build the annotated JAVA classes
# Then zip them and send them to client
@csrf_exempt
def download(request):
    if request.method == 'POST':
        if not request.session['std_sel']:
            return HttpResponseRedirect('/compare/')
        file_dir = os.path.join(request.session['tmp'], java_dir)
        try:
            dict_confirmed = json.loads(request.body)['associations']
            validation(request, dict_confirmed)
            annotate_dict_and_build(dict_confirmed, request.session['tmp'], request.session['std'])
        except BaseException as e:
            sys.stderr.write(str(e))
            return HttpResponseBadRequest()
        return send_zip(file_dir, request)
    else:
        return HttpResponseBadRequest()


# From now on, helper functions only
def send_zip(file_dir, request):
    fpath = shutil.make_archive(file_dir, 'zip', file_dir)
    with open(fpath, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fpath)
        return response


def validation(request, dict_confirmed):
    for key, value in dict_confirmed.items():
        std_type = request.session['standard_dict'][key]
        ref_type = request.session['reference_dict'][value]
        if not is_valid(std_type, ref_type):
            raise AnnotationError('Validation failed')


def is_valid_view(request):
    if not request.session['ref_sel'] or request.method != 'POST':
        return HttpResponseBadRequest()
    try:
        pair = json.loads(request.body)['pair']
        return HttpResponse(str(is_valid(pair[0], pair[1])), content_type="text/plain")
    except KeyError:
        return HttpResponseBadRequest()


def is_valid(type_base, type_comp):
    return not (type_base != '' and type_comp != '' and type_comp != type_base)


def get_valid_standards(request):
    if not request.session['ref_sel']:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        # term is plain/text content in request body @TODO
        term = ''

        std_type = request.session['standard_dict'][term]
        list_valid = [key for (key, value) in request.session['reference_dict'].items() if is_valid(std_type, value)]
        return JsonResponse(list_valid)
    else:
        return HttpResponseBadRequest()


def get_valid_references(request):
    if not request.session['ref_sel']:
        return HttpResponseBadRequest()
    if request.method == 'POST':
        # term is plain/text content in request body @TODO
        term = ''

        ref_type = request.session['reference_dict'][term]
        list_valid = [key for (key, value) in request.session['standard_dict'].items() if is_valid(ref_type, value)]
        return JsonResponse(list_valid)
    else:
        return HttpResponseBadRequest()


def return_standard_type(request):
    try:
        return JsonResponse(request.session['standard_dict'])
    except:
        return HttpResponseBadRequest()


def return_reference_type(request):
    try:
        return JsonResponse(request.session['reference_dict'])
    except:
        return HttpResponseBadRequest()


def get_associations(request):
    try:
        candidates_dict = get_candidates(request.session['tmp'], request.session['std'],
                                         request.session['ref'], request.session['standard_dict'],
                                         MODEL_DIR + MODEL_NAME, request.session['reference_dict'],
                                         request.session['ext'])
        request.session['candidates_dict'] = candidates_dict
    except:
        return HttpResponseBadRequest()
    return JsonResponse(candidates_dict, safe=False)


# Convert OWL ontology in proper format so that it can be visualized
def get_ontology(request):
    if not request.session['ref_sel']:
        return HttpResponseBadRequest()
    try:
        y = owl2json(request.session['ref'], OWL_TOOL_PATH)
    except ReferenceError:
        return HttpResponseBadRequest()
    return JsonResponse(y)


def get_xsd(request):
    if not request.session['std_sel']:
        return HttpResponseBadRequest()
    try:
        y = xsd2str(request.session['std'])
    except StandardError:
        return HttpResponseBadRequest()
    return HttpResponse(y, content_type="application/xml")


def handle_file(request, flag: str):
    temp_dir = request.session['tmp']
    f = request.FILES['file']
    # Write memory object in persistent file
    fd, filepath = tempfile.mkstemp(prefix=f.name, dir=request.session['tmp'])
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(f, dest)

    # Check if file is zip then extract or move in actual folder
    file_writedown(filepath, flag, request, temp_dir)


def file_writedown(f, flag, request, temp_dir):
    if flag == 'standard':
        input_path = standard_dir
        path = 'std'
        iszip = 'std_zip'
    else:
        input_path = reference_dir
        path = 'ref'
        iszip = 'ref_zip'

    input_path = os.path.join(temp_dir, input_path)

    if os.path.exists(input_path):
        shutil.rmtree(input_path)
    os.makedirs(input_path)
    # IS ZIP
    if zipfile.is_zipfile(f):
        with zipfile.ZipFile(f, 'r') as zipObj:
            # Extract all the contents of zip file in different directory
            zipObj.extractall(input_path)
        request.session[iszip] = True
        request.session[path] = input_path
    else:
        file_name = os.path.basename(f)
        file_path = os.path.join(input_path, file_name)

        shutil.copy(f, file_path)
        request.session[iszip] = False
        request.session[path] = file_path


def redirect_wait(request, msg, view_name):
    # Renders Redirect page with error message
    request.session["msg_r"] = str(msg)
    request.session["url_r"] = reverse(view_name)
    return HttpResponseRedirect('/redirect/')


def redirect_view(request):
    return render(request, 'annotator/redirect.html',
                  {"msg": request.session["msg_r"], "url": request.session["url_r"]})
