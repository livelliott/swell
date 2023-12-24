from django import forms
# from board.models import Invitation, Group, UserGroup
from .models import Envelope
from django.utils import timezone
from swell.constants import TWO_WEEKS, ONE_MONTH, TWO_MONTHS, SIX_MONTHS

class EnvelopeForm(forms.ModelForm):
    current_date = timezone.localdate()
    FREQUENCY = [
        (TWO_WEEKS, 'Every two weeks'),
        (ONE_MONTH, 'Every month'),
        (TWO_MONTHS, 'Every two months'),
        (SIX_MONTHS, 'Every six months'),
    ]
    envelope_frequency = forms.ChoiceField(choices=FREQUENCY, required=False)
    class Meta:
        model = Envelope
        fields = ["envelope_name", "envelope_query_date", "envelope_frequency"]
        widgets = {
            'envelope_query_date': forms.DateInput(attrs={'type': 'date'}),
        }
    admin_display_name = forms.CharField(max_length=50, required=True)
    members = forms.CharField(max_length=1000, required=True)