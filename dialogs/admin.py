from django.contrib import admin
from dialogs.models import Dialog, Message


admin.site.register((Dialog, Message))
