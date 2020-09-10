from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseBadRequest
from annotator.api import *
import tempfile
import os
from annotator.exceptions import *
from Sprint.settings import PATH_FILES, MODEL_DIR, MODEL_NAME, URI_TOOL_PATH, OWL_TOOL_PATH, ONT_TOOL_PATH
import shutil


def index(request):
    try:

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

            # std_dir_abs = os.path.join(request.session['tmp'], standard_dir)
            # ASSIGNMENT IS USR CHOICE
            std_file = 'std.xsd'
            #
            #

            try:
                process_standard(request, std_file)
            except StandardError as e:
                return redirect_wait(request, e, "standard_select")
            except BaseException as r:
                return redirect_wait(request, "ERROR: " + str(r), "index")
        else:
            return render(request, 'annotator/select.html')
    return HttpResponseRedirect('/reference_upload/')


def process_standard(request, std_file):
    if not check_standard(std_file):
        raise StandardError("File not well formatted")
    standard_dict = standard_init(request.session['tmp'], std_file, URI_TOOL_PATH, ONT_TOOL_PATH)
    request.session['std'] = std_file
    request.session['standard_dict'] = standard_dict
    request.session['std_sel'] = True


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


def reference_select(request):
    if not request.session['ref_up']:
        return HttpResponseRedirect('/reference_upload/')
    if not request.session['ref_sel']:
        if request.method == 'POST':

            #
            # ASSIGNMENT IS USR CHOICE
            ref_file = 'it.owl'
            #
            #

            try:
                process_reference(request, ref_file)
            except ReferenceError as e:
                return redirect_wait(request, e, "reference_select")
            except BaseException as r:
                return redirect_wait(request, "ERROR: " + str(r), "index")
        else:
            return render(request, 'annotator/select.html')
    return HttpResponseRedirect('/compare/')


def process_reference(request, ref_file):
    ext = check_reference(ref_file)
    if ext == '':
        raise ReferenceError("File not well formatted")
    reference_dict, ext, new_ref_file = reference_init(ref_file, ext)
    request.session['ext'] = ext
    request.session['ref_sel'] = True
    request.session['ref'] = new_ref_file
    request.session['reference_dict'] = reference_dict


def path_to_dict(path):
    d = {'name': os.path.basename(path)}
    if os.path.isdir(path):
        d['type'] = "directory"
        d['children'] = [path_to_dict(os.path.join(path, x)) for x in os.listdir(path)]
    else:
        d['type'] = "file"
    return d


def get_standard_path(request):
    if not request.session['std_up'] and request.session['std_sel']:
        return HttpResponseBadRequest()
    return JsonResponse(path_to_dict(request.session['std']))


def get_reference_path(request):
    if not request.session['ref_up'] and request.session['ref_sel']:
        return HttpResponseBadRequest()
    return JsonResponse(path_to_dict(request.session['ref']))


def compare(request):
    if not request.session['ref_sel'] or not request.session['std_sel']:
        return HttpResponseBadRequest()
    request.session['done'] = True
    return render(request, 'annotator/compare.html')


def download(request):
    if not request.session['std_sel']:
        return HttpResponseRedirect('/compare/')
    file_dir = os.path.join(request.session['tmp'], java_dir)

    dict_confirmed = {'a': '1', 'b': '2', 'c': '3'}

    validation(request, dict_confirmed)
    annotate_dict_and_build(dict_confirmed, request.session['tmp'], request.session['std'])

    return send_zip(file_dir, request)


def send_zip(file_dir, request):
    fpath = shutil.make_archive(file_dir, 'zip', file_dir)
    with open(fpath, 'rb') as fh:
        response = HttpResponse(fh.read(), content_type="application/zip")
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(fpath)
        return response


def validation(request, dict_confirmed):
    for key, value in dict_confirmed.items():
        std_type = request.session['standard_dict']
        ref_type = request.session['reference_dict']
        if ref_type != '' and std_type != '' and std_type != ref_type:
            raise AnnotationError('Validation failed')


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
        candidates_dict = get_candidates(request.session['tmp'], request.session['std'],
                                         request.session['ref'], request.session['standard_dict'],
                                         MODEL_DIR + MODEL_NAME, request.session['reference_dict'],
                                         request.session['ext'])
        request.session['candidates_dict'] = candidates_dict
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
    return JsonResponse(y)


def get_xsd(request):
    if not request.session['std_sel']:
        return HttpResponseBadRequest()
    try:
        y = xsd2str(request.session['std'])
    except StandardError:
        return HttpResponseBadRequest()
    return HttpResponse(y, content_type="application/xml")


def handle_uploaded_file(source, tmp):
    fd, filepath = tempfile.mkstemp(prefix=source.name, dir=tmp)
    with open(filepath, 'wb') as dest:
        shutil.copyfileobj(source, dest)
    return filepath


def handle_file(request, flag: str):
    temp_dir = request.session['tmp']
    f = request.FILES['file']
    f = handle_uploaded_file(f, request.session['tmp'])
    file_writedown(f, flag, request, temp_dir)


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
    request.session["msg_r"] = str(msg)
    request.session["url_r"] = reverse(view_name)
    return HttpResponseRedirect('/redirect/')


def redirect_view(request):
    return render(request, 'annotator/redirect.html',
                  {"msg": request.session["msg_r"], "url": request.session["url_r"]})
