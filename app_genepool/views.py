from django.shortcuts import render, HttpResponse,redirect , get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views import View # Views is a base class needed to create view based classes 
from .forms import QuoteRequestForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UnauthorisedQuoteRequests
# Create your views here.

class Index(View): # This line defines a new class named Index that inherits from the View class. This means Index is a subclass of the View class, which provides the basic structure for handling HTTP requests
    def get(self,request): #The self parameter is required in class methods. It refers to the instance of the class (in this case, an instance of Index), allowing you to access attributes and other methods of the class.
        return render(request, 'index.html') #request is the HTTP request object that was sent by the client. It contains information about the request, such as headers, user data, and more.


    def post(self,request): 
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Quote request submitted successfully!')
            return redirect('home-page') # Redirect remebers where users were last on.
        else:
            print(form.errors)  # This will print form errors to the console
            messages.error(request, 'Error submitting quote request. Please ensure the required fields indicated by * are correctly filled in')
            return redirect('home-page')


class Products_And_Services(View):
    def get(self,request):
        return render(request, 'products-and-services.html')

class Staff_Page(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user  # This retrieves the currently logged-in user
        messages.success(request, 'Succesfully logged in as ')
        quoteRequests = UnauthorisedQuoteRequests.objects.all()
        return render(request, 'staff-login-page.html', {'user': user, 'quoteRequests': quoteRequests})

@login_required(login_url='login')
def edit_quote_request(request, quote_id):
    quote = get_object_or_404(UnauthorisedQuoteRequests, pk=quote_id)
    form = QuoteRequestForm(instance=quote)
    return render(request, 'edit_quote_request.html', {'quote_id': quote_id, 'form': form})

    # def post(self, request):
    #     # 1. Instantiate the QuoteRequestForm with the POST data
    #     form = QuoteRequestForm(request.POST)

    #     # 2. Check if the form is valid
    #     if form.is_valid():
    #         # 3. Retrieve the quote_id from the form data (replace 'quote_id' with your actual field name)
    #         quote_id = request.POST.get('quote_id')

    #         # 4. Get the existing UnauthorisedQuoteRequests instance based on the quote_id
    #         quote = UnauthorisedQuoteRequests.objects.get(pk=quote_id)

    #         # 5. Bind the form to the existing instance for updating
    #         form = QuoteRequestForm(request.POST, instance=quote)

    #         # 6. Check if the updated form is valid
    #         if form.is_valid():
    #             # 7. Save the updated form data to the database
    #             form.save()

    #             # 8. Display a success message
    #             messages.success(request, 'Quote request updated successfully!')
    #         else:
    #             # 9. Display an error message if the form is not valid
    #             messages.error(request, 'Error updating quote request. Please check the form data.')
    #     else:
    #         # 10. Display an error message if the initial form is not valid
    #         messages.error(request, 'Error submitting quote request. Please ensure the required fields are correctly filled in.')

    #     # 11. Redirect to the staff page after processing the form
    #     return render(request, 'staff-login-page.html', {'user': user, 'quoteRequests': quoteRequests})