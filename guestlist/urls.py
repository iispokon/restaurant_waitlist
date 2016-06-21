from django.conf.urls import url
from django.contrib.auth.views import login, logout

from .views import GuestListView, GuestCreateView, GuestDetailView, GuestUpdateView, GuestDeleteView, GuestPageView, \
    GuestActionView


urlpatterns = [
    # Login and logout views
    url(r'^login/$', login, name='login_user'),
    url(r'^logout/$', logout, name='logout_user'),

    # List and detail views
    url(r'^$', GuestListView.as_view(), name='list_guests'),
    url(r'^(?P<code>[0-9A-Z]+)$', GuestDetailView.as_view(), name='view_guest'),

    # Create, update, delete
    url(r'^new$', GuestCreateView.as_view(), name='new_guest'),
    url(r'^(?P<code>[0-9A-Z]+)/edit$', GuestUpdateView.as_view(), name='edit_guest'),
    url(r'^(?P<code>[0-9A-Z]+)/delete$', GuestDeleteView.as_view(), name='delete_guest'),

    # User action views
    url(r'^(?P<code>[0-9A-Z]+)/page$', GuestPageView.as_view(), name='page_guest'),
    url(r'^action/$', GuestActionView.as_view(), name='guest_action'),
]
