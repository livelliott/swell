from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from question.models import DefaultQuestionEnvelope, UserQuestion, Answer

# created by a user, sent to other users
class DateManager(models.Model):
    # changes query date for next issue
    change_query_date = models.CharField(max_length=50, blank=True, null=True)
    # changes due date for next issue
    change_due_date = models.CharField(max_length=50, blank=True, null=True)
    # changes issue number
    change_issue_number = models.CharField(max_length=50, blank=True, null=True)
    # # email users when questions are released
    # email_query_date = models.CharField(max_length=50, blank=True, null=True)
    # # email users when issue is published
    # email_due_date = models.CharField(max_length=50, blank=True, null=True)
    # # email reminder for admin to create the next issue (sent two days before next envelope start date)
    # email_admin_next_issue = models.CharField(max_length=50, blank=True, null=True)

class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    envelope_query_date = models.DateField(default=(timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date(), null=True)
    envelope_frequency = models.IntegerField()
    envelope_due_date = models.DateField(blank=True, null=True)
    envelope_issue = models.IntegerField(default=1)
    questions_default = models.ManyToManyField(DefaultQuestionEnvelope, blank=True)
    questions_user = models.ManyToManyField(UserQuestion, blank=True)
    user_answers = models.ManyToManyField(Answer, blank=True)
    date_manager = models.ForeignKey(DateManager, on_delete=models.CASCADE, null=True)
    def get_user_questions_display(self):
        return ', '.join(question.content for question in self.questions_user.all())
    get_user_questions_display.short_description = 'User Questions'
    # create date manager instance when envelope is created
    def save(self, *args, **kwargs):
        if not self.date_manager:
            date_manager = DateManager.objects.create()
            self.date_manager = date_manager
        super().save(*args, **kwargs)
    @property
    def delivery_date(self):
        today = timezone.localdate()
        start_date = (self.envelope_query_date - today).days
        remaining_days = (self.envelope_due_date - today).days
        if start_date == 1:
            return f"Starts tomorrow"
        elif start_date > 1:
            return f"Starts in {start_date} days"
        elif remaining_days < 0:
            return "Delivered, view now"
        elif remaining_days == 0:
            return "Delivers today"
        elif remaining_days == 1:
            return "Delivers tomorrow"
        else:
            return f"Delivers in {remaining_days} days"

