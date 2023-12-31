from django.http import HttpResponseServerError
from django.shortcuts import render, redirect, reverse
from .models import UserGroup
from envelope.models import Envelope
from question.models import Answer, BaseQuestion, UserQuestion
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
        context = {
            'envelope_id': envelope_id,
            'envelope': envelope,
            'user': user,
            'prev_answers': prev_answers,
            'started': started,
        }
        if request.method == 'POST' and envelope_member(user, envelope_id):
            # if question period commenced
            if started:
                for a in answers:
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
                    return redirect(reverse('board:board_home'))
            else:
                # get user to suggest questions
                if len(UserQuestion.objects.filter(user=user, envelope=envelope)) < 2:
                    user_question = request.POST.get('user_question')
                    question = UserQuestion(content=user_question, user=user)
                    question.save()
                    envelope.questions_user.add(question)
                    envelope.save()
                    messages.success(request, "Submitted.")
                    return redirect(reverse('board:board_home'))
                else:
                    messages.success(request, "You may only submit two prompts per envelope.")
                    return redirect(reverse('board:board_home'))
        else:
            return render(request, 'envelope.html', context)
    except ObjectDoesNotExist:
        messages.success(request, "You do not have permission to view this page.")
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

# returns a list envelopes the user has joined
def get_joined_envelopes(request):
    joined_envelopes = []
    user_groups = UserGroup.objects.filter(user=request.user)
    for user_group in user_groups:
        joined_envelopes.append(user_group.envelope)
    return joined_envelopes

def envelope_started(envelope):
    today = timezone.localdate()
    start_date = (envelope.envelope_query_date - today).days
    if start_date > 0:
        return False
    else:
        return True

# retrieves all questions associated with envelope
# @return [dictionary] - {all questions, corresponding ids}
def get_envelope_questions(envelope):
    questions_user = envelope.questions_user.all()
    questions_default = envelope.questions_default.all()
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
