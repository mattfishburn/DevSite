from django.contrib import admin

# Register your models here.

from .models import EmailAddress
from .models import EmailAddressRegistrationRequest

admin.site.register(EmailAddress)
admin.site.register(EmailAddressRegistrationRequest)
