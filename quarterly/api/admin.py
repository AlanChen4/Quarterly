from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import *


admin.site.register(Portfolio, SimpleHistoryAdmin)
admin.site.register(Review, SimpleHistoryAdmin)
admin.site.register(Asset, SimpleHistoryAdmin)
