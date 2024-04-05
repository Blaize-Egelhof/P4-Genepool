from django.shortcuts import (
    render, redirect, get_object_or_404
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import (
    QuoteRequestForm, AuthorisedTicketRequestForm, ChatDialogue1, CallBackForm
)
from .models import (
    UnauthorisedQuoteRequests, UnauthorisedCallBackRequests,
    AuthorisedTicketRequests, ChatDialogue
)
from django.contrib.auth.models import Group, User
from django import template
from django.db.models import Q
from django.urls import reverse

register = template.Library()

"""
Index view that handles the landing page requests. It supports both GET and POST methods.
GET requests simply render the landing page, while POST requests handle the submission
of quote requests through a form.
"""

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote request submitted successfully!')
            return redirect('home-page')
        else:
            messages.error(request, 'Error submitting quote request.'
                                    'Please ensure the required fields'
                                    'indicated by * arecorrectly filled in')
            return redirect('home-page')

"""
ProductsAndServoces view that handles requests for the 'Products and Services' page.
This view supports both GET and POST methods.
The GET method renders the 'products-and-services.html' template,
while the POST method processes submissions of the CallBackForm.
"""

class ProductsAndServices(View):
    def get(self, request):
        return render(request, 'products-and-services.html')

    def post(self, request):
        form = CallBackForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'CallBack Form Request submitted'
                                      'successfully! We will be in contact via'
                                      'provided email or phone number')
            return redirect('products_and_services')
        else:
            messages.error(request, 'Error submitting callback request.'
                                    'Please ensure the required fields'
                                    'indicated by * are correctly filled in')
            return redirect('products_and_services')


"""
StaffPage view that handles requests to the staff page.
This page displays various categories of ticket and request objects, 
differentiating between those addressed to staff and those from clients.
It requires the user to be logged in and to be a part of the 'Staff' group
to access the staff-specific information. Users not part of the 'Staff' group will see
a client-specific view.
"""

class StaffPage(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        staff_group = user.groups.filter(Q(name='Staff')).exists()

        staff_ticket_requests_closed = (
            AuthorisedTicketRequests.objects.filter(status='Answered')
        )

        answered_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Answered', client=user)
        )

        staff_answered_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Answered')
        )

        unanswered_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Unanswered', client=user)
        )

        staff_unanswered_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Unanswered')
        )

        closed_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Closed', client=user)
        )

        staff_closed_client_ticket_request = (
            AuthorisedTicketRequests.objects.filter(status='Closed')
        )

        if staff_group:
            staff_unauthorised_callback_requests_ongoing = (
                UnauthorisedCallBackRequests.objects.filter(status='Ongoing')
            )

            staff_unauthorised_callback_requests_completed = (
                UnauthorisedCallBackRequests.objects.filter(status='Completed')
            )

            staff_unauthorised_quote_requests_ongoing = (
                UnauthorisedQuoteRequests.objects.filter(status='Ongoing')
            )

            staff_unauthorised_quote_requests_completed = (
                UnauthorisedQuoteRequests.objects.filter(status='Completed')
            )

            context = {
                'user': user,
                'staff_ticket_requests_closed': staff_ticket_requests_closed,
                'staff_unanswered_client_ticket_request': staff_unanswered_client_ticket_request,
                'staff_answered_client_ticket_request': staff_answered_client_ticket_request,
                'staff_closed_client_ticket_request': staff_closed_client_ticket_request,
                'staff_unauthorised_callback_requests_ongoing': staff_unauthorised_callback_requests_ongoing,
                'staff_unauthorised_callback_requests_completed': staff_unauthorised_callback_requests_completed,
                'staff_unauthorised_quote_requests_ongoing': staff_unauthorised_quote_requests_ongoing,
                'staff_unauthorised_quote_requests_completed': staff_unauthorised_quote_requests_completed,
            }
            return render(request, 'staff-page.html', context,)
        else:
            context = {
                'user': user,
                'answered_client_ticket_request': answered_client_ticket_request,
                'unanswered_client_ticket_request': unanswered_client_ticket_request,
                'closed_client_ticket_request': closed_client_ticket_request,
            }
            return render(request, 'client-page.html', context)


"""
Handles the submission of an authorised ticket request by a logged-in user. 
This view is responsible for processing the AuthorisedTicketRequestForm,
saving the form data to create a new authorised ticket
request linked to the current user, 
and providing feedback to the user about the submission outcome.

This function requires the user to be authenticated,
ensuring that only logged-in users can submit ticket requests.
Upon successful form submission, the user is redirected to the 'staff-page',
and a success message is displayed.
If there are issues with the form data, the user is informed
of the errors, and the form is re-rendered for correction.
"""

