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
            # retrieve info from the form
            envelope_name = form.cleaned_data['envelope_name']
            envelope_query_date = form.cleaned_data['envelope_query_date']
            envelope_due_date = form.cleaned_data['envelope_due_date']
            envelope_form.envelope_admin = request.user
            # create envelope instance
            # Create envelope instance with envelope_admin set to the current user
            Envelope(envelope_name=envelope_name,
                     envelope_query_date=envelope_query_date,
                     envelope_due_date=envelope_due_date)
            # send invitations via email
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

# sends invites to all members via email
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
