from django.contrib.auth.decorators import login_required
from .models import Team

def user_team(request):
    if request.user.is_authenticated:
        team = Team.objects.get(owner=request.user)
        return {'user_team': team}
    return {'user_team': None}
