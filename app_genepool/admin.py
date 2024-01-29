from django.contrib import admin

from .models import UnauthorisedQuoteRequests
from .models import UnauthorisedCallBackRequests


admin.site.register(UnauthorisedQuoteRequests)
admin.site.register(UnauthorisedCallBackRequests)
