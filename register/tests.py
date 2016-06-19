from django.test import TestCase
from .models import EmailAddressRegistrationRequest, EmailAddress
# Create your tests here.
from datetime import datetime, timedelta, timezone

class RegisterTests(TestCase):
    def test_already_validated(self):
        addr = EmailAddress(Address="foo@bar.com")
        addr.save()
        req = EmailAddressRegistrationRequest(EmailAddress=addr)
        req.save()
        self.assertTrue(req.CanBeValidated())
        req.CreationDate += timedelta(days=-2)
        req.save()
        self.assertFalse(req.CanBeValidated())

        req = EmailAddressRegistrationRequest(EmailAddress=addr)
        req.save()
        self.assertTrue(req.CanBeValidated())
        req.ClickDate = datetime.now(timezone.utc)
        req.save()
        self.assertFalse(req.CanBeValidated())

class EmailTests(TestCase):
    def test_valid(self):
        self.assertFalse(EmailAddress.ValidEmail('foo'))
        self.assertFalse(EmailAddress.ValidEmail(' foo@bar.com'))
        self.assertTrue(EmailAddress.ValidEmail('foo@bar.com'))
