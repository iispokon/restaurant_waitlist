from django.contrib import admin

from .models import Guest

# Register our model with the basic ModelAdmin
admin.site.register(Guest, admin.ModelAdmin)
