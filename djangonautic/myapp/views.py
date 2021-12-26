from django.shortcuts import render  
from django.http import HttpResponse  
from myapp.functions.functions import handle_uploaded_file  
from myapp.forms import StudentForm 
from .input_preprocess import save_mfcc
from .cnn import classify 
import os
def index(request):  
    if request.method == 'POST':  
        student = StudentForm(request.POST, request.FILES)  
        file=request.FILES['file'].name

        if student.is_valid() and file.endswith('.wav'):  
            handle_uploaded_file(request.FILES['file'])  
            save_mfcc(os.path.dirname(os.path.realpath(__file__))+"/static/upload/"+file,
                json_path=os.path.dirname(os.path.realpath(__file__))+"/audio.json", 
                num_segments=10)

            genre=classify()
            genre = genre[16:]
            return render(request, 'index.html', {'genre':genre})

        else:
            return HttpResponse('Invalid file')

    else:  
        student = StudentForm()  
        return render(request,"index.html",{'form':student, 'genre':""})  