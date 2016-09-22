from django.shortcuts import render
from django.http import HttpResponse

import json



# Create your views here.
def index(request):
    #return HttpResponse("You made it!")
    return render(request, 'chillhome/index.html')
    
    
