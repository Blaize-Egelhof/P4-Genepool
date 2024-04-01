from django import forms
from django.forms.widgets import Textarea
from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests
from .models import AuthorisedTicketRequests
from .models import ChatDialogue
from django.contrib.auth.forms import AuthenticationForm


class QuoteRequestForm(forms.ModelForm):
    class Meta:
        model = UnauthorisedQuoteRequests
        fields = ['id', 'full_nameORcompany_name', 'email', 'phone',
                  'service', 'request_description', 'status']
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
        }


class CallBackForm(forms.ModelForm):
    class Meta:
        model = UnauthorisedCallBackRequests
        fields = [
            'id', 'full_nameORcompany_name', 'email',
            'phone', 'service', 'request_description', 'status'
        ]
        widgets = {
            'id': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone': forms.TextInput(attrs={'readonly': 'readonly'}),
            'request_description': forms.TextInput
            (attrs={'readonly': 'readonly'}),
        }


class AuthorisedTicketRequestForm(forms.ModelForm):
    class Meta:
        model = AuthorisedTicketRequests
        fields = ['full_nameORcompany_name', 'request_description','client','closed_by']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AuthorisedTicketRequestForm, self).__init__(*args, **kwargs)
        self.fields['full_nameORcompany_name'].label = 'Ticket Title'
        self.fields['request_description'].widget = forms.Textarea(attrs={'rows': 3, 'cols': 20})

        if not (user and user.groups.filter(name='Staff').exists()):
            self.fields.pop('client', None)
            self.fields.pop('closed_by', None)


class Meta:
    model = AuthorisedTicketRequests
    fields = ['full_nameORcompany_name', 'request_description']


class ChatDialogue1(forms.ModelForm):
    class Meta:
        model = ChatDialogue
        fields = ['message', 'file']
