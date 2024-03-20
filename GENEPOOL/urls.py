"""GENEPOOL URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from app_genepool import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view() , name ='home-page'), # FIND INDEX CLASS AND CONVERT TO A GLORIFED VIEW FUNCTION USING .as_view , name is used for reverse URL lookup, in html doc for example
    path('products-and-services/', views.ProductsAndServices.as_view(), name ='products_and_services') ,
    path('accounts/', include('allauth.urls')),
    path('client-page/', views.StaffPage.as_view(), name='staff-page'),
    path('submit-authorised-ticket-request/', views.submit_authorised_ticket_request, name='submit_authorised_ticket_request'),
    path('edit-quote-request/<int:quote_id>/', views.EditQuoteRequest.as_view(), name='edit-quote-request'),
    path('delete-quote-request/<int:quote_id>/', views.DeleteQuoteRequest.as_view(), name='delete-quote-request'),
    path('edit-callback-request/<int:callback_request_id>/', views.EditCallBackRequest.as_view(), name='edit-callback-request'),
    path('delete-callback-request/<int:callback_request_id>/', views.DeleteCallBackRequest.as_view(), name='delete-callback-request'),
    path('close-ticket/<int:ticket_id>/', views.CloseTicketForClientPage.as_view(), name='close-client-ticket'),
    path('delete-ticket/<int:ticket_id>/', views.DeleteTicketForClientPage.as_view(), name='delete-ticket'),
    path('edit-ticket/<int:ticket_id>/', views.EditTicketForClientPage.as_view(), name='edit-ticket'),
    path('view-ticket/<int:ticket_id>/', views.ViewTicketForClientPage.as_view(), name='view-ticket'),
    path('re-open-ticket/<int:ticket_id>/', views.ReopenTicket.as_view(), name='re-open-ticket'),
]
