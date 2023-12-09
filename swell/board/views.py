from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from .models import Invitation, Group, UserGroup
from dotenv import load_dotenv
import os
load_dotenv()
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

def send_invite(envelope_id, email):
    pass

def custom_invite_link(invite_token):
    custom_link = f"https://{os.getenv('HOST_DOMAIN')}/register/?invite_token={invite_token}"
