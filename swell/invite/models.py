from django.db import models
from django.contrib.auth.models import User

class Invite(models.Model):
    email = models.EmailField(unique=True)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    expiration_date = models.DateTimeField()
    confirmation_key = models.CharField(max_length=64, unique=True)
    is_confirmed = models.BooleanField(default=False)

    def send_invitation(self, request):
        # Logic to send the actual invitation, including the invitation content.
        pass