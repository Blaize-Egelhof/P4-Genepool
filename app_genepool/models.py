from django.conf import settings
from django.db import models
from django.utils import timezone

class UnauthorisedQuoteRequests(models.Model):
     full_nameORcompany_name = models.CharField(max_length=100 , blank=False)
     email = models.EmailField(blank=False)
     phone = models.CharField(max_length=15, blank=True , default='No phone provided')
     SERVICE_CHOICES = [  #List of tuplets, first value is db , second is user choice
        ('support', 'Support'),
        ('hardware', 'Hardware'),
        ('software', 'Software'),  
        ('microsoft', 'Microsoft'),  
        ('power_solutions', 'Power Solutions')  
     ]
     STATUS_CHOICES = [ 
        ('Ongoing', 'Open'),
        ('Completed', 'Closed'),
     ]
     request_description = models.CharField(max_length=800 , blank=True)
     service = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
     status = models.CharField(max_length=20, choices =STATUS_CHOICES , default="Ongoing", blank=True)
     time_requested = models.DateTimeField(default=timezone.now)

class UnauthorisedCallBackRequests(models.Model): 
     full_nameORcompany_name = models.CharField(max_length=100 , blank=False)
     email = models.EmailField(blank=False)
     phone = models.CharField(max_length=15, blank=True , default='No phone provided')
     SERVICE_CHOICES = [  #List of tuplets, first value is db , second is user choice
        ('support', 'Support'),
        ('hardware', 'Hardware'),
        ('software', 'Software'),  
        ('microsoft', 'Microsoft'),  
        ('power_solutions', 'Power Solutions')  
     ]
     STATUS_CHOICES = [ 
        ('Ongoing', 'Open'),
        ('Completed', 'Closed'),
     ]
     request_description = models.CharField(max_length=800 , blank=True)
     service = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
     status = models.CharField(max_length=20, choices =STATUS_CHOICES , default="Ongoing", blank=True)
     time_requested = models.DateTimeField(default=timezone.now)

## For Clients directly 

class AuthorisedQuoteRequests(models.Model):
     full_nameORcompany_name = models.CharField(max_length=100 , blank=False)
     email = models.EmailField(blank=False)
     phone = models.CharField(max_length=15, blank=True , default='No phone provided')
     SERVICE_CHOICES = [  #List of tuplets, first value is db , second is user choice
        ('support', 'Support'),
        ('hardware', 'Hardware'),
        ('software', 'Software'),  
        ('microsoft', 'Microsoft'),  
        ('power_solutions', 'Power Solutions')  
     ]
     STATUS_CHOICES = [ 
        ('Unanswered', 'Unanswered'),
        ('Answered', 'Answered'),
        ('Closed', 'Closed'),
     ]
     request_description = models.CharField(max_length=800 , blank=True)
     service = models.CharField(max_length=20, choices=SERVICE_CHOICES, blank=True)
     status = models.CharField(max_length=20, choices =STATUS_CHOICES , default="Unanswered", blank=True)
     time_requested = models.DateTimeField(default=timezone.now)
     client = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name='quote_requests',
     )



