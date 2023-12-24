from django.http import HttpResponseServerError
from django.shortcuts import render
from .models import UserGroup
from envelope.models import Envelope
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from envelope.views import valid_invite, send_invite

@login_required
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

@login_required
def envelope(request, envelope_id):
    user = request.user
    try:
        user_group = UserGroup.objects.get(user=user, env_id=envelope_id)
        envelope = user_group.envelope
        questions = get_envelope_questions(envelope)
        context = {
            'envelope_id': envelope_id,
            'envelope': envelope,
            'user': user,
            'questions': questions,
        }
        return render(request, 'envelope.html', context)
    except ObjectDoesNotExist:
        messages.success(request, "You do not have permission to view this page.")
        return render(request, 'home.html')
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred. Please try again later.")

@login_required
def envelope_members(request, envelope_id):
    user = request.user
    try:
        # retrieve all of the users in the envelope
        envelope = Envelope.objects.get(envelope_id=envelope_id)
        envelope_admin = envelope.envelope_admin
        envelope_users = UserGroup.objects.filter(envelope=envelope)
        context = {
            'user': user,
            'envelope_admin': envelope_admin,
            'envelope': envelope,
            'envelope_users': envelope_users,
        }
        # if the admin clicks the 'add user' button
        if request.method == 'POST' and user == envelope_admin:
            # allow admin to invite users to the envelope
            invite_email = request.POST.get('user_email')
            if valid_invite(invite_email) != None:
              send_invite(request, envelope_id, invite_email)
              messages.success(request, f"Invite sent to {invite_email}")       
        return render(request, 'envelope_members.html', context)
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred. Please try again later.")

# returns a list envelopes the user has joined
def get_joined_envelopes(request):
    joined_envelopes = []
    user_groups = UserGroup.objects.filter(user=request.user)
    for user_group in user_groups:
        joined_envelopes.append(user_group.envelope)
    return joined_envelopes

# retrieves all questions associated with envelope
# returns list of all questions
def get_envelope_questions(envelope):
    questions_admin = envelope.questions_admin.all()
    questions_user = envelope.questions_user.all()
    questions_default = envelope.questions_default.all()
    return list(chain(questions_admin, questions_user, questions_default))