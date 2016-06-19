from django.db import models
import uuid
import random
import string

from datetime import timezone, datetime

# Create your models here.

def randomKey():
    return str(uuid.uuid4())+'-'+''.join(random.choice(string.ascii_uppercase+string.digits) for _ in range(64))

class EmailAddress(models.Model):
    def ValidEmail(unvalidatedEmail):
        return '@' in unvalidatedEmail and not ' ' in unvalidatedEmail    

    StatusUnverified = 0
    StatusVerified = 1
    StatusClosed = 2

    StatusChoices = (
        (StatusUnverified, 'Unverified', ),
        (StatusVerified, 'Verified', ),
        (StatusClosed, 'Closed', ),
    )

    Status = models.IntegerField(default=0, choices=StatusChoices)
    Address = models.CharField(max_length=256)    

class EmailAddressRegistrationRequest(models.Model):
    EmailAddress = models.ForeignKey(EmailAddress, on_delete=models.CASCADE)
    CreationDate = models.DateTimeField('Date Created', null=False, blank=False, auto_now_add=True)

    #null is magic value for unclicked
    ClickDate = models.DateTimeField('Date Clicked', null=True, blank=True, default=None)

    ExternalKey = models.CharField(max_length=256, null=False, blank=False, default=randomKey)

    def CanBeValidated(self):
        now = datetime.now(timezone.utc)
        if self.ClickDate is not None:
            return False
        return (now - self.CreationDate).total_seconds() < 24 * 60 * 60
