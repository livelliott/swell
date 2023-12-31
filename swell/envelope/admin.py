from django.contrib import admin
from django.utils.html import format_html
from .models import Envelope

class EnvelopeAdmin(admin.ModelAdmin):
    list_display = ('envelope_name', 'envelope_admin', 'delivery_date')
    readonly_fields = ('display_user_questions',)

    def get_user_questions_display(self, obj):
        return ', '.join(question.content for question in obj.questions_user.all())

    get_user_questions_display.short_description = 'User Questions'

    def display_user_questions(self, obj):
        # Create an HTML representation of the User Questions
        return format_html('<br>'.join(question.content for question in obj.questions_user.all()))

    display_user_questions.short_description = 'User Questions (Content)'

    # Override the change_view method to customize the detail view
    def change_view(self, request, object_id, form_url='', extra_context=None):
        # Add custom logic or context for the change view
        extra_context = extra_context or {}
        extra_context['show_user_questions'] = True  # Flag to determine whether to show user questions

        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_fields(self, request, obj=None):
        # Override get_fields to conditionally include the display_user_questions field
        fields = super().get_fields(request, obj)
        show_user_questions = request.GET.get('show_user_questions', False)
        if show_user_questions:
            fields += ('display_user_questions',)
        return fields
    
admin.site.register(Envelope, EnvelopeAdmin)