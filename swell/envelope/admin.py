from django.contrib import admin
from .models import Envelope

class EnvelopeAdmin(admin.ModelAdmin):
    list_display = ('envelope_name', 'envelope_id')

admin.site.register(Envelope, EnvelopeAdmin)