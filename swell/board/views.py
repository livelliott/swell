from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, reverse
from .models import UserGroup
from envelope.models import Envelope
from question.models import Answer, BaseQuestion, UserQuestion, DefaultQuestionEnvelope
from itertools import chain
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from envelope.views import valid_invite, send_invite
from django.utils import timezone

@login_required
def home_page(request):
    user = request.user
    created_envelopes = Envelope.objects.filter(envelope_admin=user)
    joined_envelopes = get_joined_envelopes(request)
    all_envelopes =  set(chain(created_envelopes, joined_envelopes))
    sorted_envelopes = sorted(all_envelopes, key=lambda x: x.envelope_due_date)
    context = {
        'user': user,
        'all_envelopes': sorted_envelopes,
    }
    return render(request, 'home.html', context)

@login_required
def envelope(request, envelope_id):
    user = request.user
    try:
        user_group = UserGroup.objects.get(user=user, env_id=envelope_id)
        envelope = user_group.envelope
        questions = get_envelope_questions(envelope)['questions']
        prev_answers = get_previous_answers(envelope, user, questions)
        answers = get_envelope_questions(envelope)['answers']
        started = envelope_started(envelope)
        ended = envelope_ended(envelope)
        published = envelope.envelope_due_date.strftime("%B %d, %Y")
        members = get_envelope_members(envelope)
        context = {
            'envelope_id': envelope_id,
            'envelope': envelope,
            'user': user,
            'prev_answers': prev_answers,
            'started': started,
            'ended': ended,
            'published': published,
            'members': members,
        }
        if request.method == 'POST' and envelope_member(user, envelope_id):
            # if question period has begun
            if started:
                # for each question-answer pair
                for a in answers:
                    # if admin enabled question
                    question = BaseQuestion.objects.get(id=a) 
                    if question.is_enabled:
                        # answer name == question.id
                        user_answer = request.POST.get(a)
                        # if question was answered
                        if not user_answer.isspace():
                            question = BaseQuestion.objects.get(id=a)
                            answered = Answer.objects.filter(envelope=envelope, user=user, question=question).first()
                            # if user has answered this question already
                            if answered:
                                # modify the question
                                answered.user_answer = user_answer
                                answered.save()
                            else:
                                # else create it 
                                answer = Answer(user=request.user, question=question, user_answer=user_answer)
                                answer.save()
                                envelope.user_answers.add(answer)
                messages.success(request, f"Saved answers for {envelope.envelope_name}.")
                return redirect('board:board_envelope', envelope_id=envelope_id)
            else:
                # get user to suggest questions
                if len(UserQuestion.objects.filter(user=user, envelope=envelope)) < 2:
                    user_question = request.POST.get('user_question')
                    question = UserQuestion(content=user_question, user=user, display_name=user_group.display_name)
                    question.save()
                    envelope.questions_user.add(question)
                    envelope.save()
                    messages.success(request, "Submitted prompts.")
                    return redirect('board:board_envelope', envelope_id=envelope_id)
                else:
                    messages.error(request, "You may only submit two prompts per envelope.")
                    return redirect('board:board_envelope', envelope_id=envelope_id)
        return render(request, 'envelope.html', context)
    except ObjectDoesNotExist:
        messages.error(request, "You do not have permission to view this page.")
        return render(request, 'home.html')
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred. Please try again later.")

@login_required
def envelope_members(request, envelope_id):
    user = request.user
    try:
        # retrieve all of the users in the envelope
        envelope = Envelope.objects.get(envelope_id=envelope_id)
        envelope_admin = envelope.envelope_admin
        envelope_users = UserGroup.objects.filter(envelope=envelope)
        context = {
            'user': user,
            'envelope_admin': envelope_admin,
            'envelope': envelope,
            'envelope_users': envelope_users,
        }
        # if the admin clicks the 'add user' button
        if request.method == 'POST' and user == envelope_admin:
            # allow admin to invite users to the envelope
            invite_email = request.POST.get('user_email')
            if valid_invite(invite_email) != None:
              send_invite(request, envelope_id, invite_email)
              messages.success(request, f"Invite sent to {invite_email}")       
        return render(request, 'envelope_members.html', context)
    except Exception as e:
        print(f"An error occurred: {e}")
        return HttpResponseServerError("An error occurred. Please try again later.")

