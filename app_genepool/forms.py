from django import forms
from .models import UnauthorisedQuoteRequests

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = UnauthorisedQuoteRequests
        fields = ['full_nameORcompany_name', 'email', 'phone', 'service']