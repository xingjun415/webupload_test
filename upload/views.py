from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    print("OK")
    return render(request, 'upload.html')

def data(request):
    print("OK")
    files = request.FILES['file']
    print(type(files))
    print(dir(files))
    with open("./" + files.name, "wb") as file:
        for file_upload in files:
            file.write(file_upload)
    return HttpResponse("OK")
