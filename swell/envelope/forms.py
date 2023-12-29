from django import forms
from .models import Envelope
from django.utils import timezone
from swell.constants import TWO_WEEKS, ONE_MONTH, TWO_MONTHS, SIX_MONTHS

class EnvelopeForm(forms.ModelForm):
    current_date = timezone.localdate()
    FREQUENCY = [
        (TWO_WEEKS, 'Twice a Month'),
        (ONE_MONTH, 'Once a Month'),
        (TWO_MONTHS, 'Once Every Two Months'),
        (SIX_MONTHS, 'Once Every Three Months'),
    ]
    admin_display_name = forms.CharField(max_length=50, required=True)
    envelope_frequency = forms.ChoiceField(choices=FREQUENCY, required=False)
    class Meta:
        model = Envelope
        fields = ["envelope_name", "admin_display_name", "envelope_frequency"]
        labels = {
            'envelope_name': 'Choose an Envelope name',
            'admin_display_name': 'User display name',
            'envelope_frequency': 'Custom Label 3',
        }
    