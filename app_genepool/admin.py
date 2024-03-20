from django.contrib import admin

from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests
from .models import AuthorisedTicketRequests
from .models import ChatDialogue

admin.site.register(UnauthorisedQuoteRequests)
admin.site.register(UnauthorisedCallBackRequests)
admin.site.register(AuthorisedTicketRequests)
admin.site.register(ChatDialogue)
