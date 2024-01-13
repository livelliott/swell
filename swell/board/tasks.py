from datetime import datetime, timedelta, time
from django.utils import timezone
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import UserGroup
from envelope.models import Envelope
from .utils import get_all_question_answers, get_envelope_members, get_envelope_questions

@shared_task
def send_envelope_email_task(envelope_id):
    try:
        envelope = Envelope.objects.get(envelope_id=envelope_id)
        members = get_envelope_members(envelope)
        user_emails = [user_group for name, user_group in members.items()]
        print(f"Members email: {user_emails}")
        questions = get_envelope_questions(envelope)['questions']
        question_answers = get_all_question_answers(questions)
        published = envelope.envelope_due_date.strftime("%B %d, %Y")
        subject = f"Issue #{envelope.envelope_issue}: {envelope.envelope_name}"
        html_message = render_to_string('envelope_email.html', {'envelope': envelope, 'members': members, 'question_answers': question_answers, 'published': published})

        send_mail(
            subject=subject,
            message='test',
            from_email='swellapp.info@gmail.com',
            recipient_list=user_emails,
            html_message=html_message,
        )
    except Envelope.DoesNotExist:
        # Handle the case where the envelope is not found
        print("Could not find envelope.")

@shared_task
def schedule_send_envelope_email(envelope_id, scheduled_time):
    # schedule task to run at specified time
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    task = send_envelope_email_task.apply_async(args=[envelope_id], eta=scheduled_time)
    envelope.celery_task_id = task.id
    envelope.save()

@shared_task
def update_envelope_query_date(envelope_id):
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    # new query date two days after envelope updated
    envelope.envelope_query_date = (timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date()
    envelope.save()
    # # updates issue number
    # envelope.envelope_issue = envelope.envelope_issue + 1

@shared_task
def update_envelope_due_date(envelope_id):
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    # new due date x days after query date: x = envelope_frequency
    envelope.envelope_due_date = envelope.envelope_query_date + timedelta(days=envelope.envelope_frequency)
    envelope.save()

@shared_task
def update_envelope_issue_number(envelope_id):
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    envelope.envelope_issue = envelope.envelope_issue + 1
    envelope.save()

@shared_task
def update_envelope_task(envelope_id, scheduled_time):
    envelope = Envelope.objects.get(envelope_id=envelope_id)
    # access date manager to store scheduled tasks
    date_manager = envelope.date_manager
    # Schedule tasks and store the task instances in the DateManager
    date_manager.change_query_date = update_envelope_query_date.apply_async(args=[envelope_id], eta=scheduled_time)
    date_manager.change_due_date = update_envelope_due_date.apply_async(args=[envelope_id], eta=scheduled_time)
    date_manager.change_issue_number = update_envelope_issue_number.apply_async(args=[envelope_id], eta=scheduled_time)
    date_manager.save()
