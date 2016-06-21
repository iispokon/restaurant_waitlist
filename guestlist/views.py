from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django_twilio.decorators import twilio_view
from django.contrib import messages
from twilio import twiml
from twilio.rest import TwilioRestClient

from .models import Guest


class GuestListView(ListView):
    """List view"""

    model = Guest


class SecondaryKeyMixinView(View):
    model = Guest

    def get_object(self):
        return get_object_or_404(Guest, code=self.kwargs.get('code', None))


class GuestDetailView(SecondaryKeyMixinView, DetailView):
    """Detail view"""


class GuestCreateView(SuccessMessageMixin, CreateView):
    """Form for adding/editing guest"""

    model = Guest
    fields = ['name', 'number_of_guests', 'phone_number']
    success_message = 'Your name has been successfully added to the list.'
    success_url = reverse_lazy('list_guests')


class GuestUpdateView(SuccessMessageMixin, SecondaryKeyMixinView, UpdateView):
    """Powers a form to edit existing data"""

    fields = ['name', 'number_of_guests', 'phone_number']
    success_message = 'Successfully updated your info.'


class GuestDeleteView(SecondaryKeyMixinView, DeleteView):
    """Prompts users to confirm deletion"""

    success_url = reverse_lazy('list_guests')
    success_message = "Successfully removed from list."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(GuestDeleteView, self).delete(request, *args, **kwargs)


class GuestPageView(GuestDetailView):

    template_name = 'guestlist/page_guest.html'
    success_message = "Successfully paged guest."

    def post(self, request, code):
        guest = Guest.objects.get(code=code)
        if settings.TWILIO_NUMBER and guest.phone_number:
            body = 'Hi {0} (party of {1}). Your table is ready. '.format(
                guest.name,
                guest.number_of_guests)
            try:
                client = TwilioRestClient()
                message = client.messages.create(
                    body=body,
                    to=guest.phone_number,
                    from_=settings.TWILIO_NUMBER
                )
                messages.success(self.request, self.success_message)
            except Exception as e:
                # TODO handle twilio exceptions
                return

        return HttpResponseRedirect(reverse_lazy('list_guests'))


class GuestActionView(View):

    @method_decorator(twilio_view)
    def dispatch(self, *args, **kwargs):
        return super(GuestActionView, self).dispatch(*args, **kwargs)

    def post(self, request):
        message_from = request.POST.get('From', '')
        action = request.POST.get('Body', '').upper()
        if message_from and action in ['EDIT', 'STATUS']:
            guest = Guest.objects.get(phone_number=message_from)
            if guest.code:
                if action == 'EDIT':
                    full_url = ''.join(['http://', settings.APP_DOMAIN, reverse('edit_guest', kwargs={'code': guest.code})])

                if action == 'STATUS':
                    full_url = ''.join(['http://', settings.APP_DOMAIN, reverse('list_guests'), '?q=', guest.code])

                message = 'Follow this link to complete your request: ' + full_url
                response = twiml.Response()
                response.message(message)
                return response

        return HttpResponse("/")
