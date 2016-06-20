from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from twilio.rest import TwilioRestClient

CODE_LENGTH = 16

@python_2_unicode_compatible
class Guest(models.Model):
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=CODE_LENGTH, unique=True)
    number_of_guests = models.IntegerField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Guest: {0} (Party of {1})'.format(self.name, self.number_of_guests)

    def get_absolute_url(self):
        return reverse('view_guest', args=[str(self.code)])

    def save(self, *args, **kwargs):
        """Custom save method"""

        # generate a unique alphanumeric unique secondary key
        random = str(uuid.uuid4())  # Convert UUID format to a Python string.
        random = random.upper()
        random = random.replace("-", "")
        random = random[0:CODE_LENGTH]

        # save
        self.code = random
        super(Guest, self).save(*args, **kwargs)

        if settings.TWILIO_NUMBER:
            body = 'Hi {0} (party of {1}). Your name is on our waitlist. '.format(
                self.name,
                self.number_of_guests
            )\
                   + 'We will ping you again when your table is ready.\n'\
                   + 'Reply [edit] to change your request.\n'\
                   + 'Reply [status] to view your position on the list.'

            try:
                client = TwilioRestClient()
                message = client.messages.create(
                    body=body,
                    to=self.phone_number,
                    from_=settings.TWILIO_NUMBER
                )
            except Exception:
                # TODO handle twilio exceptions
                return
