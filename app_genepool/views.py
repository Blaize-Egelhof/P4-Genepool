from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import QuoteRequestForm,AuthorisedTicketRequestForm,ChatDialogue1,CallBackForm
from .models import UnauthorisedQuoteRequests,UnauthorisedCallBackRequests,AuthorisedTicketRequests,ChatDialogue
from django.contrib.auth.models import Group, User
from django import template
from django.db.models import Q
from django.urls import reverse
register = template.Library()

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
            messages.error(request, 'Error submitting quote request. Please ensure the required fields indicated by * are correctly filled in')
            return redirect('home-page')

class ProductsAndServices(View):
    def get(self, request):
        return render(request, 'products-and-services.html')
    
    def post(self, request):
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'CallBack Form Request submitted successfully! We will be in contact via provided email or phone number')
            return redirect('products_and_services')
        else:
            messages.error(request, 'Error submitting callback request. Please ensure the required fields indicated by * are correctly filled in')
            return redirect('products_and_services')

class StaffPage(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        staff_group = user.groups.filter(Q(name='Staff')).exists()
        staff_ticket_requests_closed = AuthorisedTicketRequests.objects.filter(status='Answered')
        answered_client_ticket_request = AuthorisedTicketRequests.objects.filter(status='Answered', client=user)
        staff_answered_client_ticket_request = AuthorisedTicketRequests.objects.filter(status='Answered')
        unanswered_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Unanswered', client=user)
        staff_unanswered_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Unanswered')
        closed_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Closed', client=user)
        staff_closed_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Closed')

        if staff_group: 
            staff_unauthorised_callback_requests_ongoing = UnauthorisedCallBackRequests.objects.filter(status='Ongoing')
            staff_unauthorised_callback_requests_completed = UnauthorisedCallBackRequests.objects.filter(status='Completed')
            staff_unauthorised_quote_requests_ongoing = UnauthorisedQuoteRequests.objects.filter(status ='Ongoing')
            staff_unauthorised_quote_requests_completed = UnauthorisedQuoteRequests.objects.filter(status ='Completed')
            return render(request, 'staff-page.html', {
                'user': user, 
                'staff_ticket_requests_closed' : staff_ticket_requests_closed,
                'staff_unanswered_client_ticket_request' : staff_unanswered_client_ticket_request,
                'staff_answered_client_ticket_request' : staff_answered_client_ticket_request,
                'staff_closed_client_ticket_request' : staff_closed_client_ticket_request,
                'staff_unauthorised_callback_requests_completed' : staff_unauthorised_callback_requests_completed,
                'staff_unauthorised_callback_requests_ongoing' : staff_unauthorised_callback_requests_ongoing,
                'staff_unauthorised_quote_requests_ongoing' : staff_unauthorised_quote_requests_ongoing,
                'staff_unauthorised_quote_requests_completed' : staff_unauthorised_quote_requests_completed, 
            })
        else:
            return render(request, 'client-page.html', {
                'user': user,
                'answered_client_ticket_request': answered_client_ticket_request ,
                'unanswered_client_ticket_request':unanswered_client_ticket_request,
                'closed_client_ticket_request':closed_client_ticket_request,
            })

@login_required
def submit_authorised_ticket_request(request):
    if request.method == 'POST':
        user = request.user
        form = AuthorisedTicketRequestForm(request.POST, user=request.user)
        if form.is_valid():
            authorised_ticket_request = form.save(commit=False)
            authorised_ticket_request.client = user  
            authorised_ticket_request.save()
            messages.success(request, 'Your Ticket request has been submitted successfully.')
            return redirect('staff-page')
        else:
            print(form.errors) 
            messages.error(request, 'There was an error in your form.')
            return render(request, 'client-page.html', {'form': form})





class EditQuoteRequest(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)  
        form = QuoteRequestForm(instance=quote)
        messages.success(request, f'Now Editing Quote: {quote.id}')
        return render(request, "edit-quote-request.html", {'quote_id': quote_id, 'form': form})

    # def post(self, request, *args, **kwargs):
    #     quote_id = kwargs.get('quote_id')
    #     quote = self.get_object(quote_id)
    #     form = QuoteRequestForm(request.POST, instance=quote)

    #     if 'save_changes' in request.POST:
    #         if form.is_valid():
    #             form.save()
    #             messages.success(request, 'Quote updated successfully!')
    #             return redirect('staff-page')
    #         else:
    #             messages.error(request, 'Please correct the error below.')

    #     elif 'go_back' in request.POST:
    #         return redirect('staff-page')

    #     return render(request, self.template_name, {'form': form})



class CloseUnauthorisedQuote (LoginRequiredMixin,View):
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        quote.status = 'Completed'
        quote.save()
        messages.success(request, f'Quote {quote.id} has been marked as completed!')
        return redirect(reverse('staff-page'))

class CloseUnauthorisedCallback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        callback_id = kwargs.get('callback_id')
        print(callback_id)
        callback_object = get_object_or_404(UnauthorisedCallBackRequests, pk=callback_id)
        callback_object.status = 'Completed'
        callback_object.save()
        messages.success(request, f'Callback {callback_object.id} has been marked as completed!')
        return redirect(reverse('staff-page'))














class EditCallBackRequest(LoginRequiredMixin, View):
    template_name = 'edit-callback-request.html'
    login_url = reverse_lazy('login')

    def get(self, request, callback_request_id, *args, **kwargs):
        callback_request = get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        form = CallBackForm(instance=callback_request)
        messages.success(request, f'Now Working On Callback Number: {callback_request_id}')
        return render(request, self.template_name, {'callback_request_id': callback_request_id, 'form': form})
    
    def post(self, request, callback_request_id, *args, **kwargs):
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, callback_request_id)
        elif 'delete_this_quote' in request.POST:
            return self.handle_delete_quote(request, callback_request_id)
    
