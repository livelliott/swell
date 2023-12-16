from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .models import Invitation, UserGroup
from envelope.models import Envelope
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from dotenv import load_dotenv
import os
load_dotenv()
from django.contrib.auth.decorators import login_required


def home_page(request):
    # Assuming you have a user object
    user = request.user
    created_by = Envelope.objects.filter(envelope_admin=user)
    member_of = UserGroup.objects.filter(user=user)
    invited_to = Invitation.objects.filter(recipient=user)
    context = {
        'user': user,
        'created_by': created_by,
        'member_of': member_of,
        'invited_to': invited_to,
    }
    return render(request, 'home.html', context)