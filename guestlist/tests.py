from django.test import TestCase
from guestlist.models import Guest
from mock import Mock


class GuestModelTest(TestCase):

    def test_str(self):
        mock_guest = Mock(spec=Guest)
        mock_guest.name = "Test Guest"
        mock_guest.number_of_guests = 1
        mock_guest.phone_number = "+13101231235"
        self.assertEqual(Guest.__str__(mock_guest),
                         'Guest: {0} (Party of {1})'.format(mock_guest.name, mock_guest.number_of_guests)
                         )

    def test_gest_absolute_url(self):
        guest = Guest.objects.create(name="test", number_of_guests=1, phone_number="test")
        self.assertEqual(guest.get_absolute_url(), '/guestlist/{}'.format(guest.code))

