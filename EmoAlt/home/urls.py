from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView
from django.urls import include

urlpatterns = [
    path("", views.index, name="index")
]

urlpatterns += staticfiles_urlpatterns()