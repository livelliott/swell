from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board.models import Invitation, UserGroup
from question.models import DefaultQuestion, AdminQuestion
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
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
            admin_display_name = form.cleaned_data['admin_display_name']
            envelope_form.envelope_admin = request.user
            envelope_form.save()
            default_questions(envelope_form)
            # create corresponding user group instance
            envelope_id = envelope_form.envelope_id
            user_group = UserGroup(user=request.user, display_name=admin_display_name, envelope=envelope_form, env_id=envelope_id)
            user_group.save()
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

# adds all default questions to envelope
# can be disabled by admin
def default_questions(envelope):
    all_default_questions = DefaultQuestion.objects.all()
    for question in all_default_questions:
        envelope.questions_default.add(question)
    envelope.save()

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
    invite = Invitation(envelope_id=envelope_id, email=email, sender=request.user)
    invite.save()
    custom_link = f"http://{os.getenv('HOST_DOMAIN')}/accept-invite/{invite.invite_token}"
    send_mail(subject="Invite to Swell",
              message=f"Invite link: {custom_link}",
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              html_message=None)