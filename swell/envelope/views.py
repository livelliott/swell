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
from django.utils import timezone
from datetime import datetime, time
import re

@login_required
def envelope_create(request):
    if request.method == 'POST':
        form = EnvelopeForm(request.POST)
        if form.is_valid():
            envelope_form = form.save(commit=False)
            members = form.cleaned_data['members']
            envelope_name = form.cleaned_data['envelope_name']
            # partition invitees
            split_members = [member.strip() for member in members.split(' ')]
            # send invite to each
            for member in split_members:
                if valid_invite(member):
                    pass
                    # send invite
                else:
                    pass
                    # save and display could not send invite message
                pass
            # create envelope instance
            envelope = Envelope.objects.create(envelope_name=envelope_name)
            group = Group.ojects.create(group_name=envelope_name)
            # save to database
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
    # if valid username in user database
    username = User.objects.filter(username=user).first()
    if not username == None:
        # retrieve and return valid email
        user_found = get_object_or_404(User, username=user)
        return user_found.email
    return None