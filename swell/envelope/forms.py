from django import forms
# from board.models import Invitation, Group, UserGroup
from .models import Envelope
from datetime import datetime, timedelta

class EnvelopeForm(forms.ModelForm):
    current_date = datetime.now()
    DUE_DATE_CHOICES = [
        ((current_date + timedelta(days=14)).strftime("%Y-%m-%d"), 'Every two weeks'),
        ((current_date + timedelta(days=30)).strftime("%Y-%m-%d"), 'Every month'),
        ((current_date + timedelta(days=60)).strftime("%Y-%m-%d"), 'Every two months'),
        ((current_date + timedelta(days=180)).strftime("%Y-%m-%d"), 'Every six months'),
    ]
    envelope_due_date = forms.ChoiceField(choices=DUE_DATE_CHOICES, required=False)
    class Meta:
        model = Envelope
        fields = ["envelope_name", "envelope_query_date", "envelope_due_date"]
        widgets = {
            'envelope_query_date': forms.DateInput(attrs={'type': 'date'}),
        }
    members = forms.CharField(max_length=1000, required=True)