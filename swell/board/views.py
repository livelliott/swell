from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from .models import Invitation, UserGroup
from envelope.models import Envelope
from itertools import chain
from django.contrib import messages 
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
import os
load_dotenv()

def home_page(request):
    user = request.user
    created_envelopes = Envelope.objects.filter(envelope_admin=user)
    joined_envelopes = get_joined_envelopes(request)
    all_envelopes =  set(chain(created_envelopes, joined_envelopes))
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
        joined_envelopes.append(user_group.envelope)
    return joined_envelopes

@login_required
def envelope(request, envelope_id):
    user = request.user
    try:
        user_group = UserGroup.objects.get(user=user, env_id=envelope_id)
        envelope = user_group.envelope
        context = {
            'envelope_id': envelope_id,
            'user': user,
            'envelope': envelope,
        }
        return render(request, 'envelope.html', context)
    except ObjectDoesNotExist:
        messages.success(request, "You do not have permission to view this page.")
        return render(request, 'home.html')
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred. Please try again later.")