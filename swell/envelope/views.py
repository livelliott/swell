from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from board.models import Group
from .models import Envelope
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
from invitations.utils import get_invitation_model
from .forms import EnvelopeForm
from django.core.mail import send_mail
from django.conf import settings
import re

@login_required
def envelope_create(request):
    if request.method == 'POST':
        form = EnvelopeForm(request.POST)
        if form.is_valid():
            envelope_form = form.save(commit=False)
            # envelope_id = form.cleaned_data['envelope_id']
            envelope_name = form.cleaned_data['envelope_name']
            members = form.cleaned_data['members']
            invite_members(request, members)
            envelope_form.save()
            return redirect(reverse('envelope:envelope_create_success'))
    else:
        form = EnvelopeForm()
    return render(request, 'envelope_create.html', {'form': form})

@login_required
def envelope_create_success(request):
    return render(request, 'envelope_create_success.html')

# checks if string is a valid email/username
# @return [String] valid email address
def valid_invite(user):
    # if valid email address
    if re.fullmatch(EMAIL_PATTERN, user):
        return user
    else: # if valid username in user database
      try:
        user_instance = User.objects.get(username=user)
        return user_instance.email
      except User.DoesNotExist:
        # Handle the case where the user with the given username does not exist
        return None

# invites all members via email
def invite_members(request, members):
    split_members = [member.strip() for member in members.split(' ')]
    for member in split_members:
        user_email = valid_invite(member)
        if user_email:
            send_mail(subject="Invite to Swell",message="This is where the invite message will be.",from_email=settings.EMAIL_HOST_USER, recipient_list=[user_email], html_message=None)
            messages.success(request, "Invite sent to " + user_email)
            # send invite
        else:
            messages.success(request, "ERROR")
            # save and display could not send invite message
        pass
    pass
