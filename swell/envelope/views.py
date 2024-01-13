from django.core.serializers.json import DjangoJSONEncoder
from itertools import chain
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from question.models import DefaultQuestion, DefaultQuestionEnvelope, UserQuestion
from board.models import Invitation, UserGroup
from board.tasks import schedule_send_envelope_email, update_envelope_task
from envelope.models import Envelope
from .forms import EnvelopeForm
from swell.constants import EMAIL_PATTERN
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import datetime, time, timedelta, date
import json
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
            print("Form data:", form.cleaned_data)
            # save form data in session
            display_name = form.cleaned_data['admin_display_name']
            request.session['admin_display_name'] = display_name
            request.session['envelope_data'] = json.dumps(model_to_dict(envelope_form), cls=CustomJSONEncoder)
            return redirect('envelope:envelope_create_prompts')
    else:
        form = EnvelopeForm()
    return render(request, 'envelope_create.html', {'form': form})

@login_required
def envelope_create_prompts(request):
    # retrieve saved form data from session
    envelope_data = request.session.get('envelope_data')
    display_name = request.session.get('admin_display_name')
    if not envelope_data:
        # redirect back to the first page if session data is missing
        messages.error(request, 'Please complete the previous step.')
        return redirect('envelope:envelope_create')
    all_default_questions = DefaultQuestion.objects.all()
    envelope_query_date = (timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date()
    edit_day = envelope_query_date.strftime("%A")
    context = {
        'edit_day': edit_day,
        'questions': all_default_questions,
    }
    # if user clicks next
    if request.method == "POST":
        # get default questions that admin enables
        questions_str = request.POST.get('checked_question_ids')
        questions = [int(q) for q in questions_str.split(',') if q.isdigit()]
        # get custom prompts the admin created
        custom_prompts = request.POST.get('custom_prompts_input')
        if custom_prompts == '' :  prompts = [] 
        else : prompts = [prompt for prompt in custom_prompts.split(',')]
        # if no prompts have been added to the envelope
        if len(questions) > 0 or len(prompts) > 0:
            # retrieve data from current and previous page
            data = json.loads(envelope_data)
            envelope_frequency = data['envelope_frequency']
            envelope_due_date = (envelope_query_date + timedelta(days=envelope_frequency)).strftime("%Y-%m-%d")
            # create envelope instance
            envelope = Envelope(
                envelope_name=data['envelope_name'],
                envelope_admin=request.user,
                envelope_frequency=envelope_frequency,
                envelope_due_date=envelope_due_date)
            envelope.save()
            # create corresponding user group for admin
            user_group = UserGroup(user=request.user, display_name=display_name, envelope=envelope, env_id=envelope.envelope_id)
            user_group.save()
            # add default + custom questions to envelope
            default_questions(envelope, questions)
            user_questions(envelope, request.user, prompts)
            # schedule email publishing date
            scheduled_time = datetime.combine(datetime.strptime(envelope_due_date, "%Y-%m-%d"), time(12, 0))
            schedule_send_envelope_email(envelope.envelope_id, scheduled_time)
            request.session['envelope_id'] = str(envelope.envelope_id)
            # schedule time to update envelope for next instance
            update_envelope_time = datetime.combine((datetime.strptime(envelope_due_date, '%Y-%m-%d').date() + timedelta(days=(envelope_frequency - 2))), time(0, 0))
            # update_envelope_time = datetime.now() + timedelta(minutes=5)
            update_envelope_task(envelope.envelope_id, update_envelope_time)
            # redirect to invite page
            messages.success(request, f"Successfully added prompts to Envelope.")
            return redirect('envelope:envelope_create_invite')
        else:
            messages.error(request, f"You need at least one prompt in your Envelope.")
            return redirect('envelope:envelope_create_prompts')
    return render(request, 'envelope_create_prompts.html', context)

@login_required
def envelope_create_invite(request):
    envelope_data = request.session.get('envelope_id')
    envelope_id = json.loads(envelope_data)
    envelope = get_object_or_404(Envelope, envelope_id=int(envelope_id))
    context = {
        'envelope': envelope,
    }
    if request.method == 'POST' and request.user == envelope.envelope_admin:
        # allow admin to invite users to the envelope
        invite_email = request.POST.get('user_email')
        if valid_invite(invite_email) != None:
            send_invite(request, envelope_id, invite_email)
            messages.success(request, f"Invite sent to {invite_email}.")       
            return render(request, 'envelope_create_invite.html', context)
    return render(request, 'envelope_create_invite.html', context)

# retrieves all questions associated with envelope
# @return [dictionary] - {all questions, corresponding ids}
def get_envelope_questions(envelope):
    questions_user = envelope.questions_user.all()
    questions_default = DefaultQuestion.objects.all()
    all_questions = list(chain(questions_user, questions_default))
    question_ids = [ str(q.id) for q in all_questions ]
    return { 'questions': all_questions, 'answers': question_ids }

# displays envelope creation success screen
@login_required
def envelope_create_success(request):
    return render(request, 'envelope_create_success.html')

# creates copy of all existing default questions + adds to envelope
def make_copy_default_questions(envelope):
    envelope_id = envelope.envelope_id
    all_default_questions = DefaultQuestion.objects.all()
    for question in all_default_questions:
        create_question = DefaultQuestionEnvelope(content=question.content, envelope_id=envelope_id, default_id=question.id)
        create_question.save()
        envelope.questions_default.add(create_question)
    envelope.save()

# adds all default questions to envelope
# can be disabled by admin
def default_questions(envelope, questions_enabled):
    envelope_id = envelope.envelope_id
    make_copy_default_questions(envelope)
    print(f"default questions enabled: {questions_enabled}")
    if len(questions_enabled) > 0:
        # questions to be enabled by user
        for question_id in questions_enabled:
            # retrieve envelope-question instance and enable
            enable_question = envelope.questions_default.filter(envelope_id=envelope_id, default_id=question_id).first()
            enable_question.is_enabled = True
            enable_question.save()
        
# creates user questions + adds to envelope
def user_questions(envelope, user, prompts):
    if len(prompts) > 0:
        for prompt in prompts:
            user_group = UserGroup.objects.filter(user=user, envelope=envelope).first()
            create_prompt = UserQuestion(content=prompt, user=user, display_name=user_group.display_name, is_enabled=True)
            create_prompt.save()
            envelope.questions_user.add(create_prompt)
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
            messages.error(request, f"Could not send invite to {user_email}")

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