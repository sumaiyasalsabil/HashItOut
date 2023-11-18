from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def feed(request):
    return render(request, "feed.html", context={"date":"nov 17"})