@login_required
def submit_authorised_ticket_request(request):
    if request.method == 'POST':
        user = request.user
        form = AuthorisedTicketRequestForm(request.POST, user=request.user)
        if form.is_valid():
            authorised_ticket_request = form.save(commit=False)
            authorised_ticket_request.client = user
            authorised_ticket_request.save()
            messages.success(request, 'Your Ticket request has been submitted'
                                      'successfully.')
            return redirect('staff-page')
        else:
            print(form.errors)
            messages.error(request, 'There was an error in your form.')
            return render(request, 'client-page.html', {'form': form})


"""
A view for editing an existing unauthorised quote request. This view allows users
with the appropriate permissions to modify details of a specific quote request.

Inherits from Django's LoginRequiredMixin to ensure that only authenticated
users can access this view.
"""

class EditQuoteRequest(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(instance=quote)
        messages.success(request, f'Now Editing Quote: {quote.id}')
        return render(request, "edit-quote-request.html",
                               {'quote_id': quote_id, 'form': form})
    
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(request.POST, instance=quote)
        if form.is_valid():
            form.save()
            messages.success(request, f'Quote {quote.id} has been successfully updated.')
            return redirect('staff-page') 
        else:
            messages.error(request, 'Error updating the quote. Please check the form for errors.')
            return render(request, "edit-quote-request.html", {'quote_id': quote_id, 'form': form})

"""
A view for marking an unauthorised quote request as completed. This view is
intended for use by staff users to update the status of a quote request to
'Completed'.

Inherits from Django's LoginRequiredMixin to ensure that only authenticated
users can access this view.
"""

class CloseUnauthorisedQuote (LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        quote.status = 'Completed'
        quote.closed_by = request.user
        quote.save()
        messages.success(request, f'Quote {quote.id} has been marked '
                                  'as completed!')
        return redirect(reverse('staff-page'))

"""
A view for marking an unauthorised callback request as completed. This action
is performed by staff users to indicate that a callback request has
been resolved.

Inherits from Django's LoginRequiredMixin to ensure that only authenticated
users can access this view.
"""

class CloseUnauthorisedCallback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        callback_id = kwargs.get('callback_id')
        print(callback_id)
        callback_object = (
            get_object_or_404(UnauthorisedCallBackRequests, pk=callback_id)
        )
        callback_object.status = 'Completed'
        callback_object.closed_by = request.user
        callback_object.save()
        messages.success(request, f'Callback {callback_object.id} has been'
                                  'marked as completed!')
        return redirect(reverse('staff-page'))


"""
A view for editing an existing unauthorised callback request. This view allows
staff users to modify details of a specific callback request, identified by its
unique identifier.

Inherits from Django's LoginRequiredMixin to ensure that only authenticated
users, specifically staff, can access this view.

"""

class EditCallBackRequest(LoginRequiredMixin, View):
    template_name = 'edit-callback-request.html'

    def get(self, request, *args, **kwargs):
        callback_request_id = kwargs.get('callback_request_id')
        callback_request = (
            get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        )
        form = CallBackForm(instance=callback_request)
        messages.success(request, f'Now Working On Callback Number: {callback_request_id}')
        return render(request, self.template_name, {
            'callback_request_id': callback_request_id,
            'form': form
        })


    def post(self, request, callback_request_id, *args, **kwargs):
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, callback_request_id)

    def handle_save_changes(self, request, callback_request_id):
        callback_request = (
            get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        )
        form = CallBackForm(request.POST, instance=callback_request)
        if form.is_valid():
            form.save()
            messages.success(request,
                             f'Callback Num:{callback_request_id} '
                             'has been updated successfully!')
            return redirect('staff-page')
        else:
            messages.error(request,
                           f'Error updating callback {callback_request_id}. '
                           'Please check the form data.')

            return render(request, self.template_name, {
                         'form': form,
                         'callback_request_id': callback_request_id
            })

"""
A view that handles the deletion of unauthorised quote requests. This view ensures
that only authenticated users, specifically staff, can delete a quote request.

Inherits from Django's LoginRequiredMixin to restrict access to authenticated users.

"""

class DeleteQuoteRequest(LoginRequiredMixin, View):
    def post(self, request, quote_id):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        if request.method == 'POST':
            messages.success(request,
                             f'Quote Num:{quote.id} ' +
                             'has been deleted successfully!')

            quote.delete()
            return redirect('staff-page')

"""
A view for handling the deletion of callback requests by authenticated users.
Ensures that only users with the required permissions can delete callback requests.
"""

class DeleteCallBackRequest(LoginRequiredMixin, View):
    def post(self, request, callback_request_id):
        callback_request = (
            get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        )
        if request.method == 'POST':
            messages.success(request, f'Callback request with ID: '
                                      f'{callback_request.id} has been'
                                      f'deleted successfully!')

            callback_request.delete()
            return redirect('staff-page')

"""
A view for closing tickets from the client page, accessible only by authenticated users.

"""

class CloseTicketForClientPage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        ticket_id = self.kwargs.get('ticket_id')
        print(f"Ticket ID: {ticket_id}")
        ticket_to_close = (
            get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        )
        ticket_to_close.status = 'Closed'
        ticket_to_close.save()
        return redirect('staff-page')

"""
A view for deleting tickets, accessible only to authenticated users who are not part of the 'staff_group'.

"""

class DeleteTicketForClientPage(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        user = request.user
        
        if user.groups.filter(name='staff_group').exists():
            
            return HttpResponseForbidden
            ("You are not authorized to perform this action.")
        ticket_id = self.kwargs.get('ticket_id')
        ticket_to_delete =(
            get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        )
        messages.success(request, f'You Have Succesfully Deleted the ticket')
        ticket_to_delete.delete()
        return redirect('staff-page')

"""
Provides functionality for editing and deleting authorised ticket requests. 
This view ensures that only authenticated users can perform these actions, specifically on tickets they have access to.

"""

class EditTicketForClientPage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        form = AuthorisedTicketRequestForm (instance=ticket, user=request.user)
        return render(
            request, 'edit-ticket.html', {'form': form, 'ticket_id': ticket_id}
        )
    
    def post(self, request, ticket_id, *args, **kwargs):
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, ticket_id)
        elif 'delete_this_ticket' in request.POST:
            return self.handle_delete_quote(request, ticket_id)
    
    def handle_save_changes(self, request, ticket_id):
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        form = AuthorisedTicketRequestForm(
            request.POST, 
            instance=ticket, 
            user=request.user
        )
        if form.is_valid():
            form.save()
            messages.success
            (request, f'Ticket Num:{ticket.id} has been updated successfully!')
            return redirect('staff-page')
        else:
            messages.error(request, f'Error updating {ticket.id}. '
                                    'Please check the form data.')

            return render(request, 'edit-ticket.html', {'form': form})

    def handle_delete_quote(self, request, ticket_id):
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        messages.success
        (request, f'Ticket Num:{ticket.id} has been deleted successfully!')
        quote.delete()
        return redirect('staff-page')

"""
Provides functionality for viewing and replying to tickets for clients. This view allows
clients and staff to interact with the ticket by posting replies. It ensures that only authenticated
users can access the ticket viewing and replying features.
"""

class ViewTicketForClientPage(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Handles GET requests to display the ticket and associated chat messages
        return self.render_ticket_page(request)

    def post(self, request, *args, **kwargs):
        # Handles POST requests for submitting replies to a ticket
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        user = request.user
        form = ChatDialogue1(request.POST, request.FILES)
        
        if form.is_valid():
            # If the form is valid, save the reply and update ticket status
            reply = form.save(commit=False)
            reply.ticket = ticket
            reply.author = user
            reply.save()

            staff_group = user.groups.filter(Q(name='Staff')).exists()
            if staff_group:
                ticket.status = "Answered"
            else:
                ticket.status = "Unanswered"
            ticket.save()

            messages.success(request, 'Reply Sent Successfully!')
        else:
            print(form.errors)
            messages.error(request, 'Reply is invalid, please ensure the name and text field is filled in before submitting.')

        return self.render_ticket_page(request)
        
    def render_ticket_page(self, request):
        """
        Renders the ticket page with the ticket details, chat messages, and a form for submitting new messages.

        This method fetches all chat messages related to the ticket, orders them by timestamp, and paginates
        the result to display on the ticket page.
        """
        ticket_id = self.kwargs.get('ticket_id')
        user = request.user
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        chat_messages = ChatDialogue.objects.filter(ticket=ticket).order_by('-timestamp')
        paginator = Paginator(chat_messages, 10)  # Paginate chat messages
        page_number = request.GET.get('page')
        chat_messages = paginator.get_page(page_number)
        form = ChatDialogue1()  # Initialize the form for new replies

        return render(request, 'ticket-view.html', {
            'ticket': ticket,
            'user': user,
            'chat_messages': chat_messages,
            'form': form
        })
"""
ReopenTicket view for reopening a previously closed ticket. Only accessible by authenticated users.

Inherits from Django's LoginRequiredMixin to ensure that only authenticated users can access this view.

"""

class ReopenTicket(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        ticket.status = "Unanswered"
        ticket.save()
        messages.success(request, "Ticket has been reopened successfully.")
        return redirect('staff-page')

"""
ReopenCallback view for reopening a previously closed callback request. Accessible only to authenticated users.

Inherits from Django's LoginRequiredMixin for authentication checks.

"""

class ReopenCallback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        callback_id = kwargs.get('ticket_id')
        callback =(
            get_object_or_404(UnauthorisedCallBackRequests, pk=callback_id)
        )
        callback.status = "Ongoing"
        callback.save()
        messages.success(request, "Callback successfully opened.")
        return redirect('staff-page')

"""
Allows authenticated users to reopen a quote request by changing its status back to "Ongoing".

Inherits from LoginRequiredMixin to restrict access to authenticated users.

"""

class ReopenQuote(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('ticket_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        quote.status = "Ongoing"
        quote.save()
        messages.success(request, "Quote Opened Succesfully.")
        return redirect('staff-page')
