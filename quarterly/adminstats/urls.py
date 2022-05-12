from django.urls import path
from .views import *


urlpatterns = [
    path('adminstats/', index, name='index')
]