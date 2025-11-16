from django.contrib import admin
from cashify_app.models import Device, Transaction

# Register your models here.

admin.site.register(Device)
admin.site.register(Transaction)