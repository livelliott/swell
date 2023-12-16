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
    is_accepted = models.BooleanField(default=False)

# an instance of a group >> initialized when an envelope is created
class Group(models.Model):
    envelope = models.ForeignKey('envelope.Envelope', on_delete=models.CASCADE)
    # invitations associated with the group
    group_invitations = models.ManyToManyField('Invitation', through='board.UserGroup')

# represents a single user's relationship to a specific group
# user in multiple groups >> multiple UserGroup instances
class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=50, default=None, null=True)
    # invitation associated with the user and group
    invitation = models.ForeignKey('Invitation', on_delete=models.CASCADE)

# A Group can be associated with multiple invitations through the UserGroup model.
# A User can be associated with multiple groups through the UserGroup model.
# An Invitation is associated with a sender, a recipient, and optionally a group through the UserGroup model.
# The acceptance status of an invitation is tracked through the is_accepted field in the UserGroup and Invitation models.
