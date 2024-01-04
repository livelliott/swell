from itertools import chain
from django.contrib.auth.models import User
from envelope.models import Envelope
from question.models import Answer, DefaultQuestionEnvelope
from .models import UserGroup
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def get_envelope_members(envelope):
    users = {}
    members = UserGroup.objects.filter(envelope=envelope)
    for member in members:
        users[member.display_name] = member.user.email
    return users

# retrieves all questions associated with envelope
# @return [dictionary] - {all questions, corresponding ids}
def get_envelope_questions(envelope):
    questions_default = DefaultQuestionEnvelope.objects.filter(envelope_id=envelope.envelope_id)
    questions_user = envelope.questions_user.all()
    all_questions = list(chain(questions_default, questions_user))
    question_ids = [ str(q.id) for q in all_questions ]
    return { 'questions': all_questions, 'answers': question_ids }

# all_questions = get_envelope_questions(envelope)['questions']
def get_all_question_answers(all_questions):
    all_answers = {}
    # for each question
    for question in all_questions:
        # get all of the answers for it
        empty_answers = Answer.objects.filter(question=question, user_answer='')
        empty_answers.delete()
        all_answers[question] = Answer.objects.filter(question=question)
    return all_answers
