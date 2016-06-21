"""
restaurant_waitlist  app URL Configuration
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView
from guestlist import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),
    url(r'^guestlist/', include('guestlist.urls')),

    url(r'^admin/', admin.site.urls),
]
