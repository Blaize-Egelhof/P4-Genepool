from django.shortcuts import render, HttpResponse
from django.views import View # Views is a base class needed to create view based classes 

# Create your views here.

class Index(View): # This line defines a new class named Index that inherits from the View class. This means Index is a subclass of the View class, which provides the basic structure for handling HTTP requests
    def get(self,request): #The self parameter is required in class methods. It refers to the instance of the class (in this case, an instance of Index), allowing you to access attributes and other methods of the class.
        return render(request, 'index.html') #request is the HTTP request object that was sent by the client. It contains information about the request, such as headers, user data, and more.
