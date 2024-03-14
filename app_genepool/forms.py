from django import forms
from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests
from .models import AuthorisedQuoteRequests
from .models import AuthorisedTicketRequests
from .models import ChatDialogue
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

class AuthorisedQuoteRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AuthorisedQuoteRequestForm, self).__init__(*args, **kwargs)
        
        if not user.is_staff:
            readonly_fields = ['full_nameORcompany_name', 'email', 'phone', 'status']
            for field_name in readonly_fields:
                self.fields[field_name].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = AuthorisedQuoteRequests
        fields = ['full_nameORcompany_name', 'email', 'phone', 'service', 'request_description', 'status']

class AuthorisedTicketRequestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AuthorisedTicketRequestForm, self).__init__(*args, **kwargs)
        
        if user and not user.is_staff:
            readonly_fields = ['full_nameORcompany_name']
            for field_name in readonly_fields:
                self.fields[field_name].widget.attrs['readonly'] = 'readonly'

    class Meta:
        model = AuthorisedTicketRequests
        fields = ['full_nameORcompany_name','request_description',]

class ChatDialogue1(forms.ModelForm):
    class Meta:
        model=ChatDialogue 
        fields = ['message','file']

