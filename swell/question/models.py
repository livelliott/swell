from django.db import models
from django.contrib.auth.models import User

# Admin decides if questions are included in the newsletter
class BaseQuestion(models.Model):
    content = models.CharField(max_length=400)
    is_enabled = models.BooleanField(default=False)

class DefaultQuestion(BaseQuestion):
    pass

class DefaultQuestionEnvelope(BaseQuestion):
    envelope_id = models.IntegerField()
    default_id = models.IntegerField()

class UserQuestion(BaseQuestion):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    display_name = models.CharField(max_length=50, null=True)

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    question = models.ForeignKey(BaseQuestion, on_delete=models.CASCADE, null=True)
    user_answer = models.CharField(max_length=2000)