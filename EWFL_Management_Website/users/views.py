from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.apps import apps

Team = apps.get_model('management', 'Team')
Feeder = apps.get_model('management', 'Feeder_Team')
lineup = apps.get_model('management', 'lineup')

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            team_name = form.cleaned_data.get('team_name')
            nation = form.cleaned_data.get('nation')
            new_team = Team(name=team_name, owner=User.objects.get(username=username))
            new_team.save()
            new_feeder_team = Feeder(name=team_name+' II', parent_club=new_team, nation=nation, team_type='youth')
            new_feeder_team.save()
            new_womens_team = Feeder(name=team_name+' W', parent_club=new_team, nation=nation, team_type='women')
            new_womens_team.save()
            new_lineup = lineup(team=new_team)
            new_lineup.save()
            messages.success(request, f'Welcome to EWFL {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
