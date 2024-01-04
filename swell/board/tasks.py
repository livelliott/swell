from celery import shared_task
from datetime import datetime, timedelta
from django.utils import timezone
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
    # Schedule the task to run at the specified time
    # send_envelope_email_task.apply_async(args=[envelope_id], eta=scheduled_time)
    send_envelope_email_task.apply_async(args=[envelope_id], eta=(timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date())