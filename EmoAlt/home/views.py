from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request):
    return render(request, "index.html", context=dict())