from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import FormView, UpdateView
from django.shortcuts import redirect
from django.urls import reverse_lazy

from .forms import RegisterForm
from .models import CustomUser


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    fields = '__all__'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('portfolios')
        return super().get(*args, **kwargs)


class RegisterPage(FormView):
    template_name = 'authentication/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super().form_valid(form)    
    
    def form_invalid(self, form):
        return HttpResponse(status=400)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('portfolios')
        return super().get(*args, **kwargs)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    fields = ['email', 'display_name', 'visible']
    template_name = 'authentication/profile.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            return redirect('portfolios')
        return super().form_valid(form)

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)


class LandingPageView(TemplateView):
    template_name = "authentication/landing_page.html"


class UserPointsView(LoginRequiredMixin, DetailView):
    model = CustomUser
    context_object_name = 'user'
    template_name = 'authentication/points.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        history_all = self.object.history.all() 
        curr_history = history_all[0]
        history_cleaned = [{'date': curr_history.history_date, 'points': curr_history.points}]
        for history in history_all:
            if history.points != curr_history.points:
                history_cleaned.append({'date': history.history_date, 'points': history.points})
                curr_history = history

        context['user_history'] = history_cleaned
        
        return context
