from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def resources(request):
    return render(request, "resources.html", context=dict())
