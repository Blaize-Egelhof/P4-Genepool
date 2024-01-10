from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import QuoteRequestForm
from .models import UnauthorisedQuoteRequests
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



class StaffPage(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        quote_requests = UnauthorisedQuoteRequests.objects.all()
        staff_group = user.groups.filter(Q(name='Staff')).exists()

        if staff_group:
            messages.info(request, 'YOU ARE A STAFF GROUP MEMBER.')  # Moved here
            return render(request, 'staff-page.html', {'user': user, 'quote_requests': quote_requests})
        else:
            messages.error(request, 'YOU ARE NOT A STAFF GROUP MEMBER.')  # Moved here
            return render(request, 'client-page.html', {'user': user, 'quote_requests': quote_requests})


class EditQuoteRequest(LoginRequiredMixin, View):
    template_name = 'edit_quote_request.html'
    login_url = reverse_lazy('login')

    def get(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(instance=quote)
        messages.success(request, f'Now Working On Quote Number: {quote.id}')
        return render(request, self.template_name, {'quote_id': quote_id, 'form': form})
    

    def post(self, request, quote_id, *args, **kwargs):
        # Handle the main form submission
        if 'save_changes' in request.POST:
            return self.handle_save_changes(request, quote_id)
        elif 'delete_quote' in request.POST:
            return self.handle_delete_quote(request, quote_id)
        elif 'delete_this_quote' in request.POST:
            return self.handle_delete_quote(request, quote_id)
        else:
            pass            

    def handle_save_changes(self, request, quote_id):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(request.POST, instance=quote)

        if form.is_valid():
            form.save()
            messages.success(request, f'Quote Num:{quote.id} has been updated successfully!')
            return redirect('staff-page')
        else:
            messages.error(request, f'Error updating {quote.id}. Please check the form data.')
            return render(request, self.template_name, {'quote_id': quote_id, 'form': form})

    def handle_delete_quote(self, request, quote_id):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        messages.success(request, f'Quote Num:{quote.id} has been deleted successfully!')
        quote.delete()
        return redirect('staff-page')
    
class DeleteQuoteRequest(LoginRequiredMixin, View):
    def post(self, request, quote_id):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        if request.method == 'POST':
            messages.success(request, f'Quote Num:{quote.id} has been deleted successfully!')
            quote.delete()
            return redirect('staff-page')

