from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import CustomLoginView, LandingPageView, RegisterPage, UserUpdateView


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('profile/<uuid:pk>/', UserUpdateView.as_view(), name='profile'),
    path('landing/', LandingPageView.as_view(), name='landing_page'),
]