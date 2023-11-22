from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

@login_required
def create_group(request):
    return render(request, 'create_group.html')