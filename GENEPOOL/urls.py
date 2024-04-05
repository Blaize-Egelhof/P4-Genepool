from django.contrib import admin
from django.urls import path, include
from app_genepool import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Index.as_view(), name='home-page'),
    path(
        'products-and-services/',
        views.ProductsAndServices.as_view(),
        name='products_and_services'
    ),
    path('accounts/', include('allauth.urls')),
    path(
        'client-page/',
        views.StaffPage.as_view(),
        name='staff-page'
    ),
    path(
        'submit-authorised-ticket-request/',
        views.submit_authorised_ticket_request,
        name='submit_authorised_ticket_request'
    ),
    path(
        'edit-quote-request/<int:quote_id>/',
        views.EditQuoteRequest.as_view(),
        name='edit-quote-request'
    ),
    path(
        'delete-quote-request/<int:quote_id>/',
        views.DeleteQuoteRequest.as_view(),
        name='delete-quote-request'
    ),
    path(
        'edit-callback-request/<int:callback_request_id>/',
        views.EditCallBackRequest.as_view(),
        name='edit-callback-request'
    ),
    path(
        'delete-callback-request/<int:callback_request_id>/',
        views.DeleteCallBackRequest.as_view(),
        name='delete-callback-request'
    ),
    path(
        'close-ticket/<int:ticket_id>/',
        views.CloseTicketForClientPage.as_view(),
        name='close-client-ticket'
    ),
    path(
        'close-unauthorised-quote/<int:quote_id>/',
        views.CloseUnauthorisedQuote.as_view(),
        name='close-quote-object'
    ),
    path(
        'close-unauthorised-callback/<int:callback_id>/',
        views.CloseUnauthorisedCallback.as_view(),
        name='close-callback-object'
    ),
    path(
        'delete-ticket/<int:ticket_id>/',
        views.DeleteTicketForClientPage.as_view(),
        name='delete-ticket'
    ),
    path(
        'edit-ticket/<int:ticket_id>/',
        views.EditTicketForClientPage.as_view(),
        name='edit-ticket'
    ),
    path(
        'view-ticket/<int:ticket_id>/',
        views.ViewTicketForClientPage.as_view(),
        name='view-ticket'
    ),
    path(
        're-open-ticket/<int:ticket_id>/',
        views.ReopenTicket.as_view(),
        name='re-open-ticket'
    ),
    path(
        're-open-callback/<int:ticket_id>/',
        views.ReopenCallback.as_view(),
        name='re-open-callback'
    ),
    path(
        're-open-quote-request/<int:ticket_id>/',
        views.ReopenQuote.as_view(),
        name='re-open-quote-request'
    ),
]
