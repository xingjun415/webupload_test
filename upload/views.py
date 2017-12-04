import json, random
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
#import django.middleware.csrf.CsrfViewMiddleware

from upload.models import FileInfo
from upload.uploader import FolderManager

def index(request):
    print("OK")
    return render(request, 'upload.html')

def data(request):
    if request.method != "POST":
        err_info = "Only support POST method now"
        print(err_info)
        return HttpResponse(err_info)

    uploadfile = request.FILES['file']
    if 'chunk' not in request.POST:
        save_file_path = FolderManager.get_save_path(uploadfile.name)
        with open(save_file_path, 'wb') as save_file:
            save_file.write(uploadfile.read())
    else:
        chunk_count, chunk_index = int(request.POST['chunks']), int(request.POST['chunk'])
        save_file_path = FolderManager.save_tmp_file(uploadfile, chunk_count, chunk_index)
        if save_file_path is None:
            return HttpResponse("Upload not complete")

    '''
    fileInfo = FileInfo(path = save_file_path)
    fileInfo.save()
    '''
    return HttpResponse(json.dumps({'status': 'OK', "slide_id": random.randint(1, 200)}), content_type='application/json')
