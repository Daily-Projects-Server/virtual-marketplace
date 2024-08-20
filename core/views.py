# core/views.py
from django.shortcuts import render
from .models import Listing

def index(request):
    listings = Listing.objects.filter(is_active=True)
    return render(request, 'marketplace/index.html', {'listings': listings})