@login_required
def envelope_admin(request, envelope_id):
    user = request.user
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    envelope_admin = envelope.envelope_admin
    questions_user = envelope.questions_user.all()
    questions_user_checked = get_enabled_questions(questions_user)
    questions_default = DefaultQuestionEnvelope.objects.filter(envelope_id=envelope_id)
    questions_default_checked = get_enabled_questions(questions_default)
    display_name = UserGroup.objects.get(envelope=envelope, user=user)
    started = envelope_started(envelope)
    context = {
        'user': user,
        'display_name': display_name.display_name,
        'started': started,
        'envelope_admin': envelope_admin,
        'envelope': envelope,
        'questions_user': questions_user,
        'questions_user_checked': questions_user_checked,
        'questions_default': questions_default,
        'questions_default_checked': questions_default_checked,
    }
    # if admin saves questions
    if request.method == 'POST' and user == envelope_admin:
        envelope_name = request.POST.get('envelope_name')
        user_display_name = request.POST.get('display_name')
        # change envelope name if modified
        if envelope_name != envelope.envelope_name:
            envelope.envelope_name = envelope_name
            envelope.save()
        if display_name.display_name != user_display_name:
            display_name.display_name = user_display_name
            display_name.save()
        user_questions_checked = request.POST.get('checked_user_question_ids')
        modify_questions_checked(questions_user, user_questions_checked)
        default_questions_checked = request.POST.get('checked_default_question_ids')
        modify_questions_checked(questions_default, default_questions_checked)
        messages.success(request, f"Successfully modified {envelope.envelope_name}.")
        return redirect('board:board_envelope_admin', envelope_id=envelope_id)
    elif request.method == 'POST':
        user_display_name = request.POST.get('display_name')
        if display_name.display_name != user_display_name:
            display_name.display_name = user_display_name
            display_name.save()
            messages.success(request, f"Successfully changed display name to {user_display_name}.")
            return redirect('board:board_envelope_admin', envelope_id=envelope_id)
    return render(request, 'envelope_admin.html', context)

def modify_questions_checked(all_questions, questions_checked):
    questions_checked_list = [int(q_id) for q_id in questions_checked.split(',') if q_id.isdigit()]
    for q in all_questions:
        # if question in should be enabled
        if q.id in questions_checked_list:
            # enable question
            q.is_enabled = True
            q.save()
        # question should be disabled
        else:
            q.is_enabled = False
            q.save()

# returns a list envelopes the user has joined
def get_joined_envelopes(request):
    joined_envelopes = []
    user_groups = UserGroup.objects.filter(user=request.user)
    for user_group in user_groups:
        joined_envelopes.append(user_group.envelope)
    return joined_envelopes

def get_enabled_questions(questions):
    checked_question_ids = []
    for q in questions:
        if q.is_enabled:
            checked_question_ids.append(q.id)
    return checked_question_ids

def envelope_started(envelope):
    today = timezone.localdate()
    start_date = (envelope.envelope_query_date - today).days
    if start_date > 0:
        return False
    return True

def envelope_ended(envelope):
    today = timezone.localdate()
    if envelope.envelope_due_date <= today:
        return True
    return False

def get_envelope_members(envelope):
    users = {}
    members = UserGroup.objects.filter(envelope=envelope)
    for member in members:
        users[member.display_name] = member.user
    return users

# retrieves all questions associated with envelope
# @return [dictionary] - {all questions, corresponding ids}
def get_envelope_questions(envelope):
    questions_user = envelope.questions_user.all()
    questions_default = DefaultQuestionEnvelope.objects.filter(envelope_id=envelope.envelope_id)
    all_questions = list(chain(questions_user, questions_default))
    question_ids = [ str(q.id) for q in all_questions ]
    return { 'questions': all_questions, 'answers': question_ids }

# retrieves questions and previous answers if they exist
# @return [dictionary] - question: previous answer
def get_previous_answers(envelope, user, questions):
    prev_answers = {}
    for question in questions:
        answered = Answer.objects.filter(envelope=envelope, user=user, question=question).first()
        # if the question was answered previously
        if answered:
            prev_answers[question] = answered.user_answer
        else:
            prev_answers[question] = ''
    return prev_answers

# checks if the user is a member of the envelope
# @return [boolean] - if a member
def envelope_member(user, envelope_id):
    try:
        UserGroup.objects.get(user=user, env_id=envelope_id)
        return True
    except ObjectDoesNotExist:
        return False
