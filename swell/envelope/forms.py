from django import forms
# from board.models import Invitation, Group, UserGroup
from .models import Envelope

class EnvelopeForm(forms.ModelForm):
    class Meta:
        model = Envelope
        fields = ["envelope_name", "envelope_query_datetime"]
        widgets = {
            'envelope_due_datetime': forms.DateInput(attrs={'type': 'date'}),
        }
    invitee_emails = forms.CharField(max_length=1000, required=True)