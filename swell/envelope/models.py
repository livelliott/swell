from django.db import models
from django.contrib.auth.models import User
from board.models import Group
from django.utils import timezone

# created by a user, sent to other users
class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_admin = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    envelope_query_date = models.DateField(default=(timezone.now() + timezone.timedelta(days=2)).date(), null=True)
    envelope_due_date = models.DateField(blank=True, null=True)
    # questions in envelope TBD...