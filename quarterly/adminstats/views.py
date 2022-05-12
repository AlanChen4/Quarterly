from django.http import HttpResponse
from django.shortcuts import render

from authentication.models import CustomUser

from datetime import date, timedelta


def index(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            users = CustomUser.objects.all()
            users_week = users.filter(date_joined__range=[str(date.today() - timedelta(6)), str(date.today())])

            last_week_user_count = users.count() - users_week.count()
            if last_week_user_count == 0:
                growth = 'N/A'
            else:
                growth = ((users_week.count()) / (last_week_user_count)) * 100 

            context = {
                'week_users': users_week.count(),
                'total_users': users.count(),
                'growth': growth,
            }
            return render(request, 'adminstats/stats.html', context)
        else:
            return HttpResponse(status=405)
    else:
        return HttpResponse(status=403)