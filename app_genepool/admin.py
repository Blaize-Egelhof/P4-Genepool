from django.contrib import admin

from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests
from .models import AuthorisedQuoteRequests


admin.site.register(UnauthorisedQuoteRequests)
admin.site.register(UnauthorisedCallBackRequests)
admin.site.register(AuthorisedQuoteRequests)

