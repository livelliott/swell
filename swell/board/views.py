from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from .models import Invitation, UserGroup, Group
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
    member_of = get_joined_envelopes(request)
    invited_to = Invitation.objects.filter(recipient=user)
    context = {
        'user': user,
        'created_by': created_by,
        'member_of': member_of,
        'invited_to': invited_to,
    }
    return render(request, 'home.html', context)

def get_joined_envelopes(request):
    joined_envelopes = []
    user_groups = UserGroup.objects.filter(user=request.user)
    for user_group in user_groups:
        joined_envelopes.append(user_group.group.envelope)
    return joined_envelopes