from django.contrib.auth.models import User
from django.db import models
import uuid

# a single instance of an invitation
class Invitation(models.Model):
    envelope_id = models.IntegerField()
    email = models.EmailField(null=True, blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations')
    invite_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations', editable=True, blank=True, null=True)

# represents a single user's relationship to a specific group
# user in multiple groups >> multiple UserGroup instances
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=50, default=None, null=True)
    # invitation associated with the user and group
    envelope = models.ForeignKey('envelope.Envelope', on_delete=models.CASCADE)
    env_id = models.IntegerField()
