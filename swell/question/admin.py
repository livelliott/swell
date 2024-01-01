from django.contrib import admin
from .models import BaseQuestion, DefaultQuestion, DefaultQuestionEnvelope, UserQuestion, Answer

@admin.register(BaseQuestion)
class BaseQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'id', 'is_enabled')

@admin.register(DefaultQuestion)
class DefaultQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_enabled')

@admin.register(DefaultQuestionEnvelope)
class DefaultQuestionEnvelopeAdmin(admin.ModelAdmin):
    list_display = ('content', 'is_enabled')

@admin.register(UserQuestion)
class UserQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'user', 'is_enabled')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'user_answer')