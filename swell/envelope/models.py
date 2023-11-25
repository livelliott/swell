from django.db import models
from django.contrib.auth.models import User

# created by a user, sent to other users
class Envelope(models.Model):
    envelope_id = models.AutoField(primary_key=True)
    envelope_name = models.CharField(max_length=200)
    envelope_members = models.ManyToManyField(User, related_name='user_envelopes')
    # questions in envelope
    # due date of envelope