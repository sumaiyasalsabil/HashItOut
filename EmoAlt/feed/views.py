from django.shortcuts import render
import random
import numpy as np
from . import models
# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

#from .live_graphs import *

def feed(request):

    # Update Database
    update()

    # Display Points
    

    # Close if needed

    return render(request, "feed.html", context={})

NUM_POINTS = 100

"""Test Purposes!!"""
points = np.random.uniform(-1, 1, NUM_POINTS)


def update():

    # Update wave
    update_wave()
    
    # Update Points


def update_wave():
    # Check if wave exists, create if not.
    if not wave_exists():
        create_wave()

def create_wave():
    models.BrainWave.objects.create()

def wave_exists():
    waves = models.BrainWave.objects.filter()
    return bool(waves)














