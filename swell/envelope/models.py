from django.db import models
from django.contrib.auth.models import User
from board.models import Invitation, Group, UserGroup
from django.utils import timezone
from datetime import datetime, time

# created by a user, sent to other users
class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_members = models.ManyToManyField(Group)
    envelope_query_datetime = models.DateTimeField(default=datetime.combine(timezone.now().date() + timezone.timedelta(days=2), time(12, 0)))
    # due date of envelope for publishing
    envelope_due_datetime = models.DateTimeField(blank=True, null=True)
    # questions in envelope TBD...