from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from question.models import DefaultQuestion, AdminQuestion, UserQuestion, Answer

# created by a user, sent to other users
class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    envelope_query_date = models.DateField(default=(timezone.now() + timezone.timedelta(days=2)).astimezone(timezone.get_current_timezone()).date(), null=True)
    envelope_frequency = models.IntegerField()
    envelope_due_date = models.DateField(blank=True, null=True)
    envelope_issue = models.IntegerField(default=1)
    questions_default = models.ManyToManyField(DefaultQuestion, blank=True)
    questions_admin = models.ManyToManyField(AdminQuestion, blank=True)
    questions_user = models.ManyToManyField(UserQuestion, blank=True)
    user_answers = models.ManyToManyField(Answer, blank=True)
    @property
    def delivery_date(self):
        today = timezone.localdate()
        start_date = (self.envelope_query_date - today).days
        remaining_days = max(0, (self.envelope_due_date - today).days)
        if start_date == 1:
            return f"Starts tomorrow"
        elif start_date > 1:
            return f"Starts in {start_date} days"
        elif remaining_days == 0:
            return "Delivers today"
        elif remaining_days == 1:
            return "Delivers tomorrow"
        else:
            return f"Delivers in {remaining_days} days"