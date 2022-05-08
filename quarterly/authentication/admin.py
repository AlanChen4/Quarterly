from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import CustomUser


admin.site.register(CustomUser, SimpleHistoryAdmin)
