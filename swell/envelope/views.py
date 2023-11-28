from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages 
from .models import Envelope
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
import re

@login_required
def create_envelope(request):
    if request.method == "POST":
        # get user info
        name = request.POST.get('envelope_name')
        envelope_members = request.POST.get('envelope_members')
        envelope_id = request.POST.get('envelope_id')
        # create envelope instance
        envelope = Envelope.objects.create(envelope_name=name)
        # add creator to group
        envelope.envelope_members.add(request.user)
        # for all members to be added
        all_users = [member.strip() for member in envelope_members.split(' ')]
        for user in all_users:
            user_to_add = user_found(user)
            # if user found in database
            if user_to_add:
                # add them to the envelope
                envelope.envelope_members.add(user_to_add)
                print("Added " + user)
        messages.success(request, "Successfully created: " + name)
        return redirect(reverse('board:board_home'))
    else:
        return render(request, 'create_envelope.html')

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
