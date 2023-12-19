from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# created by a user, sent to other users
class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    envelope_query_date = models.DateField(default=(timezone.now() + timezone.timedelta(days=2)).date(), null=True)
    envelope_due_date = models.DateField(blank=True, null=True)
    # questions in envelope TBD...
    @property
    def delivery_date(self):
        if self.envelope_due_date:
            today = timezone.now().date()
            remaining_days = max(0, (self.envelope_due_date - today).days)
            if remaining_days == 0:
                return "Delivers today"
            elif remaining_days == 1:
                return "Delivers tomorrow"
            else:
                return f"Delivers in {remaining_days} days"
        return None