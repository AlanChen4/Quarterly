from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from authentication.models import CustomUser


class LeaderboardView(LoginRequiredMixin, ListView):
    model = CustomUser
    context_object_name = 'users'
    template_name = 'api/leaderboard.html'

    def get_queryset(self):
        return CustomUser.objects.filter(visible=True).order_by('-points')

