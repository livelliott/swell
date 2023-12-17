from django.shortcuts import get_object_or_404, redirect, render
from .models import Invitation, UserGroup, Group
from envelope.models import Envelope
from itertools import chain
from dotenv import load_dotenv
import os
load_dotenv()

def home_page(request):
    user = request.user
    created_envelopes = Envelope.objects.filter(envelope_admin=user)
    joined_envelopes = get_joined_envelopes(request)
    all_envelopes =  list(chain(created_envelopes, joined_envelopes))
    sorted_envelopes = sorted(all_envelopes, key=lambda x: x.envelope_due_date)
    context = {
        'user': user,
        'all_envelopes': sorted_envelopes,
    }
    return render(request, 'home.html', context)

def get_joined_envelopes(request):
    joined_envelopes = []
    user_groups = UserGroup.objects.filter(user=request.user)
    for user_group in user_groups:
        joined_envelopes.append(user_group.group.envelope)
    return joined_envelopes