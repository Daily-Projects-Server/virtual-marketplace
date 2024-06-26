from django.shortcuts import render
from django.http import HttpResponse
from .models import *


def index(request):
    listings = Listing.objects.all()
    return HttpResponse(request, listings)