from django.core.serializers.json import DjangoJSONEncoder
from itertools import chain
from django.forms import model_to_dict
from datetime import date
import json
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from board.models import Invitation, UserGroup
from question.models import DefaultQuestion, AdminQuestion
from django.contrib.auth.models import User
from swell.constants import EMAIL_PATTERN
from envelope.models import Envelope
from .forms import EnvelopeForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone
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
            # save form data in session
            request.session['envelope_data'] = json.dumps(model_to_dict(envelope_form), cls=CustomJSONEncoder)
            return redirect('envelope:envelope_create_prompts')
    else:
        form = EnvelopeForm()
    return render(request, 'envelope_create.html', {'form': form})

def envelope_create_prompts(request):
    # retrieve saved form data from session
    envelope_data = request.session.get('envelope_data')
    if not envelope_data:
        # redirect back to the first page if session data is missing
        messages.error(request, 'Please complete the previous step.')
        return redirect('envelope:envelope_create')

    all_default_questions = DefaultQuestion.objects.all()
    envelope_query_date = (timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date()
    context = {
        'questions': all_default_questions,
    }

    if request.method == "POST":
        data = json.loads(envelope_data)
        envelope_frequency = data['envelope_frequency']
        questions_str = request.POST.get('checked_question_ids')
        questions = [int(q) for q in questions_str.split(',') if q.isdigit()]
        # Print or log form data for verification
        print(f"Envelope Data: {data}")
        print(f"Envelope Frequency: {envelope_frequency}")
        print(f"Questions: {questions}")

        # Convert envelope_data back to a dictionary
        envelope = Envelope(
            envelope_name=data['envelope_name'],
            envelope_admin=request.user,
            envelope_frequency=envelope_frequency,
            envelope_due_date=(envelope_query_date + timedelta(days=envelope_frequency)).strftime("%Y-%m-%d")
        )
        envelope.save()
        default_questions(envelope, questions)
        messages.success(request, f"{questions}.")
        return redirect('envelope:envelope_create_success')

    return render(request, 'envelope_create_prompts.html', context)

# retrieves all questions associated with envelope
# @return [dictionary] - {all questions, corresponding ids}
def get_envelope_questions(envelope):
    questions_admin = envelope.questions_admin.all()
    questions_user = envelope.questions_user.all()
    questions_default = envelope.questions_default.all()
    all_questions = list(chain(questions_admin, questions_user, questions_default))
    question_ids = [ str(q.id) for q in all_questions ]
    return { 'questions': all_questions, 'answers': question_ids }

# displays envelope creation success screen
@login_required
def envelope_create_success(request):
    return render(request, 'envelope_create_success.html')

# adds all default questions to envelope
# can be disabled by admin
def default_questions(envelope, questions):
    for question_id in questions:
        question = DefaultQuestion.objects.get(id=question_id)
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
    
class CustomJSONEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        return super().default(obj)
