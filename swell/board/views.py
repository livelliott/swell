from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')
