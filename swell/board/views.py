from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .models import UserGroup
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from dotenv import load_dotenv
import os
load_dotenv()
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

def display_envelopes(request):
    envelopes = UserGroup.objects.all(user=request.user)
    pass