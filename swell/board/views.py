from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from .models import Invitation, Group, UserGroup
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from dotenv import load_dotenv
import os
load_dotenv()
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

def send_invite(request, envelope_id, sender, email):
    invite = Invitation.objects.create(envelope_id=envelope_id, sender=sender)
    custom_link = f"https://{os.getenv('HOST_DOMAIN')}/accept-invite/?invite_token={invite.invite_token}"
    send_mail(subject="Invite to Swell",
              message=f"Invite link: {custom_link}",
              from_email=settings.EMAIL_HOST_USER,
              recipient_list=[email],
              html_message=None)
    messages.success(request, "Invite sent to " + email)
    