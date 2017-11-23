from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    print("OK")
    return render(request, 'upload.html')

def data(request):
    print("OK")
    uploadfile = request.FILES['file']
    print(type(uploadfile))
    print(dir(uploadfile))
    chunk_size = 10 * 2 ** 20
    written_size = 0
    with open("./" + uploadfile.name, "wb") as file:
        for chunk in uploadfile.chunks(chunk_size):
            file.write(chunk)
            written_size += len(chunk)
            print("Percentage : ", str(written_size / uploadfile.size * 100 ) + "%")
    return HttpResponse("OK")
