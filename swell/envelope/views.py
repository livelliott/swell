from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board.models import Group, Invitation, UserGroup
from .models import Envelope
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
# from board.models import send_invite
from .forms import EnvelopeForm
from django.core.mail import send_mail
from django.conf import settings
import re
import os

# creates an envelope instance and invites users
# @redirect - creation success screen
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
            env = Envelope(envelope_name=envelope_name,
                     envelope_query_date=envelope_query_date,
                     envelope_due_date=envelope_due_date)
            env.save()
            envelope_form.save()
            # create corresponding group instance
            envelope_id = envelope_form.envelope_id
            group = Group.objects.create(envelope=envelope_form)
            group.save()
            # send invitation to envelope via email
            invite_members(request, envelope_id, form.cleaned_data['members'])
            return redirect(reverse('envelope:envelope_create_success'))
    else:
        form = EnvelopeForm()
    return render(request, 'envelope_create.html', {'form': form})

# displays envelope creation success screen
@login_required
def envelope_create_success(request):
    return render(request, 'envelope_create_success.html')

# checks if string is a valid email/username
# @return valid email address
def valid_invite(user):
    # if valid email address
    if re.fullmatch(EMAIL_PATTERN, user):
        return user
    else: # if valid username in user database
      try:
        user_instance = User.objects.get(username=user)
        return user_instance.email
      except User.DoesNotExist:
        # given username does not exist in the database
        return None

# sends invites to all members via email
# @redirect - none
@login_required
def invite_members(request, envelope_id, members):
    split_members = [member.strip() for member in members.split(' ')]
    for member in split_members:
        user_email = valid_invite(member)
        if user_email != None:
            send_invite(request=request, envelope_id=envelope_id, email=user_email)
            messages.success(request, "Invite sent to " + user_email)
        else:
            messages.success(request, "ERROR")
        pass
    pass

# sends email invite with custom link
# @redirect - none
@login_required
def send_invite(request, envelope_id, email):
    # create and send invite
    invite = Invitation.objects.create(envelope_id=envelope_id, email=email, sender=request.user)
    group = get_object_or_404(Group, envelope_id=invite.envelope_id)
    custom_link = f"http://{os.getenv('HOST_DOMAIN')}/accept-invite/{invite.invite_token}"
    send_mail(subject="Invite to Swell",
              message=f"Invite link: {custom_link}",
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              html_message=None)
    # connect invite to group
    group.group_invitations.add(invite)
    user_group = UserGroup.objects.create(invitation=invite, group=group)
    user_group.user = user_registered(email)
    user_group.save()

# checks if user is registered in db
# @return user object if it exists
def user_registered(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None
