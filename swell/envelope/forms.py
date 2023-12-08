from django import forms
# from board.models import Invitation, Group, UserGroup
from .models import Envelope

class EnvelopeForm(forms.ModelForm):
    class Meta:
        model = Envelope
        fields = ["envelope_name", "envelope_query_date", "envelope_due_date"]
        widgets = {
            'envelope_query_date': forms.DateInput(attrs={'type': 'date'}),
            'envelope_due_date': forms.DateInput(attrs={'type': 'date'}),
        }
    invitee_emails = forms.CharField(max_length=1000, required=True)