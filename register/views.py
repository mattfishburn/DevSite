from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.mail import send_mail

from .models import EmailAddress, EmailAddressRegistrationRequest
from datetime import datetime, timezone

# Create your views here.
def Index(request):
    template = loader.get_template('register/index.html')
    return HttpResponse(template.render({}, request))

def NewEmail(request):
    template = loader.get_template('register/register.html')
    return HttpResponse(template.render({}, request))

# todo: move to service
def EmailConfirmation(address, url):
    send_mail('Please Confirm Your Email Address',
              'Please confirm your email address by visting the following URL: <a href="%s">%s</a>'%(url, url),
              'RegistrationExample@example.com',
              [address.Address],
              fail_silently=False
              )

def NewEmailRequestDone(request):
    template = loader.get_template('register/submitted.html')
    emailAddressText = request.POST['EmailAddress']
    if not EmailAddress.ValidEmail(emailAddressText):
        return HttpResponse("That is not a valid email.  Please try again.")

    if EmailAddress.objects.filter(Address=emailAddressText).exists():
        emailAddress = EmailAddress.objects.get(Address=emailAddressText)
        newRequest = EmailAddressRegistrationRequest(EmailAddress=emailAddress)

        newRequest.save()
    else:
        emailAddress = EmailAddress(Address = emailAddressText)
        emailAddress.save()
        newRequest = EmailAddressRegistrationRequest(EmailAddress=emailAddress)

        newRequest.save()

    #todo: use a url parser here
    baseUrl = request.build_absolute_uri()[:-6] +'confirm/'
    EmailConfirmation(emailAddress, baseUrl + newRequest.ExternalKey)
    return HttpResponse(template.render({'address':emailAddress.Address}, request))

def ConfirmEmail(request, code=None):    
    template = loader.get_template('register/confirm.html')

    failureMessage = "Sorry I could not confirm that code."
    successMessage = "Email successfully confirmed."
    success = False
    if EmailAddressRegistrationRequest.objects.filter(ExternalKey=code).exists():
        relevantRequest = EmailAddressRegistrationRequest.objects.get(ExternalKey=code)
        now = datetime.now(timezone.utc)
        if relevantRequest.CanBeValidated():
            relevantRequest.ClickDate  = now
            relevantRequest.save()
            emailAddress = relevantRequest.EmailAddress
            emailAddress.Status = emailAddress.StatusVerified
            emailAddress.save()
            success = True
    if success:
        return HttpResponse(template.render({'result':successMessage},
                                            request))
    else:
        return HttpResponse(template.render({'result':failureMessage},
                                            request))

