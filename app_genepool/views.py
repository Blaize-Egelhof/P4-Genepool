from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import QuoteRequestForm, AuthorisedQuoteRequestForm,AuthorisedTicketRequestForm,ChatDialogue1
from .models import UnauthorisedQuoteRequests,UnauthorisedCallBackRequests,AuthorisedQuoteRequests,AuthorisedTicketRequests,ChatDialogue
from django.contrib.auth.models import Group, User
from django import template
from django.db.models import Q

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
        authorisedclient_quote_requests = AuthorisedQuoteRequests.objects.filter(client=user)  
        unauthorised_quote_requests = UnauthorisedQuoteRequests.objects.all()
        unauthorised_callback_requests = UnauthorisedCallBackRequests.objects.all()
        unanswered_quotes = AuthorisedQuoteRequests.objects.filter(status='Unanswered', client=user)
        answered_quotes = AuthorisedQuoteRequests.objects.filter(status='Answered' , client=user)
        closed_quotes = AuthorisedQuoteRequests.objects.filter(status='Closed' , client=user)
        staff_group = user.groups.filter(Q(name='Staff')).exists()
        ticket_requests = AuthorisedTicketRequests.objects.all()
        answered_client_ticket_request = AuthorisedTicketRequests.objects.filter(status='Answered', client=user)
        unanswered_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Unanswered', client=user)
        closed_client_ticket_request =AuthorisedTicketRequests.objects.filter(status='Closed', client=user)

        if staff_group:
            messages.info(request, 'YOU ARE A STAFF MEMBER.')  
            return render(request, 'staff-page.html', {
                'user': user, 
                'unauthorised_quote_requests': unauthorised_quote_requests,
                'unauthorised_callback_requests': unauthorised_callback_requests,
                'authorisedclient_quote_requests': authorisedclient_quote_requests,
            })
        else:
            return render(request, 'client-page.html', {
                'user': user, 
                'unanswered_quotes':unanswered_quotes,
                'answered_quotes':answered_quotes, 'closed_quotes':closed_quotes,
                'closed_quotes':closed_quotes, 'answered_client_ticket_request': answered_client_ticket_request ,
                'unanswered_client_ticket_request':unanswered_client_ticket_request,
                'closed_client_ticket_request':closed_client_ticket_request
            })
    # def post(self, request):
    #     form = AuthorisedQuoteRequestForm(request.POST,user=request.user)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request, 'Quote Request submitted successfully.')
    #         return redirect('staff-page')
    #     else:
    #         messages.error(request, 'Error submitting Quote Request, please ensure the fields indicated by * are correctly filled in.')
    #         return render(request, 'staff-page', {'form': form})

@login_required
def submit_authorised_quote_request(request):
    if request.method == 'POST':
        user = request.user
        authorisedclient_quote_requests = AuthorisedQuoteRequests.objects.filter(client=user)
        form = AuthorisedQuoteRequestForm(request.POST, user=request.user)
        if form.is_valid():
            authorised_quote_request = form.save(commit=False)
            authorised_quote_request.client = request.user  
            authorised_quote_request.save()
            messages.success(request, 'Your authorized quote request has been submitted successfully.')
            return redirect('staff-page')
        else:
            print(form.errors) 
            messages.error(request, 'There was an error in your form.')
            return render(request, 'client-page.html', {'form': form , 'authorisedclient_quote_requests': authorisedclient_quote_requests })
    else:
        form = AuthorisedQuoteRequestForm(user=request.user)
        return render(request, 'client-page.html', {'form': form , 'authorisedclient_quote_requests': authorisedclient_quote_requests, })  

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
    template_name = 'edit-quote-request.html'
    login_url = reverse_lazy('login')

    def get(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(AuthorisedQuoteRequests, pk=quote_id)
        form = AuthorisedQuoteRequestForm(instance=quote, user=request.user)  
        messages.success(request, f'Now Editing Quote: {quote.id}')
        return render(request, self.template_name, {'quote_id': quote_id, 'form': form})

    def post(self, request, ticket_id, *args, **kwargs):
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, ticket_id)
        elif 'go_back' in request.POST:
            return render(request, 'staff-page.html')



class EditCallBackRequest(LoginRequiredMixin, View):
    template_name = 'edit-callback-request.html'
    login_url = reverse_lazy('login')

    def get(self, request, callback_request_id, *args, **kwargs):
        callback_request = get_object_or_404(UnauthorisedCallBackRequests, pk=callback_request_id)
        form = QuoteRequestForm(instance=callback_request)
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

class CloseQuoteForClientPage(LoginRequiredMixin,View): 
    def post(self,request, *args, **kwargs):
        user=request.user
        quote_id = self.kwargs.get('quote_id')
        quote_to_close = get_object_or_404(AuthorisedQuoteRequests , pk=quote_id)
        quote_to_close.status = 'Closed'
        quote_to_close.save()
        return render(request, 'client-page.html', {'form': form , 'authorisedclient_quote_requests': authorisedclient_quote_requests, })


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

    # def post(self, request, *args, **kwargs):
    #     ticket_id = self.kwargs.get('ticket_id')
    #     ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
    #     form = AuthorisedTicketRequestForm(request.POST, instance=ticket)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('staff-page')
    #     return render(request, 'edit-ticket.html', {'form': form})

class ViewTicketForClientPage(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        user=request.user
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        chat_messages = ChatDialogue.objects.filter(ticket=ticket).order_by('timestamp')
        return render(request,'ticket-view.html', {'ticket': ticket, 'user': user, 'chat_messages': chat_messages})
    def post(self, request, *args, **kwargs):
        ticket_id = self.kwargs.get('ticket_id')
        ticket = get_object_or_404(AuthorisedTicketRequests, pk=ticket_id)
        user = request.user
        chat_messages = ChatDialogue.objects.filter(ticket=ticket).order_by('timestamp')
        form = ChatDialogue1(request.POST, request.FILES) 
        if form.is_valid(): 
            reply = form.save(commit=False) 
            reply.ticket = ticket 
            reply.author = user  
            reply.save()
            messages.success(request, 'Reply Send Succesfully !')
            print(chat_messages)
            return render(request, 'ticket-view.html', {'ticket': ticket, 'user': user, 'form': form, 'chat_messages': chat_messages})
        else:
            messages.error(request, 'Reply is invalid, please ensure the name and text field is filled in before submitting.')
            print(chat_messages)
            return render(request, 'ticket-view.html', {'ticket': ticket, 'user': user, 'form': form, 'chat_messages': chat_messages})


