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



