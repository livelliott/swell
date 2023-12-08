from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Envelope
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
from invitations.utils import get_invitation_model
from .forms import EnvelopeForm
from django.utils import timezone
from datetime import datetime, time
import re

# @login_required
# def envelope_create(request):
#     if request.method == "POST":
#         # get user info
#         name = request.POST.get('envelope_name')
#         envelope_members = request.POST.get('envelope_members')
#         envelope_id = request.POST.get('envelope_id')
#         # create envelope instance
#         envelope = Envelope.objects.create(envelope_name=name)
#         # add creator to group
#         envelope.envelope_members.add(request.user)
#         # for all members to be added
#         all_users = [member.strip() for member in envelope_members.split(' ')]
#         for user in all_users:
#             user_to_add = user_found(user)
#             # if user found in database
#             if user_to_add:
#                 # add them to the envelope
#                 envelope.envelope_members.add(user_to_add)
#                 print("Added " + user)
#         messages.success(request, "Successfully created: " + name)
#         return redirect(reverse('board:board_home'))
#     else:
#         return render(request, 'envelope_create.html')

# checks if string is existing username or email
# @return - user object if existing in database
def user_found(user):
    # if user added is an email
    if (re.fullmatch(EMAIL_PATTERN, user)):
        print("Sending email invite...")
    else:
      username = User.objects.filter(username=user).first()
      if not username == None:
          return get_object_or_404(User, username=user)

def envelope_create(request):
    if request.method == 'POST':
        form = EnvelopeForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            # Combine the user-provided date with the fixed time (noon)
            instance.envelope_due_datetime = datetime.combine(form.cleaned_data['envelope_due_datetime'], time(12, 0))
            instance.save()
            return redirect(reverse('envelope:envelope_create_success'))
    else:
        form = EnvelopeForm()
    return render(request, 'envelope_create.html', {'form': form})

def envelope_create_success(request):
    return render(request, 'envelope_create_success.html')