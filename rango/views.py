from django.shortcuts import render
<<<<<<< HEAD
from django.http import HttpResponse
    
def index(request):
    return HttpResponse("Rango says hey there partner!")

def about(requst):
     return HttpResponse("Rango says here is the about page. <a href='/rango/'>Index</a>.")
=======

from django.http import HttpResponse
def index(request):
    return HttpResponse("Rango says hey there partner!")cd Workspace
>>>>>>> 13f636113faafbad0fa0f7ac26e56c98c53af54f
