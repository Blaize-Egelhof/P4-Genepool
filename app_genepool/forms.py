from django import forms
from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests
from django.contrib.auth.forms import AuthenticationForm

class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = UnauthorisedQuoteRequests
        fields = ['id','full_nameORcompany_name','email','phone','service','request_description','status']
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class CallBackForm(forms.ModelForm):
    class Meta:
        model = UnauthorisedCallBackRequests
        fields = ['id','full_nameORcompany_name','email','phone','service','request_description','status']
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'request_description': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


