from django.contrib import admin
from .models import Invitation, UserGroup

# Register your models here.
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('envelope_id', 'sender','recipient')


class UserGroupAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_name','env_id')

admin.site.register(Invitation, InvitationAdmin)
admin.site.register(UserGroup, UserGroupAdmin)