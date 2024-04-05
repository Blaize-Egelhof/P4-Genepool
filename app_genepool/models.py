from django.conf import settings
from django.db import models
from django.utils import timezone


class UnauthorisedQuoteRequests(models.Model):
    full_nameORcompany_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(max_length=15, blank=True, 
                            default='No phone provided')
    SERVICE_CHOICES = [
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
    request_description = models.CharField(max_length=800, blank=True)
    service = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Ongoing", blank=True)
    time_requested = models.DateTimeField(default=timezone.now)
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='Closed_requestsQuote', verbose_name='Closedquote' , blank=True, null=True)



class UnauthorisedCallBackRequests(models.Model):
    full_nameORcompany_name = models.CharField(max_length=100, blank=False)
    email = models.EmailField(blank=False)
    phone = models.CharField(
        max_length=15, blank=True, default='No phone provided'
    )
    SERVICE_CHOICES = [
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
    request_description = models.CharField(max_length=800, blank=True)
    service = models.CharField(
        max_length=20, choices=SERVICE_CHOICES, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Ongoing", blank=True)
    time_requested = models.DateTimeField(default=timezone.now)
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='Closed_requests_Callback', verbose_name='Closed_Callback', blank=True,null=True)


class AuthorisedTicketRequests(models.Model):
    STATUS_CHOICES = [
        ('Unanswered', 'Unanswered'),
        ('Answered', 'Answered'),
        ('Closed', 'Closed'),
    ]

    full_nameORcompany_name = models.CharField(max_length=100, blank=False)
    time_requested = models.DateTimeField(default=timezone.now)
    request_description = models.CharField(max_length=800, blank=False)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Unanswered")
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='client_requests', verbose_name='Client')
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='Closed_requests', verbose_name='Closed', blank=False,null=True)


class ChatDialogue(models.Model):
    ticket = models.ForeignKey(
        AuthorisedTicketRequests, related_name='chat_dialogues',
        on_delete=models.CASCADE)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    file = models.FileField(
        upload_to='GENEPOOL/templates/ticket-files/', blank=True)