class DeleteQuoteRequest(LoginRequiredMixin, View):
    def post(self, request, quote_id):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        if request.method == 'POST':
            messages.success(request, f'Quote Num:{quote.id} has been deleted successfully!')
            quote.delete()
            return redirect('staff-page')

class DeleteCallBackRequest(LoginRequiredMixin, View):
    def post(self, request, callback_request_id):
        callback_request = get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        if request.method == 'POST':
            messages.success(request, f'Callback request with ID: {callback_request.id} has been deleted successfully!')
            callback_request.delete()
            return redirect('staff-page')

class CloseTicketForClientPage(LoginRequiredMixin,View): 
    def post(self,request, *args, **kwargs):
        user=request.user
        ticket_id = self.kwargs.get('ticket_id')
        print(f"Ticket ID: {ticket_id}")
        ticket_to_close = get_object_or_404(AuthorisedTicketRequests , pk=ticket_id)
        ticket_to_close.status = 'Closed'
        ticket_to_close.save()
        return redirect('staff-page')

class DeleteTicketForClientPage(LoginRequiredMixin, View): 
    def post(self, request, *args, **kwargs):
        user = request.user
        # Check if the user belongs to the 'staff_group'
        if user.groups.filter(name='staff_group').exists():
            # If the user is not in the staff_group, return HTTP Forbidden status
            return HttpResponseForbidden("You are not authorized to perform this action.")
        ticket_id = self.kwargs.get('ticket_id')
        ticket_to_delete = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        messages.success(request, f'You Have Succesfully Deleted the ticket')
        ticket_to_delete.delete()
        return redirect('staff-page')

class EditTicketForClientPage(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        form = AuthorisedTicketRequestForm(instance=ticket, user=request.user) 
        return render(request, 'edit-ticket.html', {'form': form, 'ticket_id': ticket_id})
    
    def post(self, request, ticket_id, *args, **kwargs):
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, ticket_id)
        elif 'delete_this_ticket' in request.POST:
            return self.handle_delete_quote(request, ticket_id)
    
    def handle_save_changes(self, request, ticket_id):
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        form = AuthorisedTicketRequestForm(request.POST, instance=ticket, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f'Ticket Num:{ticket.id} has been updated successfully!')
            return redirect('staff-page')
        else:
            messages.error(request, f'Error updating {ticket.id}. Please check the form data.') 
            return render(request, 'edit-ticket.html', {'form': form})
    
    def handle_delete_quote(self, request, ticket_id):
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        messages.success(request, f'Ticket Num:{ticket.id} has been deleted successfully!')
        quote.delete()
        return redirect('staff-page')

class ViewTicketForClientPage(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        user=request.user
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        chat_messages = ChatDialogue.objects.filter(ticket=ticket).order_by('-timestamp')
        paginator = Paginator(chat_messages, 10)
        page_number = request.GET.get('page')
        chat_messages = paginator.get_page(page_number)

        return render(request, 'ticket-view.html', {'ticket': ticket,'user': user,'chat_messages': chat_messages})

    def post(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        user = request.user
        chat_messages = ChatDialogue.objects.filter(ticket=ticket).order_by('timestamp')
        staff_group = user.groups.filter(Q(name='Staff')).exists()
        form = ChatDialogue1(request.POST, request.FILES) 
        if form.is_valid():
                reply = form.save(commit=False)
                reply.ticket = ticket
                reply.author = user
                reply.save()

                if staff_group:
                    ticket.status = "Answered"
                else:
                    ticket.status = "Unanswered"
                ticket.save()

                messages.success(request, 'Reply Sent Successfully!')
                return render(request, 'ticket-view.html', {'ticket': ticket, 'user': user, 'form': form, 'chat_messages': chat_messages})
        else:
            messages.error(request, 'Reply is invalid, please ensure the name and text field is filled in before submitting.')
            return render(request, 'ticket-view.html', {'ticket': ticket, 'user': user, 'form': form, 'chat_messages': chat_messages})
            
class ReopenTicket(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        ticket_id = kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        ticket.status = "Unanswered"
        ticket.save()
        messages.success(request, "Ticket has been reopened successfully.")
        return redirect('staff-page') 
        
class ReopenCallback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        callback_id = kwargs.get('callback_id')
        callback = get_object_or_404(UnauthorisedCallBackRequests, pk=callback_id)
        callback.status = "Ongoing"
        callback.save()
        messages.success(request, "Callback Request has been reopened successfully.")
        return redirect('staff-page') 

class ReopenCallback(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        quote_id = kwargs.get('quote_id')
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        quote.status = "Ongoing"
        quote.save()
        messages.success(request, "Quote Request has been reopened successfully.")
        return redirect('staff-page') 