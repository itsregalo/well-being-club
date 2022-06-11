from django.contrib import admin
from .models import Contact, EmailSubscriber
# Register your models here.

admin.site.register(EmailSubscriber)
admin.site.register(Contact)
