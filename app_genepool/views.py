from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import View
from .forms import QuoteRequestForm
from .models import UnauthorisedQuoteRequests

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
        print(request.session.get('messages'))
        return render(request, 'staff-login-page.html', {'user': user, 'quote_requests': quote_requests})

class EditQuoteRequest(LoginRequiredMixin, View):
    template_name = 'edit_quote_request.html'
    login_url = reverse_lazy('login')

    def get(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(instance=quote)
        return render(request, self.template_name, {'quote_id': quote_id, 'form': form})
    

    def post(self, request, quote_id, *args, **kwargs):
        quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
        form = QuoteRequestForm(request.POST, instance=quote)

        if form.is_valid():
            form.save()
            messages.success(request, 'Quote request updated successfully!')
            return redirect('staff-page')
        else:
            messages.error(request, 'Error updating quote request. Please check the form data.')
            return render(request, self.template_name, {'quote_id': quote_id, 'form': form})