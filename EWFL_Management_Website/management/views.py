import time
import requests
import smtplib
from email.message import EmailMessage
from django.shortcuts import render, redirect, HttpResponseRedirect
from .models import Player, Team, Scouted_Player, offer, notification, Feeder_Team, lineup
from django.contrib.auth.decorators import login_required
import random
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DetailView
from django.core.cache import cache

def generate_player(quality, scout_level, position, tactic):
    age = random.randint(16, 33)

    tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
               'Tiki-Taka', 'Gegenpress', 'Wing Play']

    if position == 'POS':
        positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                     'CDM', 'LM', 'CM', 'RM', 'CAM',
                     'LW', 'CF', 'ST', 'RW']

        position = positions[random.randint(0, len(positions) - 1)]
    elif position == 'DEF':
        positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB']

        position = positions[random.randint(0, len(positions) - 1)]
    elif position == 'MID':
        positions = ['CDM', 'LM', 'CM', 'RM', 'CAM']

        position = positions[random.randint(0, len(positions) - 1)]
    elif position == 'FOR':
        positions = ['LW', 'CF', 'ST', 'RW']

        position = positions[random.randint(0, len(positions) - 1)]

    max_potential_increase = 33 - age

    rating_scale = {
        0.5: [25, 50],
        1.0: [30, 55],
        1.5: [35, 60],
        2.0: [40, 65],
        2.5: [45, 70],
        3.0: [50, 75],
        3.5: [55, 80],
        4.0: [60, 85],
        4.5: [65, 90],
        5.0: [70, 95]
    }

    hidden_gem = False

    player_quality = random.uniform(0, quality * 10) / 10
    player_quality = round(player_quality * 2) / 2

    if player_quality == 0.0:
        player_quality = 0.5

    if scout_level == 1:
        scout_upgrade_chance = random.randint(1, 100)

        tactic_chance = random.randint(1, 100)
        if tactic_chance > 20:
            tactic = tactics[random.randint(0, len(tactics) - 1)]

        if scout_upgrade_chance <= 10:
            upgrade = random.randint(5, 15) / 10
            upgrade = round(upgrade * 2) / 2
            player_quality += upgrade

        for i in range(2):
            hidden_gem_chance = random.randint(1, 100)

            if hidden_gem_chance <= 5:
                hidden_gem = True

            if hidden_gem:
                player_quality += 2
                hidden_gem = False

        if player_quality > 5:
            player_quality = 5

    if scout_level == 2:
        scout_upgrade_chance = random.randint(1, 100)

        tactic_chance = random.randint(1, 100)
        if tactic_chance > 30:
            tactic = tactics[random.randint(0, len(tactics) - 1)]

        if scout_upgrade_chance <= 20:
            upgrade = random.randint(0, 15) / 10
            upgrade = round(upgrade * 2) / 2
            player_quality += upgrade

        for i in range(2):
            hidden_gem_chance = random.randint(1, 100)

            if hidden_gem_chance <= 10:
                hidden_gem = True

            if hidden_gem:
                player_quality += 2
                hidden_gem = False

        if player_quality > 5:
            player_quality = 5

    if scout_level == 3:
        scout_upgrade_chance = random.randint(1, 100)

        tactic_chance = random.randint(1, 100)
        if tactic_chance > 40:
            tactic = tactics[random.randint(0, len(tactics) - 1)]

        if scout_upgrade_chance <= 30:
            upgrade = random.randint(0, 15) / 10
            upgrade = round(upgrade * 2) / 2
            player_quality += upgrade

        for i in range(2):
            hidden_gem_chance = random.randint(1, 100)

            if hidden_gem_chance <= 15:
                hidden_gem = True

            if hidden_gem:
                player_quality += 2
                hidden_gem = False

        if player_quality > 5:
            player_quality = 5

    if scout_level == 4:
        scout_upgrade_chance = random.randint(1, 100)

        tactic_chance = random.randint(1, 100)
        if tactic_chance > 50:
            tactic = tactics[random.randint(0, len(tactics) - 1)]

        if scout_upgrade_chance <= 50:
            upgrade = random.randint(0, 15) / 10
            upgrade = round(upgrade * 2) / 2
            player_quality += upgrade

        for i in range(2):
            hidden_gem_chance = random.randint(1, 100)

            if hidden_gem_chance <= 20:
                hidden_gem = True

            if hidden_gem:
                player_quality += 2
                hidden_gem = False

        if player_quality > 5:
            player_quality = 5

    if scout_level == 5:
        scout_upgrade_chance = random.randint(1, 100)

        tactic_chance = random.randint(1, 100)
        if tactic_chance > 60:
            tactic = tactics[random.randint(0, len(tactics) - 1)]

        if scout_upgrade_chance <= 60:
            upgrade = random.randint(0, 15) / 10
            upgrade = round(upgrade * 2) / 2
            player_quality += upgrade

        for i in range(2):
            hidden_gem_chance = random.randint(1, 100)

            if hidden_gem_chance <= 25:
                hidden_gem = True

            if hidden_gem:
                player_quality += 2
                hidden_gem = False

        if player_quality > 5:
            player_quality = 5.0

    player_rating = random.randint(rating_scale[player_quality][0], rating_scale[player_quality][1])
    player_potential = player_rating + random.randint(0, max_potential_increase)
    if player_potential > 99:
        player_potential = 99

    wage_scale = {
        '58,62': [2, 5],
        '63,68': [3, 8],
        '69,72': [9, 25],
        '73,78': [30, 85],
        '79,82': [100, 250],
        '83,85': [300, 450],
        '86,89': [500, 1000],
        '90,93': [1200, 1500],
        '94,96': [1800, 2000],
        '97,99': [2200, 2500],
    }

    player_wage = 0

    wage_scale_keys = wage_scale.keys()
    for i in wage_scale_keys:
        nums = i.split(',')
        if player_rating >= int(nums[0]) and player_rating <= int(nums[1]):
            player_wage = random.randint(wage_scale[i][0], wage_scale[i][1]) * 100

    contract_length = random.randint(2, 5)

    return position, age, player_rating, player_potential, tactic, player_wage, contract_length

def calculate_wage(player_rating):
    wage_scale = {
        '58,62': [2, 5],
        '63,68': [3, 8],
        '69,72': [9, 25],
        '73,78': [30, 85],
        '79,82': [100, 250],
        '83,85': [300, 450],
        '86,89': [500, 1000],
        '90,93': [1200, 1500],
        '94,96': [1800, 2000],
        '97,99': [2200, 2500],
    }

    player_wage = 0

    wage_scale_keys = wage_scale.keys()
    for i in wage_scale_keys:
        nums = i.split(',')
        if player_rating >= int(nums[0]) and player_rating <= int(nums[1]):
            player_wage = random.randint(wage_scale[i][0], wage_scale[i][1]) * 100

    if player_wage < 200:
        player_wage = 50

    return player_wage

def calculate_value(pos, age, ovr, pot):
    position_effect = 0

    pos = pos.split('/')
    pos = pos[0]

    if pos == 'GK':
        position_effect = 8
    if pos == 'CB':
        position_effect = 7
    if pos == 'LB' or pos == 'LWB' or pos == 'RB' or pos == 'RWB':
        position_effect = 6
    if pos == 'CDM':
        position_effect = 4
    if pos == 'CM' or pos == 'CAM':
        position_effect = 3
    if pos == 'LM' or pos == 'LW' or pos == 'RM' or pos == 'RW':
        position_effect = 2
    if pos == 'ST' or pos == 'CF':
        position_effect = 0

    am = 0.7 + ((41 - (99 - ovr)) * 0.05)
    pm = 0.9 + ((41 - (99 - pot)) * 0.0625)

    fm = (41 - (99 - ovr)) * 6250

    if fm < 0:
        chance = random.randint(1, 100)
        if chance % 2 == 0:
            return 0.0
        return 0.5

    discount_chance = random.randint(1, 100)
    discount = 0

    discount = random.randint(1, 100)

    if discount <= 5:
        discount = 10
    elif discount > 5 and discount <= 15:
        discount = 8
    elif discount > 15 and discount <= 35:
        discount = 6
    elif discount > 35 and discount <= 60:
        discount = 4
    elif discount > 60 and discount <= 90:
        discount = 2
    else:
        discount = 0

    value = (((ovr * 0.5) + (pot * 0.8)) * am * pm) * fm
    age_effect = (17 - (33 - age)) * ((value / 20) / 2)
    position_effect = ((value / 20) / 2) * position_effect
    discount = ((value / 20) / 2) * discount
    value -= age_effect
    value -= position_effect
    value -= discount
    value = round(value / 500000) * 500000 / 1000000

    return value

def get_position_training_values(current_position, training_position):
    position_training_times = {
        "GK": {
            "LWB": [72, 10],
            "LB": [72, 10],
            "CB": [72, 10],
            "RB": [72, 10],
            "RWB": [72, 10],
            "CDM": [72, 10],
            "CM": [72, 10],
            "LM": [72, 10],
            "RM": [72, 10],
            "CAM": [72, 10],
            "LW": [72, 10],
            "RW": [72, 10],
            "CF": [72, 10],
            "ST": [72, 10]
        },
        "LWB": {
            "GK": [72, 10],
            "LB": [2, 100],
            "CB": [17, 80],
            "RB": [12, 90],
            "RWB": [12, 90],
            "CDM": [30, 60],
            "CM": [42, 50],
            "LM": [15, 75],
            "RM": [15, 75],
            "CAM": [62, 35],
            "CF": [67, 30],
            "LW": [15, 75],
            "RW": [15, 75],
            "ST": [69, 30]
        },
        "LB": {
            "GK": [72, 10],
            "LWB": [2, 100],
            "CB": [15, 80],
            "RB": [10, 90],
            "RWB": [12, 90],
            "CDM": [30, 60],
            "CM": [40, 50],
            "LM": [15, 75],
            "RM": [15, 75],
            "CAM": [62, 35],
            "CF": [67, 30],
            "LW": [15, 75],
            "RW": [15, 75],
            "ST": [69, 30]
        },
        "RB": {
            "GK": [72, 10],
            "LWB": [12, 90],
            "LB": [10, 90],
            "CB": [15, 80],
            "RWB": [2, 100],
            "CDM": [30, 60],
            "CM": [40, 50],
            "LM": [15, 75],
            "RM": [15, 75],
            "CAM": [62, 35],
            "CF": [67, 30],
            "LW": [15, 75],
            "RW": [15, 75],
            "ST": [69, 30]
        },
        "RWB": {
            "GK": [72, 10],
            "LWB": [12, 90],
            "LB": [10, 90],
            "CB": [15, 80],
            "RB": [2, 100],
            "CDM": [30, 60],
            "CM": [40, 50],
            "LM": [15, 75],
            "RM": [15, 75],
            "CAM": [62, 35],
            "CF": [67, 30],
            "LW": [15, 75],
            "RW": [15, 75],
            "ST": [69, 30]
        },
        "CB": {
            "GK": [72, 10],
            "LWB": [17, 80],
            "LB": [15, 80],
            "RB": [15, 80],
            "RWB": [17, 80],
            "CDM": [15, 75],
            "CM": [27, 65],
            "LM": [57, 40],
            "RM": [57, 40],
            "CAM": [37, 50],
            "CF": [43, 40],
            "LW": [57, 40],
            "RW": [57, 40],
            "ST": [45, 40]
        },
        "CDM": {
            "GK": [72, 10],
            "LWB": [30, 60],
            "LB": [30, 60],
            "CB": [15, 75],
            "RB": [30, 60],
            "RWB": [30, 60],
            "CM": [12, 85],
            "LM": [42, 50],
            "RM": [42, 50],
            "CAM": [20, 65],
            "CF": [25, 50],
            "LW": [42, 50],
            "RW": [42, 50],
            "ST": [27, 50]
        },
        "CM": {
            "GK": [72, 10],
            "LWB": [42, 50],
            "LB": [42, 50],
            "CB": [27, 65],
            "RB": [42, 50],
            "RWB": [42, 50],
            "CDM": [12, 85],
            "LM": [30, 60],
            "RM": [30, 60],
            "CAM": [10, 80],
            "CF": [15, 65],
            "LW": [30, 60],
            "RW": [30, 60],
            "ST": [17, 65]
        },
        "CAM": {
            "GK": [72, 10],
            "LWB": [52, 40],
            "LB": [52, 40],
            "CB": [37, 50],
            "RB": [52, 40],
            "RWB": [52, 40],
            "CDM": [20, 65],
            "CM": [10, 80],
            "LM": [17, 65],
            "RM": [17, 65],
            "CF": [5, 80],
            "LW": [17, 65],
            "RW": [17, 65],
            "ST": [7, 80]
        },
        "LM": {
            "GK": [72, 10],
            "LWB": [15, 75],
            "LB": [15, 75],
            "CB": [57, 40],
            "RB": [15, 75],
            "RWB": [15, 75],
            "CDM": [42, 50],
            "CM": [30, 60],
            "RM": [10, 90],
            "CAM": [17, 65],
            "CF": [17, 80],
            "LW": [2, 100],
            "RW": [12, 90],
            "ST": [19, 80]
        },
        "RM": {
            "GK": [72, 10],
            "LWB": [15, 75],
            "LB": [15, 75],
            "CB": [57, 40],
            "RB": [15, 75],
            "RWB": [15, 75],
            "CDM": [42, 50],
            "CM": [30, 60],
            "LM": [10, 90],
            "CAM": [17, 65],
            "CF": [17, 80],
            "LW": [12, 90],
            "RW": [2, 100],
            "ST": [19, 80]
        },
        "LW": {
            "GK": [72, 10],
            "LWB": [15, 75],
            "LB": [15, 75],
            "CB": [57, 40],
            "RB": [15, 75],
            "RWB": [15, 75],
            "CDM": [42, 50],
            "CM": [30, 60],
            "LM": [2, 100],
            "RM": [12, 90],
            "CAM": [17, 65],
            "CF": [17, 80],
            "RW": [10, 90],
            "ST": [19, 80]
        },
        "RW": {
            "GK": [72, 10],
            "LWB": [15, 75],
            "LB": [15, 75],
            "CB": [57, 40],
            "RB": [15, 75],
            "RWB": [15, 75],
            "CDM": [42, 50],
            "CM": [30, 60],
            "LM": [12, 90],
            "RM": [2, 100],
            "CAM": [17, 65],
            "CF": [17, 80],
            "LW": [10, 90],
            "ST": [19, 80]
        },
        "CF": {
            "GK": [72, 10],
            "LWB": [67, 30],
            "LB": [67, 30],
            "CB": [43, 40],
            "RB": [67, 30],
            "RWB": [67, 30],
            "CDM": [25, 50],
            "CM": [15, 65],
            "LM": [10, 80],
            "RM": [10, 80],
            "CAM": [5, 80],
            "LW": [10, 80],
            "RW": [10, 80],
            "ST": [2, 100]
        },
        "ST": {
            "GK": [72, 10],
            "LWB": [69, 30],
            "LB": [69, 30],
            "CB": [45, 40],
            "RB": [69, 30],
            "RWB": [69, 30],
            "CDM": [27, 50],
            "CM": [17, 65],
            "LM": [10, 80],
            "RM": [10, 80],
            "CAM": [7, 80],
            "LW": [10, 80],
            "RW": [10, 80],
            "CF": [2, 100]
        },
    }
    return position_training_times[current_position][training_position][0], position_training_times[current_position][training_position][1]

def get_tactic_training_values(current_tactic, training_tactic):
    tactic_training_times = {
        "Balanced": {
            "Catenaccio": [20, 70],
            "Gegennaccio": [20, 70],
            "Route One": [20, 70],
            "Counter-Attack": [20, 70],
            "Control Possession": [20, 70],
            "Gegenpress": [20, 70],
            "Tiki-Taka": [20, 70],
            "Wing Play": [20, 70],
        },
        "Catenaccio": {
            "Balanced": [20, 70],
            "Gegennaccio": [20, 90],
            "Route One": [30, 50],
            "Counter-Attack": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Gegennaccio": {
            "Balanced": [20, 70],
            "Catenaccio": [20, 90],
            "Route One": [30, 50],
            "Counter-Attack": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Route One": {
            "Balanced": [20, 70],
            "Counter-Attack": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Counter-Attack": {
            "Balanced": [20, 70],
            "Route One": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Control Possession": {
            "Balanced": [20, 70],
            "Gegenpress": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Counter-Attack": [30, 50],
            "Route One": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Gegenpress": {
            "Balanced": [20, 70],
            "Control Possession": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Counter-Attack": [30, 50],
            "Route One": [30, 50],
            "Tiki-Taka": [30, 50],
            "Wing Play": [30, 50],
        },
        "Tiki-Taka": {
            "Balanced": [20, 70],
            "Wing Play": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Counter-Attack": [30, 50],
            "Route One": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
        },
        "Wing Play": {
            "Balanced": [20, 70],
            "Tiki-Taka": [20, 90],
            "Gegennaccio": [30, 50],
            "Catenaccio": [30, 50],
            "Counter-Attack": [30, 50],
            "Route One": [30, 50],
            "Control Possession": [30, 50],
            "Gegenpress": [30, 50],
        },
    }
    return tactic_training_times[current_tactic][training_tactic][0], tactic_training_times[current_tactic][training_tactic][1]

def home(request):
    return render(request, 'management/site-home.html')

@login_required
def advance_week(request):
    user = request.user

    if not user.is_superuser:
        return redirect('site-home')

    players = Player.objects.all()

    for p in players:
        if p.training_position_time > 0:
            p.training_position_time -= 1

            if p.training_position_time == 0:
                training_position_chance = random.randint(0,100)
                if training_position_chance <= p.training_position_chance:
                    p.position += '/' + p.training_position
                    new_notification = notification(team=p.team,
                                                    message=f"{p.name}'s position training for {p.training_position} was successful.")
                    new_notification.save()
                else:
                    new_notification = notification(team=p.team,
                                                    message=f"{p.name}'s position training for {p.training_position} was unsuccessful.")
                    new_notification.save()

                p.training_position = 'N/A'
                p.training_position_chance = 0

        if p.training_tactic_time > 0:
            p.training_tactic_time -= 1

            if p.training_tactic_time == 0:
                training_tactic_chance = random.randint(0,100)
                if training_tactic_chance <= p.training_tactic_chance:
                    p.tactic = p.training_tactic

                    new_notification = notification(team=p.team,
                                                    message=f"{p.name}'s tactic training for {p.training_tactic} was successful.")
                    new_notification.save()
                else:
                    new_notification = notification(team=p.team,
                                                    message=f"{p.name}'s tactic training for {p.training_tactic} was unsuccessful.")
                    new_notification.save()

                p.training_tactic = 'N/A'
                p.training_tactic_chance = 0

        if p.training_tactic_time == 0 and p.training_tactic_time == 0:
            p.training = False

        p.save()

    return redirect('admin-panel')

@login_required
def manage_team(request):
    team = Team.objects.get(owner=request.user)
    players = Player.objects.filter(team=team)
    loaned_players = Player.objects.filter(loaned_to=team.name)
    players = players.union(loaned_players)
    feeder_teams = Feeder_Team.objects.filter(parent_club=team)

    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    sorted_players = []

    for i in positions:
        for x in players:
            position = x.position.split('/')[0]
            if position == i:
                sorted_players.append(x)


    context =  {
        'team_name': team.name,
        'players': sorted_players,
        'transfer_budget': team.transfer_budget,
        'wage_budget': team.wage_budget_remaining,
        'facilities_budget': team.facilities_budget,
        'stadium': team.stadium,
        'scout': team.scout,
        'training_facilities': team.training_facilties,
        'youth_academy': team.youth_academy,
        'merchandise': team.merchandise,
        'director_of_football': team.director_of_football,
        'assistant_manager': team.assistant_manager,
        'goalkeeping_coach': team.goalkeeping_coach,
        'defending_coach': team.defending_coach,
        'midfield_coach': team.midfield_coach,
        'attacking_coach': team.attacking_coach,
        'set_piece_coach': team.set_piece_coach,
        'physiotherapist': team.physiotherapist,
        'feeder_teams' : feeder_teams
    }

    return render(request, 'management/manage-team.html', context)

@login_required
def scout_players(request):
    countries = [
        "Afghanistan", "Aland", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
        "Antarctica", "Antigua & Barbuda", "Argentina",
        "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
        "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire", "Bosnia & Herzegovina",
        "Botswana", "Bouvet Island", "Brazil", "British Virgin Islands", "Brunei",
        "Bulgaria", "Burkina Faso", "Burundi",
        "Cambodia", "Cameroon", "Canada", "Cape Verde", "Catalonia", "Cayman Islands", "Central African Republic",
        "Chad",
        "Chile", "China", "Christmas Island", "Cocos Islands", "Colombia", "Comoros", "Congo", "Cook Islands",
        "Costa Rica",
        "Croatia", "Cuba", "Curacao", "Cyprus",
        "Czech Republic", "Denmark", "Djibouti", "Dominican Republic", "Dominica", "DR Congo",
        "Ecuador", "Egypt", "El Salvador", "England", "Equatorial Guinea", "Eritrea", "Estonia",
        "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana",
        "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guadeloupe", "Guatemala",
        "Guernsey", "Guinea",
        "Guinea-Bissau", "Guyana", "Haiti", "Heard Island", "Holy See", "Honduras", "Hong Kong", "Hungary",
        "Iceland",
        "Isle of Man", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
        "Jersey",
        "Kazakhstan", "Kenya", "Kirain", "Kiribati", "Kosovo", "Kurdistan", "Kuwait", "Kyrgyzstan", "Laos",
        "Latvia",
        "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mapuche", "Martinique", "Mauritania",
        "Mauritius", "Manchuoko", "Marshall Islands", "Mayotte", "Mcdonald Islands", "Mexico", "Micronesia",
        "Moldova",
        "Monaco", "Mongolia", "Montenegro", "Montserrat",
        "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia",
        "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Korea", "North Macedonia",
        "Northern Ireland", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palestine", "Palau",
        "Panama",
        "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
        "Republic of Samoa", "Romania", "Russia", "Reunion", "Rwanda", "Saint Helena", "Saint Kitts & Nevis",
        "Saint Lucia",
        "Saint Pierre & Miquelon",
        "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia",
        "Scotland", "Sealand", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Sint Maarten",
        "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sandwich Islands", "South Sudan",
        "Spain",
        "Sri Lanka", "Sudan",
        "Suriname", "Svalbard", "Sweden", "Switzerland", "Syria", "Tahiti", "Taiwan", "Tajikistan", "Tanzania",
        "Thailand", "Timor Leste", "Togo", "Tokelau", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
        "Turkmenistan", "Turks & Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "Uruguay", "US Virgin Islands", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wales",
        "Wallis & Futuna", "Western Sahara", "Yemen",
        "Zambia", "Zimbabwe"
    ]

    tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Control Possession',
               'Tiki-Taka', 'Gegenpress', 'Wing Play']

    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    context ={
        'countries': countries,
        'tactics' : tactics,
        'positions' : positions
    }

    return render(request, 'management/scout-players.html', context)

@login_required
def scouted_players(request):
    team = Team.objects.get(owner=request.user)
    players = Scouted_Player.objects.filter(team=team)
    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    sorted_players = []

    for i in positions:
        for x in players:
            position = x.position.split('/')[0]
            if position == i:
                sorted_players.append(x)

    context =  {
        'players': sorted_players,
        'amount': len(Scouted_Player.objects.filter(team=team))
    }

    return render(request, 'management/scouted-players.html', context)

@login_required
def expired_players(request):
    team = Team.objects.get(owner=request.user)
    players = Player.objects.filter(team=team)
    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    sorted_players = []

    for i in positions:
        for x in players:
            position = x.position.split('/')[0]
            if position == i and x.contract_length == 0 and not x.free_agent:
                sorted_players.append(x)

    context =  {
        'players': sorted_players
    }

    return render(request, 'management/expired-players.html', context)

@login_required
def free_agents(request):
    players = Player.objects.all()
    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    sorted_players = []

    for i in positions:
        for x in players:
            position = x.position.split('/')[0]
            if position == i and x.free_agent:
                sorted_players.append(x)

    context = {
        'players': sorted_players
    }

    return render(request, 'management/free-agents.html', context)

@login_required
def no_scout_reports_remaining(request):
    return render(request, 'management/no-scout-reports.html')

@login_required
def too_many_players_scouted(request):
    return render(request, 'management/too-many-players-scouted.html')

@login_required
def scout_report(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        position = request.POST.get('position')
        nationality = request.POST.get('nationality')
        tactic = request.POST.get('tactic')

        country_quality = {
            "Afghanistan": 2,
            "Aland": 0.5,
            "Albania": 2.5,
            "Algeria": 4,
            "American Samoa": 0.5,
            "Andorra": 2,
            "Angola": 2.5,
            "Anguilla": 0.5,
            "Antarctica": 0.5,
            "Antigua & Barbuda": 0.5,
            "Argentina": 5,
            "Armenia": 1,
            "Aruba": 1.5,
            "Australia": 3.5,
            "Austria": 3.5,
            "Azerbaijan": 1.5,
            "Bahamas": 0.5,
            "Bahrain": 1,
            "Bangladesh": 0.5,
            "Barbados": 1,
            "Belarus": 1.5,
            "Belgium": 4.5,
            "Belize": 0.5,
            "Benin": 1,
            "Bermuda": 1.5,
            "Bhutan": 0.5,
            "Bolivia": 2.5,
            "Bonaire": 0.5,
            "Bosnia & Herzegovina": 2.5,
            "Botswana": 1,
            "Bouvet Island": 0.5,
            "Brazil": 5,
            "Brunei": 0.5,
            "Bulgaria": 2,
            "Burkina Faso": 2.5,
            "Burundi": 0.5,
            "Cambodia": 0.5,
            "Cameroon": 3.5,
            "Canada": 3.5,
            "Cape Verde": 2.5,
            "Cayman Islands": 0.5,
            "Central African Republic": 1.5,
            "Chad": 0.5,
            "Chile": 3.5,
            "China": 3.5,
            "Christmas Island": 0.5,
            "Cocos Islands": 0.5,
            "Colombia": 3.5,
            "Comoros": 0.5,
            "Congo": 1,
            "DR Congo": 2.5,
            "Catalonia": 1.5,
            "Cook Islands": 0.5,
            "Costa Rica": 3,
            "Croatia": 4,
            "Cuba": 1.5,
            "Cyprus": 1,
            "Czech Republic": 2,
            "Denmark": 3.5,
            "Djibouti": 0.5,
            "Dominica": 1,
            "Dominican Republic": 1.5,
            "Ecuador": 2.5,
            "Egypt": 3,
            "El Salvador": 2.5,
            "Equatorial Guinea": 1,
            "Eritrea": 0.5,
            "Estonia": 1,
            "Ethiopia": 0.5,
            "Falkland Islands": 0.5,
            "Faroe Islands": 0.5,
            "Fiji": 0.5,
            "Finland": 1.5,
            "France": 5,
            "French Guiana": 0.5,
            "Gabon": 0.5,
            "Gambia": 1,
            "Georgia": 1.5,
            "Germany": 5,
            "Ghana": 3,
            "Gibraltar": 0.5,
            "Greece": 2.5,
            "Greenland": 0.5,
            "Grenada": 0.5,
            "Guadeloupe": 0.5,
            "Guam": 0.5,
            "Guatemala": 1.5,
            "Guernsey": 0.5,
            "Guinea": 2,
            "Guinea-Bissau": 1.5,
            "Guyana": 0.5,
            "Haiti": 2,
            "Heard Island": 0.5,
            "Holy See": 0.5,
            "Honduras": 2.5,
            "Hong Kong": 1.5,
            "Hungary": 1.5,
            "Iceland": 2,
            "India": 2,
            "Indonesia": 1,
            "Iran": 3.5,
            "Iraq": 1,
            "Ireland": 2.5,
            "Isle of Man": 0.5,
            "Israel": 1,
            "Italy": 5,
            "Ivory Coast": 3,
            "Jamaica": 3,
            "Japan": 4.5,
            "Jersey": 0.5,
            "Jordan": 1,
            "Kazakhstan": 1,
            "Kenya": 1,
            "Kirain": 0.5,
            "Kiribati": 0.5,
            "Kosovo": 2.5,
            "Kurdistan": 0.5,
            "North Korea": 1.5,
            "South Korea": 4,
            "Kuwait": 1,
            "Kyrgyzstan": 0.5,
            "Laos": 1,
            "Latvia": 1,
            "Lebanon": 1.5,
            "Lesotho": 0.5,
            "Liberia": 0.5,
            "Libya": 0.5,
            "Liechtenstein": 0.5,
            "Lithuania": 0.5,
            "Luxembourg": 0.5,
            "Macau": 0.5,
            "Madagascar": 0.5,
            "Malawi": 0.5,
            "Malaysia": 0.5,
            "Maldives": 0.5,
            "Mali": 2,
            "Malta": 1,
            "Manchuoko": 0.5,
            "Mapuche": 0.5,
            "Marshall Islands": 0.5,
            "Martinique": 0.5,
            "Mauritania": 1,
            "Mauritius": 0.5,
            "Mayotte": 0.5,
            "Mcdonald Islands": 0.5,
            "Mexico": 4,
            "Micronesia": 0.5,
            "Moldova": 1,
            "Monaco": 0.5,
            "Mongolia": 0.5,
            "Montserrat": 1,
            "Morocco": 4,
            "Mozambique": 0.5,
            "Montenegro": 1,
            "Myanmar": 0.5,
            "Namibia": 1,
            "Nauru": 0.5,
            "Nepal": 0.5,
            "Netherlands": 4,
            "New Caledonia": 3,
            "New Zealand": 3,
            "Nicaragua": 1.5,
            "Niger": 1,
            "Nigeria": 4,
            "Niue": 0.5,
            "Norfolk Island": 0.5,
            "Northern Mariana Islands": 0.5,
            "North Macedonia": 1.5,
            "Norway": 2.5,
            "Oman": 1,
            "Pakistan": 1,
            "Palau": 0.5,
            "Palestine": 1,
            "Panama": 2.5,
            "Papua New Guinea": 1.5,
            "Paraguay": 2.5,
            "Peru": 2.5,
            "Philippines": 1,
            "Pitcairn": 0.5,
            "Poland": 3,
            "Portugal": 4.5,
            "Puerto Rico": 2,
            "Qatar": 2.5,
            "Reunion": 0.5,
            "Romania": 3,
            "Russia": 2.5,
            "Rwanda": 1,
            "Saint Helena": 0.5,
            "Saint Kitts & Nevis": 1,
            "Saint Lucia": 0.5,
            "Saint Pierre & Miquelon": 0.5,
            "Saint Vincent & the Grenadines": 0.5,
            "Samoa": 0.5,
            "San Marino": 2,
            "Sao Tome & Principe": 0.5,
            "Saudi Arabia": 3,
            "Sealand": 0.5,
            "Senegal": 4,
            "Serbia": 3,
            "Seychelles": 0.5,
            "Sierra Leone": 0.5,
            "Singapore": 0.5,
            "Sint Maarten": 0.5,
            "Slovakia": 2,
            "Slovenia": 2,
            "Solomon Islands": 1,
            "Somalia": 0.5,
            "South Africa": 2.5,
            "South Sandwich Islands": 0.5,
            "Spain": 5,
            "Sri Lanka": 1,
            "Sudan": 0.5,
            "Suriname": 1.5,
            "Svalbard": 0.5,
            "Eswatini": 0.5,
            "Sweden": 3,
            "Switzerland": 3,
            "Syria": 1,
            "Tahiti": 2,
            "Taiwan": 1,
            "Tajikistan": 1,
            "Tanzania": 1.5,
            "Thailand": 1.5,
            "Timor Leste": 0.5,
            "Togo": 1.5,
            "Tokelau": 0.5,
            "Tonga": 1,
            "Trinidad & Tobago": 2,
            "Tunisia": 2.5,
            "Turkey": 2.5,
            "Turkmenistan": 0.5,
            "Turks & Caicos Islands": 0.5,
            "Tuvalu": 0.5,
            "Uganda": 1,
            "Ukraine": 2.5,
            "United Arab Emirates": 1.5,
            "England": 5,
            "Scotland": 2.5,
            "Wales": 2,
            "Northern Ireland": 1.5,
            "Uruguay": 4,
            "Uzbekistan": 1,
            "Vanuatu": 0.5,
            "Venezuela": 2.5,
            "Vietnam": 1.5,
            "British Virgin Islands": 0.5,
            "US Virgin Islands": 0.5,
            "Wallis & Futuna": 0.5,
            "Western Sahara": 0.5,
            "Yemen": 1,
            "Zambia": 1,
            "Zimbabwe": 1
        }

        countries = [
            "Afghanistan", "Aland", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
            "Antarctica", "Antigua & Barbuda", "Argentina",
            "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
            "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire", "Bosnia & Herzegovina",
            "Botswana", "Bouvet Island", "Brazil", "British Virgin Islands", "Brunei",
            "Bulgaria", "Burkina Faso", "Burundi",
            "Cambodia", "Cameroon", "Canada", "Cape Verde", "Catalonia", "Cayman Islands", "Central African Republic",
            "Chad",
            "Chile", "China", "Christmas Island", "Cocos Islands", "Colombia", "Comoros", "Congo", "Cook Islands",
            "Costa Rica",
            "Croatia", "Cuba", "Curacao", "Cyprus",
            "Czech Republic", "Denmark", "Djibouti", "Dominican Republic", "Dominica", "DR Congo",
            "Ecuador", "Egypt", "El Salvador", "England", "Equatorial Guinea", "Eritrea", "Estonia",
            "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana",
            "Gabon", "Gambia", "Georgia",
            "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guadeloupe", "Guatemala",
            "Guernsey", "Guinea",
            "Guinea-Bissau", "Guyana", "Haiti", "Heard Island", "Holy See", "Honduras", "Hong Kong", "Hungary",
            "Iceland",
            "Isle of Man", "India",
            "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
            "Jersey",
            "Kazakhstan", "Kenya", "Kirain", "Kiribati", "Kosovo", "Kurdistan", "Kuwait", "Kyrgyzstan", "Laos",
            "Latvia",
            "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
            "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mapuche", "Martinique", "Mauritania",
            "Mauritius", "Manchuoko", "Marshall Islands", "Mayotte", "Mcdonald Islands", "Mexico", "Micronesia",
            "Moldova",
            "Monaco", "Mongolia", "Montenegro", "Montserrat",
            "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia",
            "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Korea", "North Macedonia",
            "Northern Ireland", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palestine", "Palau",
            "Panama",
            "Papua New Guinea",
            "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
            "Republic of Samoa", "Romania", "Russia", "Reunion", "Rwanda", "Saint Helena", "Saint Kitts & Nevis",
            "Saint Lucia",
            "Saint Pierre & Miquelon",
            "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia",
            "Scotland", "Sealand", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Sint Maarten",
            "Slovakia", "Slovenia",
            "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sandwich Islands", "South Sudan",
            "Spain",
            "Sri Lanka", "Sudan",
            "Suriname", "Svalbard", "Sweden", "Switzerland", "Syria", "Tahiti", "Taiwan", "Tajikistan", "Tanzania",
            "Thailand", "Timor Leste", "Togo", "Tokelau", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
            "Turkmenistan", "Turks & Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
            "Uruguay", "US Virgin Islands", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wales",
            "Wallis & Futuna", "Western Sahara", "Yemen",
            "Zambia", "Zimbabwe"
        ]

        player_quality = country_quality[nationality]

        team = Team.objects.get(owner=request.user)
        team_name = team.name
        scout_level = team.scout
        dof_level = team.director_of_football
        scouted_players = []

        if team.scout_reports_remaining < 1:
            return render(request, 'management/no-scout-reports.html')
        if len(Scouted_Player.objects.filter(team=team)) >= 96:
            return render(request, 'management/too-many-players-scouted.html')
        else:
            team.scout_reports_remaining -= 1
            team.save()

        for i in range(5):
            current_player = generate_player(player_quality, scout_level, position, tactic)

            current_player_value = calculate_value(current_player[0], current_player[1], current_player[2], current_player[3])

            dof_discount_chance = random.randint(1,100)

            dof_chances_by_level = {
                0 : 0,
                1 : 3,
                2 : 8,
                3 : 10,
                4 : 15,
                5 : 20,
            }

            discounts = [5,10,15,20,25]

            if dof_chances_by_level[dof_level] >= dof_discount_chance:
                discount = discounts[random.randint(0,len(discounts)-1)]

                current_player_value = current_player_value - round((current_player_value * (discount / 100)))

            skill_points_chance = random.randint(1,100)
            can_be_loaned_chance = random.randint(1,100)
            can_be_loaned = False
            loaned_wage = 0
            if can_be_loaned_chance <= 5:
                can_be_loaned = True
                loaned_wage_chance = random.randint(1,100)
                if loaned_wage_chance <= 100:
                    loaned_wage = 50
                if loaned_wage_chance <= 50:
                    loaned_wage = 0
                if loaned_wage_chance <= 20:
                    loaned_wage = 25
                if loaned_wage_chance <= 5:
                    loaned_wage = 75

                loaned_wage_buffer = loaned_wage
                loaned_wage = current_player[5] - round((loaned_wage * current_player[5]) / 100)

                print(f'wage is: {current_player[5]} discount is: {loaned_wage_buffer} loaned wage is: {loaned_wage}')

            skill_points = 0
            if skill_points_chance > 75:
                skill_points = random.randint(0,10)
            scouted_player = Scouted_Player(team=team_name, position=current_player[0], age=current_player[1], overall=current_player[2], potential=current_player[3],
                                            tactic=current_player[4], wage=current_player[5], contract_length=current_player[6], nationality=nationality, value=current_player_value,
                                            skill_points=skill_points, can_be_loaned=can_be_loaned, loaned_wage=loaned_wage)

            scouted_player.save()
            scouted_players.append(scouted_player)

        context = {
            'players': scouted_players,
            'countries': countries,
        }

        return render(request, 'management/scout-report.html', context)

@login_required
def signed_player(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        player_id = request.POST.get('player_id')
        scouted_player = Scouted_Player.objects.get(pk=player_id)

        scouted_player.sign()

        return redirect('signed-player')
    return redirect('manage-team')

class PlayerUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Player
    fields = ['name']

    def test_func(self):
        player = self.get_object()
        team = player.team
        if self.request.user == team.owner:
            return True
        return False

class PlayerDetailView(DetailView):
    model = Player

    template_name = 'management/player_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        team = Team.objects.get(owner=self.request.user)
        context['feeder_teams'] = Feeder_Team.objects.filter(parent_club=team)
        return context

def team_detail(request):
    team_name = request.POST.get('team_name')

    team = Team.objects.get(name=team_name)
    players = Player.objects.filter(team=team)

    user = request.user

    if user.is_authenticated:
        user_team = Team.objects.get(owner=request.user)
        budget = user_team.transfer_budget

        context = {
            'team': team,
            'players': players,
            'user': user,
            'budget': budget
        }
    else:
        context = {
            'team': team,
            'players': players,
        }

    return render(request, 'management/team_detail.html', context)

@login_required()
def sell_player(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        value = request.POST.get('value')
        player.sell_player(value)

        return redirect('player-sell')
    return redirect('manage-team')

@login_required()
def sell_player_nego(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        player_id = request.POST.get('player_id')

        player = cache.get(f'player_{player_id}')
        values = cache.get(f'values_{player_id}')

        if player is None:
            player = Player.objects.get(pk=player_id)

            value = calculate_value(player.position, player.age, player.overall, player.potential)

            offers = [0.0, 10.0, 15.0, 20.0, 25.0]
            values = [value, value, value]

            if value > 0.5:
                for i in range(3):
                    higher_or_lower = random.randint(1,100)
                    offer = offers[random.randint(0,4)]

                    if offer > 0.0:
                        if higher_or_lower > 70:
                            new_value = value + round((offer * value) / 100)
                            values[i] = round(new_value * 2) / 2
                        else:
                            new_value = value - round((offer * value) / 100)
                            values[i] = round(new_value * 2) / 2

            cache.set(f'player_{player_id}', player, timeout=86400)
            cache.set(f'values_{player_id}', values, timeout=86400)

        context = {
            'values': values,
            'player_id': player_id
        }

        return render(request, 'management/player-negotiate-sell.html', context)
    return redirect('manage-team')

@login_required()
def remove_scouted_player(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Scouted_Player.objects.get(id=player_id)

        if player is not None:
            player.delete()

    return redirect('scouted-players')

@login_required()
def budget_details(request):
    team = Team.objects.get(owner=request.user)

    transfer_budget = team.transfer_budget
    wage_budget = team.wage_budget_remaining
    facilities_budget = team.facilities_budget

    context = {
        'team': team,
        'transfer_budget': transfer_budget,
        'facilities_budget': facilities_budget,
        'wage_budget': wage_budget
    }

    return render(request, 'management/budgets.html', context)


@login_required()
def budget_transfer(request):
    team = Team.objects.get(owner=request.user)

    transfer_budget = team.transfer_budget
    wage_budget = team.wage_budget_remaining

    if request.method == 'POST':
        budget_to_transfer_from = request.POST.get('budget_from')
        budget_to_transfer_to = request.POST.get('budget_to')

        if budget_to_transfer_to is not None:
            if budget_to_transfer_from == 'Transfer':
                if budget_to_transfer_to == 'Wage' and transfer_budget >= 0.5:
                    team.deposit_wage_budget(250)
                    team.withdraw_transfer_budget(0.5)
                elif budget_to_transfer_to == 'Facilities' and transfer_budget >= 0.5:
                    team.deposit_facilities_budget(0.5)
                    team.withdraw_transfer_budget(0.5)
            if budget_to_transfer_from == 'Wage':
                if budget_to_transfer_to == 'Transfer' and wage_budget >= 250:
                    team.deposit_transfer_budget(0.5)
                    team.withdraw_wage_budget(250)
                elif budget_to_transfer_to == 'Facilities' and wage_budget >= 0.5:
                    team.deposit_facilities_budget(0.5)
                    team.withdraw_wage_budget(250)

    return redirect('budgets')

@login_required()
def facilities_detail(request):
    team = Team.objects.get(owner=request.user)

    context = {
        'facilities_budget': team.facilities_budget,
        'stadium': team.stadium,
        'training_facilities': team.training_facilties,
        'youth_academy': team.youth_academy,
        'merchandise': team.merchandise
    }

    return render(request, 'management/facilities.html', context)

@login_required()
def facilities_upgrade(request):
    team = Team.objects.get(owner=request.user)

    if request.method == 'POST':
        facility = request.POST.get('facility')

        if facility is not None:
            if facility == 'stadium':
                team.upgrade_stadium()
            elif facility == 'training':
                team.upgrade_training_facilities()
            elif facility == 'youth':
                team.upgrade_youth_academy()
            elif facility == 'merchandise':
                team.upgrade_merchandise()

    return redirect('facilities')

@login_required()
def staff_detail(request):
    team = Team.objects.get(owner=request.user)

    context = {
        'facilities_budget': team.facilities_budget,
        'scout': team.scout,
        'dof': team.director_of_football,
        'assistant_manager': team.assistant_manager,
        'gk_coach': team.goalkeeping_coach,
        'def_coach': team.defending_coach,
        'mid_coach': team.midfield_coach,
        'att_coach': team.attacking_coach,
        'set_piece_coach': team.set_piece_coach
    }

    return render(request, 'management/staff.html', context)

@login_required()
def staff_upgrade(request):
    team = Team.objects.get(owner=request.user)

    if request.method == 'POST':
        staff = request.POST.get('staff')

        if staff is not None:
            if staff == 'scout':
                team.upgrade_scout()
            elif staff == 'dof':
                team.upgrade_director_of_football()
            elif staff == 'assistant_manager':
                team.upgrade_assistant_manager()
            elif staff == 'gk_coach':
                team.upgrade_goalkeeping_coach()
            elif staff == 'def_coach':
                team.upgrade_defending_coach()
            elif staff == 'mid_coach':
                team.upgrade_midfield_coach()
            elif staff == 'att_coach':
                team.upgrade_attacking_coach()
            elif staff == 'set_piece_coach':
                team.upgrade_set_piece_coach()

    return redirect('staff')

def league(request):
    teams = Team.objects.all()

    context = {'teams': teams}

    return render(request, 'management/league.html', context)

@login_required()
def make_offer(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        offer_type = request.POST.get('offer_type')

        player_id = request.POST.get('player_id')
        team_to_name = request.POST.get('team_to')
        player = Player.objects.get(pk=player_id)
        amount = float(request.POST.get('amount'))
        if amount < 0:
            amount = 0
        if offer_type.lower() == 'loan':
            if amount > player.wage:
                amount = player.wage
        team_from = Team.objects.get(owner=request.user)
        team_to = Team.objects.get(name=team_to_name)

        new_offer = offer(team_from=team_from, team_to=team_to, player=player, amount=amount, type=offer_type.capitalize())
        new_offer.save()

    return redirect('league')

@login_required()
def inbox(request):
    team = Team.objects.get(owner=request.user)

    offers_received_query = offer.objects.filter(team_to=team)
    offers_received = []

    for i in offers_received_query:
        offers_received.append(i)

    offers_received = offers_received[::-1]

    context = {'offers_received': offers_received}

    return render(request, 'management/inbox.html', context)

@login_required()
def outbox(request):
    team = Team.objects.get(owner=request.user)

    offers_sent_query = offer.objects.filter(team_from=team)
    offers_sent = []

    for i in offers_sent_query:
        offers_sent.append(i)

    offers_sent = offers_sent[::-1]

    context = {'offers_sent': offers_sent}

    return render(request, 'management/outbox.html', context)

@login_required()
def notifications(request):
    team = Team.objects.get(owner=request.user)

    team.new_message = False
    team.save()

    notifications_received_query = notification.objects.filter(team=team)
    notifications_received = []

    for i in notifications_received_query:
        notifications_received.append(i)

    notifications_received = notifications_received[::-1]

    context = {'notifications_received': notifications_received}

    return render(request, 'management/notifications.html', context)

@login_required()
def reject_offer(request):
    if request.method == 'POST':
        offer_to_reject = offer.objects.get(id=request.POST.get('offer_id'))
        offer_to_reject.reject()

    return redirect('inbox')

@login_required()
def remove_offer(request):
    if request.method == 'POST':
        offer_to_reject = offer.objects.get(id=request.POST.get('offer_id'))
        offer_to_reject.remove()

    return redirect('inbox')

@login_required()
def remove_notification(request):
    if request.method == 'POST':
        notification_to_reject = notification.objects.get(id=request.POST.get('notification_id'))
        notification_to_reject.remove()

    return redirect('notifications')

@login_required()
def accept_offer(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        offer_to_accept = offer.objects.get(id=request.POST.get('offer_id'))
        if offer_to_accept.type == 'Transfer':
            offer_to_accept.accept()
        else:
            offer_to_accept.accept_loan()

    return redirect('inbox')

@login_required()
def offer_contract(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        team = Team.objects.get(owner=request.user)
        wage_budget = team.wage_budget_remaining

        context = {
            'player_id': player.id,
            'player_name': player.name,
            'current_wage': player.wage,
            'current_contract_length': player.contract_length,
            'wage_budget': wage_budget + player.wage,
            'player_loaned': player.loaned,
            'team_offering': team
        }

        return render(request, 'management/offer-contract.html', context)

@login_required()
def offer_contract_outside_team(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        team = Team.objects.get(owner=request.user)
        wage_budget = team.wage_budget_remaining

        context = {
            'player_id': player.id,
            'player_name': player.name,
            'current_wage': player.wage,
            'current_contract_length': player.contract_length,
            'wage_budget': wage_budget,
            'player_loaned': player.loaned,
            'team_offering': team
        }

        return render(request, 'management/offer-contract-outside-team.html', context)

@login_required()
def contract_offer(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = cache.get(f'player_contract_offer_{player_id}')
        minimum_accepted = cache.get(f'minimum_accepted_{player_id}')

        if player is None:
            player = Player.objects.get(pk=player_id)
            offer = int(request.POST.get('offer'))
            length = int(request.POST.get('length'))
            player_wage = player.wage
            team = Team.objects.get(owner=request.user)
            minimum_accepted = 0
            accepted_or_rejected = 'pending'

            more_or_less = random.randint(1,100)

            offers = [0, 10, 15, 20, 25]

            if more_or_less <= 10:
                minimum_accepted = player_wage - round(offers[random.randint(0,2)] * player_wage / 100)
            else:
                minimum_accepted = player_wage - round(offers[random.randint(0, 4)] * player_wage / 100)

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                team.wage_budget_spent -= player.wage
                team.save()
                player.wage = offer
                player.contract_length = length
                player.save()
                team.wage_budget_spent += player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()

            cache.set(f'player_contract_offer_{player_id}', player, timeout=86400)
            cache.set(f'minimum_accepted_{player_id}', minimum_accepted, timeout=86400)
        else:
            offer = int(request.POST.get('offer'))
            length = int(request.POST.get('length'))
            player_wage = player.wage
            team = Team.objects.get(owner=request.user)

            accepted_or_rejected = 'pending'

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                team.wage_budget_spent -= player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()
                player.wage = offer
                player.contract_length = length
                player.save()
                team.wage_budget_spent += player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()

        context = {
            'response' : accepted_or_rejected
        }

        return render(request, 'management/contract-offer-response.html', context)

@login_required()
def contract_offer_outside_team(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        team_offering = request.POST.get('team_offering')
        player = cache.get(f'player_contract_offer_{player_id}_{team_offering}')
        minimum_accepted = cache.get(f'minimum_accepted_{player_id}_{team_offering}')

        if player is None:
            player = Player.objects.get(pk=player_id)
            offer = int(request.POST.get('offer'))
            length = int(request.POST.get('length'))
            player_wage = player.wage
            team = Team.objects.get(owner=request.user)
            minimum_accepted = 0
            accepted_or_rejected = 'pending'

            more_or_less = random.randint(1,100)

            offers = [0, 10, 15, 20, 25]

            if more_or_less <= 10:
                minimum_accepted = player_wage - round(offers[random.randint(0,2)] * player_wage / 100)
            else:
                minimum_accepted = player_wage - round(offers[random.randint(0, 4)] * player_wage / 100)

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                team.wage_budget_spent -= player.wage
                team.save()
                player.wage = offer
                player.contract_length = length
                player.team = team
                player.free_agent = False
                player.save()
                team.wage_budget_spent += player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()

            cache.set(f'player_contract_offer_{player_id}', player, timeout=86400)
            cache.set(f'minimum_accepted_{player_id}', minimum_accepted, timeout=86400)
        else:
            offer = int(request.POST.get('offer'))
            length = int(request.POST.get('length'))
            player_wage = player.wage
            team = Team.objects.get(owner=request.user)

            accepted_or_rejected = 'pending'

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                team.wage_budget_spent -= player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()
                player.wage = offer
                player.contract_length = length
                player.team = team
                player.free_agent = False
                player.save()
                team.wage_budget_spent += player.wage
                team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
                team.save()

        context = {
            'response' : accepted_or_rejected
        }

        return render(request, 'management/contract-offer-response.html', context)


@login_required()
def negotiate_signing(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Scouted_Player.objects.get(pk=player_id)
        team = Team.objects.get(owner=request.user)
        transfer = team.transfer_budget

        context = {
            'player_id': player.id,
            'player_name': player.name,
            'player_value': player.value,
            'transfer_budget': transfer
        }

        return render(request, 'management/player-negotiate-buy.html', context)

@login_required()
def signing_negotiation(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = cache.get(f'player_negotiation_{player_id}')
        minimum_accepted = cache.get(f'minimum_transfer_accepted_{player_id}')

        if player is None:
            player = Scouted_Player.objects.get(pk=player_id)
            offer = float(request.POST.get('offer'))
            player_value = player.value
            team = Team.objects.get(owner=request.user)
            minimum_accepted = 0
            accepted_or_rejected = 'pending'

            more_or_less = random.randint(1,100)

            offers = [0, 10, 15, 20, 25]

            if more_or_less <= 10:
                minimum_accepted = player_value - round(offers[random.randint(2,4)] * player_value / 100)
            else:
                minimum_accepted = player_value - round(offers[random.randint(0, 1)] * player_value / 100)

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                player.value = float(offer)
                player.save()
                player.sign()

            cache.set(f'player_negotiation_{player_id}', player, timeout=86400)
            cache.set(f'minimum_transfer_accepted_{player_id}', minimum_accepted, timeout=86400)
        else:
            offer = int(request.POST.get('offer'))
            player_value = player.value
            team = Team.objects.get(owner=request.user)

            accepted_or_rejected = 'pending'

            if offer < minimum_accepted:
                accepted_or_rejected = 'rejected'
            else:
                accepted_or_rejected = 'accepted'
                player.value = float(offer)
                player.save()
                player.sign()

        context = {
            'response' : accepted_or_rejected
        }

        return render(request, 'management/player-negotiation-response.html', context)

def open_transfer_window(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    teams = Team.objects.all()

    for team in teams:
        team.can_transfer = True
        team.save()

    return redirect('admin-panel')

def close_transfer_window(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    teams = Team.objects.all()

    for team in teams:
        team.can_transfer = False
        team.save()

    return redirect('admin-panel')

def return_loans(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    players = Player.objects.filter(loaned='out')

    for player in players:
        player.return_loan()

    out_of_league_loans = Player.objects.filter(out_of_league_loan=True)

    for player in out_of_league_loans:
        team = player.team
        scouted_player = Scouted_Player.objects.get(team=player.team, position=player.position, name=player.name, age=player.age, overall=player.overall, potential=player.potential,
                                                    tactic=player.tactic, loaned=player.out_of_league_loan)
        scouted_player.loaned = False
        scouted_player.save()
        player.delete()
        fix_wages(team)

    return redirect('admin-panel')

def return_loans_offseason():
    players = Player.objects.filter(loaned='out')

    for player in players:
        player.return_loan()

    out_of_league_loans = Player.objects.filter(out_of_league_loan=True)

    for player in out_of_league_loans:
        team = player.team
        scouted_player = Scouted_Player.objects.get(id=player.id)
        scouted_player.loaned = False
        scouted_player.save()
        player.delete()
        fix_wages(team)

    return redirect('admin-panel')

def admin_panel(request):
    user = request.user
    if user.is_superuser:
        return render(request, 'management/admin-panel.html')
    else:
        return redirect('site-home')

def transfer_window_closed(request):
    return render(request, 'management/transfer-window-closed.html')

def add_trait(request):
    response = ''

    if request.method == 'POST':
        trait = request.POST.get('trait')
        cost = int(request.POST.get('cost'))
        player_id = request.POST.get('player_id')
        player = Player.objects.get(id=player_id)
        if player.loaned != 'out':
            player_traits_string = player.traits
            player_traits = player_traits_string.split(',')
            skill_points = player.skill_points

            requirements = {
                'Deus' : ['Medietas'],
                'Medietas' : [],
                'Vindicta': ['Guardian'],
                'Auxilior': ['Maestro'],
                'Impetus': ['Gunslinger'],
                'Guardian' : ['2-Way'],
                '2-Way': ['King', 'Keeper'],
                'King': ['Wall'],
                'Wall': ['Underdog'],
                'Underdog': ['Jester'],
                'Keeper': ['Engine'],
                'Engine': ['Ironclad'],
                'Ironclad': ['Fresh'],
                'Maestro': ['Visionary'],
                '2-Way': ['Swinger', 'Sleeper'],
                'Swinger': ['Leader'],
                'Leader': ['Artist'],
                'Artist': ['Receba'],
                'Sleeper': ['Late Bloomer'],
                'Late Bloomer': ['Einstein'],
                'Einstein': ['Gift-Giver'],
                'Gunslinger': ['Silencer'],
                'Silencer': ['Big Game Player', 'Super Sub'],
                'Big Game Player': ['Headliner'],
                'Headliner': ['Merchant'],
                'Merchant': ['Statpadder'],
                'Super Sub': ['Clutch Pro'],
                'Clutch Pro': ['Seller'],
                'Seller': ['Speed Demon'],
            }

            defensive_positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB', 'CDM']
            midfield_positons = ['LM', 'CM', 'CAM', 'RM']
            attacking_postions = ['LW', 'CF', 'ST', 'RW']

            if player.position in defensive_positions:
                requirements['Medietas'] = ['Vindicta']
            elif player.position in midfield_positons:
                requirements['Medietas'] = ['Auxilior']
            elif player.position in attacking_postions:
                requirements['Medietas'] = ['Impetus']

            starter_traits = ['Jester', 'Fresh', 'Receba', 'Gift-Giver', 'Statpadder', 'Speed Demon']

            if trait not in player_traits and skill_points >= cost:
                if trait not in starter_traits:
                    for i in requirements[trait]:
                        if i not in player_traits:
                            response = 'This player does not have the required traits to obtain this trait.'
                            context = {
                                'response': response
                            }
                            return render(request, 'management/add-trait.html', context)
                if player_traits_string != '':
                    player_traits_string += ',' + trait
                else:
                    player_traits_string += trait
                player.skill_points -= cost
                player.traits = player_traits_string
                player.save()
                response = f'This player now has the {trait} trait.'
                context = {
                    'response': response
                }
            if trait in player_traits:
                response = 'This player already has this trait.'
                context = {
                    'response': response
                }
            if trait not in player_traits and skill_points < cost:
                response = 'This player does not have sufficient skill points to purchase this trait.'
                context = {
                    'response': response
                }
        else:
            return redirect('manage-team')

        return render(request, 'management/add-trait.html', context)

@login_required()
def train_position(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        training_position = request.POST.get('training_position')

        if training_position not in player.position.split('/') and player.loaned != 'out' and len(player.position.split('/')) < 4:
            training_values = get_position_training_values(player.position, training_position)

            player.training = True
            player.training_position = training_position
            player.training_position_time = training_values[0]
            player.training_position_chance = training_values[1]
            player.save()

            team = Team.objects.get(owner=request.user)

            new_notification = notification(team=team, message=f'{player.name} has begun position training for {training_position}. Duration: {player.training_position_time} weeks.')
            new_notification.save()

            team.new_message = True
            team.save()
        else:
            return redirect('manage-team')

        return redirect('notifications')
@login_required()
def train_tactic(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        training_tactic = request.POST.get('training_tactic')

        if player.tactic != training_tactic and player.loaned != 'out':
            training_values = get_tactic_training_values(player.tactic, training_tactic)

            player.training = True
            player.training_tactic = training_tactic
            player.training_tactic_time = training_values[0]
            player.training_tactic_chance = training_values[1]
            player.save()

            team = Team.objects.get(owner=request.user)

            new_notification = notification(team=team, message=f'{player.name} has begun tactic training for {training_tactic}. Duration: {player.training_tactic_time} weeks.')
            new_notification.save()
            team.new_message = True
            team.save()
        else:
            return redirect('manage-team')

        return redirect('notifications')

@login_required
def manage_feeder_team(request):
    team_name = request.POST.get('team_name')
    team_type = request.POST.get('team_type')
    team_level = request.POST.get('team_level')
    team = Feeder_Team.objects.get(name=team_name)
    players = Player.objects.filter(feeder_team=team)

    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    sorted_players = []

    for i in positions:
        for x in players:
            position = x.position.split('/')[0]
            if position == i:
                sorted_players.append(x)

    context =  {
        'team_name': team.name,
        'team_type': team_type,
        'team_level': team_level,
        'players': sorted_players,
        'level': team.level
    }

    return render(request, 'management/manage_feeder_team.html', context)

def send_to_feeder(request):
    team_name = request.POST.get('team_name')
    player_id = request.POST.get('player_id')
    team = Feeder_Team.objects.get(name=team_name)
    player = Player.objects.get(id=player_id)

    parent_team = team.parent_club

    if player.sex == 'Male':
        if team.team_type != "women":
            player.send_to_feeder_team(team)

            new_notification = notification(team=player.team,
                                            message=f'{player.name} has been sent to {team.name}.')
            new_notification.save()
    else:
        player.send_to_feeder_team(team)

        new_notification = notification(team=player.team,
                                        message=f'{player.name} has been sent to {team.name}.')
        new_notification.save()

    parent_team.new_message = True
    parent_team.save()

    return redirect('notifications')

def promote_to_senior_team(request):
    player_id = request.POST.get('player_id')
    player = Player.objects.get(id=player_id)
    player.promote_to_senior_team()

    new_notification = notification(team=player.team,
                                    message=f'{player.name} has been promoted to the senior team.')
    new_notification.save()
    team = player.team
    team.new_message = True
    team.save()

    return redirect('notifications')

def create_player_form(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    countries = [
        "Afghanistan", "Aland", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
        "Antarctica", "Antigua & Barbuda", "Argentina",
        "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
        "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire", "Bosnia & Herzegovina",
        "Botswana", "Bouvet Island", "Brazil", "British Virgin Islands", "Brunei",
        "Bulgaria", "Burkina Faso", "Burundi",
        "Cambodia", "Cameroon", "Canada", "Cape Verde", "Catalonia", "Cayman Islands", "Central African Republic",
        "Chad",
        "Chile", "China", "Christmas Island", "Cocos Islands", "Colombia", "Comoros", "Congo", "Cook Islands",
        "Costa Rica",
        "Croatia", "Cuba", "Curacao", "Cyprus",
        "Czech Republic", "Denmark", "Djibouti", "Dominican Republic", "Dominica", "DR Congo",
        "Ecuador", "Egypt", "El Salvador", "England", "Equatorial Guinea", "Eritrea", "Estonia",
        "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana",
        "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guadeloupe", "Guatemala",
        "Guernsey", "Guinea",
        "Guinea-Bissau", "Guyana", "Haiti", "Heard Island", "Holy See", "Honduras", "Hong Kong", "Hungary", "Iceland",
        "Isle of Man", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
        "Jersey",
        "Kazakhstan", "Kenya", "Kirain", "Kiribati", "Kosovo", "Kurdistan", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
        "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mapuche", "Martinique", "Mauritania",
        "Mauritius", "Manchuoko", "Marshall Islands", "Mayotte", "Mcdonald Islands", "Mexico", "Micronesia", "Moldova",
        "Monaco", "Mongolia", "Montenegro", "Montserrat",
        "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia",
        "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Korea", "North Macedonia",
        "Northern Ireland", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palestine", "Palau", "Panama",
        "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
        "Republic of Samoa", "Romania", "Russia", "Reunion", "Rwanda", "Saint Helena", "Saint Kitts & Nevis",
        "Saint Lucia",
        "Saint Pierre & Miquelon",
        "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia",
        "Scotland", "Sealand", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Sint Maarten",
        "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sandwich Islands", "South Sudan", "Spain",
        "Sri Lanka", "Sudan",
        "Suriname", "Svalbard", "Sweden", "Switzerland", "Syria", "Tahiti", "Taiwan", "Tajikistan", "Tanzania",
        "Thailand", "Timor Leste", "Togo", "Tokelau", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
        "Turkmenistan", "Turks & Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "Uruguay", "US Virgin Islands", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wales",
        "Wallis & Futuna", "Western Sahara", "Yemen",
        "Zambia", "Zimbabwe"
    ]

    countries_dict = {
        "Afghanistan": "pas",
        "Albania": "alb",
        "Algeria": "afr",
        "American Samoa": "smn",
        "Andorra": "cat",
        "Anguilla": "nrm",
        "Antigua & Barbuda": "nrm",
        "Argentina": "spa",
        "Armenia": "arm",
        "Aruba": "cha",
        "Austria": "ger",
        "Azerbaijan": "aze",
        "Bahamas": "cha",
        "Bahrain": "ara",
        "Bangladesh": "ben",
        "Barbados": "nrm",
        "Belarus": "bel",
        "Belgium": "dut",
        "Belize": "cha",
        "Benin": "afr",
        "Bermuda": "nrm",
        "Bhutan": "bhu",
        "Bolivia": "aym",
        "Bonaire": "dut",
        "Bosnia & Herzegovina": "bos",
        "Botswana": "tsw",
        "Brazil": "por",
        "British Virgin Islands": "nrm",
        "Brunei": "mly",
        "Bulgaria": "bul",
        "Burkina Faso": "afr",
        "Burundi": "afr",
        "Cambodia": "khm",
        "Canada": "sio",
        "Cape Verde": "por",
        "Catalonia": "cat",
        "Cayman Islands": "nrm",
        "Central African Republic": "afr",
        "Chad": "afr",
        "Chile": "spa",
        "Colombia": "spa",
        "Comoros": "cmr",
        "Congo": "kon",
        "Cook Islands": "cha",
        "Costa Rica": "spa",
        "Croatia": "cro",
        "Cuba": "spa",
        "Curacao": "fle",
        "Cyprus": "gre",
        "Czech Republic": "cze",
        "Denmark": "dan",
        "Djibouti": "afr",
        "Dominican Republic": "spa",
        "Dominica": "pcd",
        "DR Congo": "kon",
        "Ecuador": "map",
        "Egypt": "cop",
        "El Salvador": "spa",
        "England": "eng",
        "Equatorial Guinea": "afr",
        "Eritrea": "tig",
        "Estonia": "est",
        "Eswatini": "swz",
        "Ethiopia": "tig",
        "Faroe Islands": "fae",
        "Fiji": "fij",
        "Finland": "fin",
        "France": "fre",
        "Gabon": "fre",
        "Georgia": "geo",
        "Germany": "ger",
        "Ghana": "aka",
        "Gibraltar": "geo",
        "Greece": "gre",
        "Greenland": "grn",
        "Grenada": "nrm",
        "Guam": "cha",
        "Guadeloupe": "fre",
        "Guatemala": "spa",
        "Guinea": "afr",
        "Guinea-Bissau": "afr",
        "Guyana": "nrm",
        "Haiti": "fre",
        "Honduras": "spa",
        "Hong Kong": "chi",
        "Hungary": "hun",
        "Iceland": "ice",
        "India": "ind",
        "Indonesia": "ins",
        "Iran": "per",
        "Iraq": "per",
        "Ireland": "iri",
        "Israel": "heb",
        "Italy": "ita",
        "Ivory Coast": "aka",
        "Jamaica": "afr",
        "Jordan": "afr",
        "Kazakhstan": "kaz",
        "Kenya": "luh",
        "Kirain": "ame",
        "Kiribati": "fij",
        "Kosovo": "alb",
        "Kurdistan": "kur",
        "Kuwait": "ara",
        "Kyrgyzstan": "kyr",
        "Laos": "lao",
        "Latvia": "lat",
        "Lebanon": "arm",
        "Lesotho": "sot",
        "Liberia": "afr",
        "Libya": "ara",
        "Liechtenstein": "ger",
        "Lithuania": "lth",
        "Luxembourg": "lim",
        "Macau": "chi",
        "Madagascar": "afr",
        "Malawi": "cew",
        "Malaysia": "mly",
        "Maldives": "dhi",
        "Mali": "som",
        "Malta": "mal",
        "Mapuche": "map",
        "Martinique": "fre",
        "Mauritania": "afr",
        "Mauritius": "afr",
        "Manchuoko": "jap",
        "Marshall Islands": "cha",
        "Mexico": "spa",
        "Micronesia": "fij",
        "Moldova": "mol",
        "Mongolia": "mon",
        "Montenegro": "alb",
        "Montserrat": "nrm",
        "Morocco": "ara",
        "Mozambique": "yao",
        "Myanmar": "bur",
        "Namibia": "afk",
        "Nauru": "cha",
        "Nepal": "nep",
        "Netherlands": "dut",
        "New Caledonia": "fre",
        "New Zealand": "eng",
        "Nicaragua": "spa",
        "Niger": "afr",
        "Nigeria": "afr",
        "Niue": "ton",
        "North Korea": "kor",
        "North Macedonia": "mac",
        "Northern Ireland": "iri",
        "Norway": "nor",
        "Oman": "ara",
        "Pakistan": "pas",
        "Palestine": "ara",
        "Palau": "ton",
        "Panama": "spa",
        "Papua New Guinea": "eng",
        "Paraguay": "spa",
        "Peru": "spa",
        "Philippines": "tag",
        "Poland": "pol",
        "Portugal": "por",
        "Puerto Rico": "spa",
        "Qatar": "ara",
        "Republic of Samoa": "sam",
        "Romania": "rmn",
        "Russia": "rus",
        "Rwanda": "kig",
        "Saint Kitts & Nevis": "eng",
        "Saint Lucia": "eng",
        "Saint Vincent & the Grenadines": "eng",
        "Samoa": "sam",
        "San Marino": "ita",
        "Sao Tome & Principe": "afr",
        "Saudi Arabia": "ara",
        "Scotland": "sco",
        "Sealand": "eng",
        "Serbia": "ser",
        "Seychelles": "afr",
        "Sierra Leone": "afr",
        "Singapore": "mly",
        "Slovakia": "slk",
        "Slovenia": "sln",
        "Solomon Islands": "eng",
        "Somalia": "som",
        "South Africa": "afr",
        "South Sudan": "afr",
        "Spain": "spa",
        "Sri Lanka": "tam",
        "Sudan": "afr",
        "Suriname": "dut",
        "Sweden": "swe",
        "Switzerland": "ger",
        "Syria": "ara",
        "Tahiti": "tah",
        "Taiwan": "chi",
        "Tajikistan": "taj",
        "Tanzania": "tum",
        "Thailand": "tha",
        "Timor Leste": "por",
        "Togo": "afr",
        "Tokelau": "fij",
        "Tonga": "ton",
        "Trinidad & Tobago": "eng",
        "Tunisia": "afr",
        "Turkey": "tur",
        "Turkmenistan": "tkm",
        "Turks & Caicos Islands": "eng",
        "Tuvalu": "fij",
        "Uganda": "afr",
        "Ukraine": "ukr",
        "United Arab Emirates": "ara",
        "Uruguay": "spa",
        "US Virgin Islands": "eng",
        "USA": "eng",
        "Uzbekistan": "uzb",
        "Vanuatu": "tah",
        "Venezuela": "spa",
        "Vietnam": "vie",
        "Wales": "wel",
        "Wallis & Futuna": "fre",
        "Zambia": "tum",
        "Zimbabwe": "sho",
        "Aland": "dan",
        "Angola": "afr",
        "Antarctica": "eng",
        "Australia": "eng",
        "Bouvet Island": "fre",
        "Cameroon": "afr",
        "China": "chi",
        "Christmas Island": "eng",
        "Cocos Islands": "eng",
        "Falkland Islands": "ger",
        "French Guiana": "fre",
        "Gambia": "afr",
        "Guernsey": "eng",
        "Heard Island": "eng",
        "Holy See": "eng",
        "Isle of Man": "eng",
        "Japan": "jap",
        "Jersey": "eng",
        "South Korea": "kor",
        "Mayotte": "fre",
        "Mcdonald Islands": "eng",
        "Monaco": "fre",
        "Norfolk Island": "ger",
        "Northern Mariana Islands": "eng",
        "Pitcairn": "eng",
        "Reunion": "fre",
        "Saint Helena": "eng",
        "Saint Pierre & Miquelon": "fre",
        "Senegal": "afr",
        "Sint Maarten": "dut",
        "South Sandwich Islands": "eng",
        "Svalbard": "swe",
        "Western Sahara": "afr",
        "Yemen": "ara"
    }

    tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
               'Tiki-Taka', 'Gegenpress', 'Wing Play']

    teams = Team.objects.all()

    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    context = {
        'countries' : countries,
        'tactics' : tactics,
        'teams' : teams,
        'positions' : positions
    }

    return render(request, 'management/create-player.html', context)

def create_youth_player_form(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    countries = [
        "Afghanistan", "Aland", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla",
        "Antarctica", "Antigua & Barbuda", "Argentina",
        "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
        "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan", "Bolivia", "Bonaire", "Bosnia & Herzegovina",
        "Botswana", "Bouvet Island", "Brazil", "British Virgin Islands", "Brunei",
        "Bulgaria", "Burkina Faso", "Burundi",
        "Cambodia", "Cameroon", "Canada", "Cape Verde", "Catalonia", "Cayman Islands", "Central African Republic",
        "Chad",
        "Chile", "China", "Christmas Island", "Cocos Islands", "Colombia", "Comoros", "Congo", "Cook Islands",
        "Costa Rica",
        "Croatia", "Cuba", "Curacao", "Cyprus",
        "Czech Republic", "Denmark", "Djibouti", "Dominican Republic", "Dominica", "DR Congo",
        "Ecuador", "Egypt", "El Salvador", "England", "Equatorial Guinea", "Eritrea", "Estonia",
        "Eswatini", "Ethiopia", "Falkland Islands", "Faroe Islands", "Fiji", "Finland", "France", "French Guiana",
        "Gabon", "Gambia", "Georgia",
        "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guam", "Guadeloupe", "Guatemala",
        "Guernsey", "Guinea",
        "Guinea-Bissau", "Guyana", "Haiti", "Heard Island", "Holy See", "Honduras", "Hong Kong", "Hungary", "Iceland",
        "Isle of Man", "India",
        "Indonesia", "Iran", "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica", "Japan", "Jordan",
        "Jersey",
        "Kazakhstan", "Kenya", "Kirain", "Kiribati", "Kosovo", "Kurdistan", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
        "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
        "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta", "Mapuche", "Martinique", "Mauritania",
        "Mauritius", "Manchuoko", "Marshall Islands", "Mayotte", "Mcdonald Islands", "Mexico", "Micronesia", "Moldova",
        "Monaco", "Mongolia", "Montenegro", "Montserrat",
        "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "New Caledonia",
        "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island", "North Korea", "North Macedonia",
        "Northern Ireland", "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palestine", "Palau", "Panama",
        "Papua New Guinea",
        "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar",
        "Republic of Samoa", "Romania", "Russia", "Reunion", "Rwanda", "Saint Helena", "Saint Kitts & Nevis",
        "Saint Lucia",
        "Saint Pierre & Miquelon",
        "Saint Vincent & the Grenadines", "Samoa", "San Marino", "Sao Tome & Principe", "Saudi Arabia",
        "Scotland", "Sealand", "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Sint Maarten",
        "Slovakia", "Slovenia",
        "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sandwich Islands", "South Sudan", "Spain",
        "Sri Lanka", "Sudan",
        "Suriname", "Svalbard", "Sweden", "Switzerland", "Syria", "Tahiti", "Taiwan", "Tajikistan", "Tanzania",
        "Thailand", "Timor Leste", "Togo", "Tokelau", "Tonga", "Trinidad & Tobago", "Tunisia", "Turkey",
        "Turkmenistan", "Turks & Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates",
        "Uruguay", "US Virgin Islands", "USA", "Uzbekistan", "Vanuatu", "Venezuela", "Vietnam", "Wales",
        "Wallis & Futuna", "Western Sahara", "Yemen",
        "Zambia", "Zimbabwe"
    ]

    tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
               'Tiki-Taka', 'Gegenpress', 'Wing Play']

    teams = Team.objects.all()
    feeder_teams = Feeder_Team.objects.all()

    positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                 'CDM', 'LM', 'CM', 'RM', 'CAM',
                 'LW', 'CF', 'ST', 'RW']

    context = {
        'countries' : countries,
        'tactics' : tactics,
        'teams' : teams,
        'feeder_teams' : feeder_teams,
        'positions' : positions
    }

    return render(request, 'management/create-youth-player.html', context)

def fix_wages(team):
    players = Player.objects.filter(team=team)
    total_wages = 0
    for i in players:
        if not i.free_agent:
            print(i.name, i.wage)
            total_wages += i.wage
    team.wage_budget_spent = total_wages
    team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
    team.save()

def fix_wages_all():
    teams = Team.objects.all()

    for team in teams:
        players = Player.objects.filter(team=team)
        total_wages = 0
        for player in players:
            if not player.free_agent:
                total_wages += player.wage
        team.wage_budget_spent = total_wages
        team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
        team.save()

def create_player(request):
    team_id = request.POST.get('team')
    team = Team.objects.get(id=team_id)
    name = request.POST.get('name')
    position = request.POST.get('position')
    age = int(request.POST.get('age'))
    overall = int(request.POST.get('overall'))
    potential = int(request.POST.get('potential'))
    nationality = request.POST.get('nationality')
    tactic = request.POST.get('tactic')
    wage = int(request.POST.get('wage'))
    contract_length = int(request.POST.get('contract_length'))
    sex = request.POST.get('sex')

    new_player = Player(team=team, position=position, name=name, sex=sex, age=age, overall=overall, potential=potential, nationality=nationality, tactic=tactic, wage=wage,
                        contract_length=contract_length, skill_points=0, goals=0, assists=0, motm=0)
    new_player.save()

    fix_wages(team)

    new_notification = notification(team=new_player.team,
                                    message=f'{new_player.name} has been added to {team.name}.')
    new_notification.save()
    team.new_message = True
    team.save()

    return redirect('admin-panel')

def create_youth_player(request):
    team_id = request.POST.get('team')
    team = Feeder_Team.objects.get(name=team_id)
    name = request.POST.get('name')
    position = request.POST.get('position')
    age = int(request.POST.get('age'))
    overall = int(request.POST.get('overall'))
    potential = int(request.POST.get('potential'))
    nationality = request.POST.get('nationality')
    tactic = request.POST.get('tactic')
    wage = int(request.POST.get('wage'))
    contract_length = int(request.POST.get('contract_length'))
    sex = request.POST.get('sex')

    new_player = Player(team=team.parent_club, feeder_team=team, position=position, name=name, sex=sex, age=age, overall=overall, potential=potential, nationality=nationality, tactic=tactic, wage=wage,
                        contract_length=contract_length, skill_points=0, goals=0, assists=0, motm=0)
    new_player.save()

    fix_wages(team.parent_club)

    new_notification = notification(team=new_player.team,
                                    message=f'{new_player.name} has been added to {team.name}.')
    new_notification.save()

    parent_team = team.parent_club
    parent_team.new_message = True
    parent_team.save()

    return redirect('admin-panel')

def select_team_transfer_budget(request):
    teams = Team.objects.all()

    context = {
        'teams' : teams
    }

    return render(request, 'management/change-transfer-budget-form.html', context)

def change_transfer_budget(request):
    team_id = request.POST.get('team')
    team = Team.objects.get(id=team_id)
    amount = float(request.POST.get('amount'))

    team.transfer_budget += amount
    team.save()

    if amount > 0:
        new_notification = notification(team=team,
                                        message=f'{amount}M has been added to your transfer budget.')
    else:
        new_notification = notification(team=team,
                                        message=f'{-amount}M has been removed from your transfer budget.')

    new_notification.save()
    team.new_message = True
    team.save()

    return redirect('admin-panel')

def select_team_facilities_budget(request):
    teams = Team.objects.all()

    context = {
        'teams' : teams
    }

    return render(request, 'management/change-facilities-budget-form.html', context)

def change_facilities_budget(request):
    team_id = request.POST.get('team')
    team = Team.objects.get(id=team_id)
    amount = float(request.POST.get('amount'))

    team.facilities_budget += amount
    team.save()

    if amount > 0:
        new_notification = notification(team=team,
                                        message=f'{amount}M has been added to your facilities budget.')
    else:
        new_notification = notification(team=team,
                                        message=f'{-amount}M has been removed from your facilities budget.')

    new_notification.save()
    team.new_message = True
    team.save()

    return redirect('admin-panel')

def select_team_wage_budget(request):
    teams = Team.objects.all()

    context = {
        'teams' : teams
    }

    return render(request, 'management/change-wage-budget-form.html', context)

def change_wage_budget(request):
    team_id = request.POST.get('team')
    team = Team.objects.get(id=team_id)
    amount = float(request.POST.get('amount'))

    team.wage_budget_total += amount
    team.save()
    fix_wages(team)

    if amount > 0:
        new_notification = notification(team=team,
                                        message=f'{amount} has been added to your wage budget.')
    else:
        new_notification = notification(team=team,
                                        message=f'{-amount} has been removed from your wage budget.')

    new_notification.save()
    team.new_message = True
    team.save()

    return redirect('admin-panel')

def select_team_faciltiies(request):
    teams = Team.objects.all()

    facilities = ['Stadium', 'Training Facilities', 'Youth Academy', 'Merchandise']

    context = {
        'teams' : teams,
        'facilities' : facilities
    }

    return render(request, 'management/update-facilities-form.html', context)

def update_facilities(request):
    team_id = request.POST.get('team')
    team = Team.objects.get(id=team_id)
    action = request.POST.get('action')
    facility = request.POST.get('facility').lower()

    if action == 'upgrade':
        if facility == 'stadium':
            if team.stadium < 120000:
                team.stadium += 1000
        elif facility == 'training':
            if team.training_facilties < 5:
                team.training_facilties += 1
        elif facility == 'youth academy':
            if team.youth_academy < 5:
                team.youth_academy += 1
        else:
            if team.merchandise < 5:
                team.merchandise += 1
        new_notification = notification(team=team, message=f'{facility.title()} has been upgraded.')
    else:
        if facility == 'stadium':
            if team.stadium > 1000:
                team.stadium -= 1000
        elif facility == 'training':
            if team.training_facilties > 1:
                team.training_facilties -= 1
        elif facility == 'youth academy':
            if team.youth_academy > 1:
                team.youth_academy -= 1
        else:
            if team.merchandise > 1:
                team.merchandise -= 1
        new_notification = notification(team=team, message=f'{facility.title()} has been downgraded.')

    new_notification.save()

    team.new_message = True
    team.save()

    return redirect('admin-panel')

@login_required
def loan_out_of_league_player(request):
    if request.method == 'POST':
        team_logged_in = Team.objects.get(owner=request.user)
        if not team_logged_in.can_transfer:
            return redirect('transfer-window-closed')

        player_id = request.POST.get('player_id')
        scouted_player = Scouted_Player.objects.get(pk=player_id)

        scouted_player.loan()

        new_notification = notification(team=team_logged_in, message=f'{scouted_player.name} has been loaned.')
        new_notification.save()

        team_logged_in.new_message = True
        team_logged_in.save()

    return redirect('manage-team')

def update_scouted_players(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    scouted_players = Scouted_Player.objects.all()

    for player in scouted_players:
        player.age += 1

        if player.age >= 36:
            player.delete()
        else:
            if player.age < 26 and player.potential <= 85:
                upgrade_potential_chance = random.randint(1, 100)
                if upgrade_potential_chance <= 25:
                    player.potential += random.randint(0,3)

            if player.overall < player.potential and player.overall <= 85:
                upgrade_overall_chance = random.randint(1, 100)
                if upgrade_overall_chance <= 25:
                    player.overall += random.randint(0,3)
                    if player.overall > player.potential:
                        player.overall = player.potential

            player.wage = calculate_wage(player.overall)

            player.value = calculate_value(player.position, player.age, player.overall, player.potential)

            if player.can_be_loaned:
                loaned_wage = 0
                loaned_wage_chance = random.randint(1, 100)
                if loaned_wage_chance <= 100:
                    loaned_wage = 50
                if loaned_wage_chance <= 50:
                    loaned_wage = 0
                if loaned_wage_chance <= 20:
                    loaned_wage = 25
                if loaned_wage_chance <= 5:
                    loaned_wage = 75

                loaned_wage = player.wage - round((loaned_wage * player.wage) / 100)

                player.loaned_wage = loaned_wage

            player.save()

    for team in Team.objects.all():
        new_notification = notification(team=team, message=f'Scouted players have been updated.')
        new_notification.save()

        team.new_message = True
        team.save()

    return redirect('admin-panel')

def update_scouted_players_offseason():
    scouted_players = Scouted_Player.objects.all()

    for player in scouted_players:
        player.age += 1

        if player.age >= 36:
            player.delete()
        else:
            if player.age < 26 and player.potential <= 85:
                upgrade_potential_chance = random.randint(1, 100)
                if upgrade_potential_chance <= 25:
                    player.potential += random.randint(0,3)

            if player.overall < player.potential and player.overall <= 85:
                upgrade_overall_chance = random.randint(1, 100)
                if upgrade_overall_chance <= 25:
                    player.overall += random.randint(0,3)
                    if player.overall > player.potential:
                        player.overall = player.potential

            player.wage = calculate_wage(player.overall)

            player.value = calculate_value(player.position, player.age, player.overall, player.potential)

            if player.can_be_loaned:
                loaned_wage = 0
                loaned_wage_chance = random.randint(1, 100)
                if loaned_wage_chance <= 100:
                    loaned_wage = 50
                if loaned_wage_chance <= 50:
                    loaned_wage = 0
                if loaned_wage_chance <= 20:
                    loaned_wage = 25
                if loaned_wage_chance <= 5:
                    loaned_wage = 75

                loaned_wage = player.wage - round((loaned_wage * player.wage) / 100)

                player.loaned_wage = loaned_wage

            player.save()

    for team in Team.objects.all():
        new_notification = notification(team=team, message=f'Scouted players have been updated.')
        new_notification.save()

        team.new_message = True
        team.save()

    return redirect('admin-panel')


@login_required
def invest_in_womens_team(request):
    if request.method == 'POST':
        team_name = request.POST.get('team_name')
        amount = request.POST.get('amount')
        team = Feeder_Team.objects.get(name=team_name)

        if team.parent_club.facilities_budget >= int(amount):
            level_increase = random.randint(0, int(amount))
            team.level += level_increase
            team.save()

            team.parent_club.facilities_budget -= int(amount)

            new_notification = notification(team=team.parent_club, message=f'{amount}M has been invested into {team_name} and resulted in a level increase of {level_increase}.')
            new_notification.save()

            team.parent_club.new_message = True
            team.parent_club.save()

    return redirect('manage-team')

@login_required
def update_womens_teams(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    womens_teams = Feeder_Team.objects.filter(team_type="women")

    for team in womens_teams:
        level_decrease = random.randint(0, 5)
        team.level -= level_decrease
        team.save()

        positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                     'CDM', 'LM', 'CM', 'RM', 'CAM',
                     'LW', 'CF', 'ST', 'RW']

        tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
                   'Tiki-Taka', 'Gegenpress', 'Wing Play']

        nationality = team.nation

        tactic = tactics[random.randint(0, len(tactics) - 1)]

        age = random.randint(13, 19)

        overall = random.randint(team.level-5, team.level+5)

        potential = random.randint(overall, overall+10)

        if potential > 99:
            potential = 99

        new_player = Player(team=team.parent_club, feeder_team=team, position=positions[random.randint(0, len(positions) - 1)],
                            name='Youth Player', age=age, sex='Female',
                            overall=overall, potential=potential, nationality=nationality, tactic=tactic,
                            wage=50, contract_length=2)

        new_player.save()

        new_notification = notification(team=team.parent_club,
                                        message=f"{team.name}'s level has decreased by {level_decrease}.")
        new_notification.save()

        team.parent_club.new_message = True
        team.parent_club.save()

    return redirect('admin-panel')

def update_womens_teams_offseason():
    womens_teams = Feeder_Team.objects.filter(team_type="women")

    for team in womens_teams:
        level_decrease = random.randint(0, 5)
        team.level -= level_decrease
        team.save()

        positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                     'CDM', 'LM', 'CM', 'RM', 'CAM',
                     'LW', 'CF', 'ST', 'RW']

        tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
                   'Tiki-Taka', 'Gegenpress', 'Wing Play']

        nationality = team.nation

        tactic = tactics[random.randint(0, len(tactics) - 1)]

        age = random.randint(13, 19)

        overall = random.randint(team.level-5, team.level+5)

        potential = random.randint(overall, overall+10)

        if potential > 99:
            potential = 99

        countries_dict = {
            "Afghanistan": "pas",
            "Albania": "alb",
            "Algeria": "afr",
            "American Samoa": "smn",
            "Andorra": "cat",
            "Anguilla": "nrm",
            "Antigua & Barbuda": "nrm",
            "Argentina": "spa",
            "Armenia": "arm",
            "Aruba": "cha",
            "Austria": "ger",
            "Azerbaijan": "aze",
            "Bahamas": "cha",
            "Bahrain": "ara",
            "Bangladesh": "ben",
            "Barbados": "nrm",
            "Belarus": "bel",
            "Belgium": "dut",
            "Belize": "cha",
            "Benin": "afr",
            "Bermuda": "nrm",
            "Bhutan": "bhu",
            "Bolivia": "aym",
            "Bonaire": "dut",
            "Bosnia & Herzegovina": "bos",
            "Botswana": "tsw",
            "Brazil": "por",
            "British Virgin Islands": "nrm",
            "Brunei": "mly",
            "Bulgaria": "bul",
            "Burkina Faso": "afr",
            "Burundi": "afr",
            "Cambodia": "khm",
            "Canada": "sio",
            "Cape Verde": "por",
            "Catalonia": "cat",
            "Cayman Islands": "nrm",
            "Central African Republic": "afr",
            "Chad": "afr",
            "Chile": "spa",
            "Colombia": "spa",
            "Comoros": "cmr",
            "Congo": "kon",
            "Cook Islands": "cha",
            "Costa Rica": "spa",
            "Croatia": "cro",
            "Cuba": "spa",
            "Curacao": "fle",
            "Cyprus": "gre",
            "Czech Republic": "cze",
            "Denmark": "dan",
            "Djibouti": "afr",
            "Dominican Republic": "spa",
            "Dominica": "pcd",
            "DR Congo": "kon",
            "Ecuador": "map",
            "Egypt": "cop",
            "El Salvador": "spa",
            "England": "eng",
            "Equatorial Guinea": "afr",
            "Eritrea": "tig",
            "Estonia": "est",
            "Eswatini": "swz",
            "Ethiopia": "tig",
            "Faroe Islands": "fae",
            "Fiji": "fij",
            "Finland": "fin",
            "France": "fre",
            "Gabon": "fre",
            "Georgia": "geo",
            "Germany": "ger",
            "Ghana": "aka",
            "Gibraltar": "geo",
            "Greece": "gre",
            "Greenland": "grn",
            "Grenada": "nrm",
            "Guam": "cha",
            "Guadeloupe": "fre",
            "Guatemala": "spa",
            "Guinea": "afr",
            "Guinea-Bissau": "afr",
            "Guyana": "nrm",
            "Haiti": "fre",
            "Honduras": "spa",
            "Hong Kong": "chi",
            "Hungary": "hun",
            "Iceland": "ice",
            "India": "ind",
            "Indonesia": "ins",
            "Iran": "per",
            "Iraq": "per",
            "Ireland": "iri",
            "Israel": "heb",
            "Italy": "ita",
            "Ivory Coast": "aka",
            "Jamaica": "afr",
            "Jordan": "afr",
            "Kazakhstan": "kaz",
            "Kenya": "luh",
            "Kirain": "ame",
            "Kiribati": "fij",
            "Kosovo": "alb",
            "Kurdistan": "kur",
            "Kuwait": "ara",
            "Kyrgyzstan": "kyr",
            "Laos": "lao",
            "Latvia": "lat",
            "Lebanon": "arm",
            "Lesotho": "sot",
            "Liberia": "afr",
            "Libya": "ara",
            "Liechtenstein": "ger",
            "Lithuania": "lth",
            "Luxembourg": "lim",
            "Macau": "chi",
            "Madagascar": "afr",
            "Malawi": "cew",
            "Malaysia": "mly",
            "Maldives": "dhi",
            "Mali": "som",
            "Malta": "mal",
            "Mapuche": "map",
            "Martinique": "fre",
            "Mauritania": "afr",
            "Mauritius": "afr",
            "Manchuoko": "jap",
            "Marshall Islands": "cha",
            "Mexico": "spa",
            "Micronesia": "fij",
            "Moldova": "mol",
            "Mongolia": "mon",
            "Montenegro": "alb",
            "Montserrat": "nrm",
            "Morocco": "ara",
            "Mozambique": "yao",
            "Myanmar": "bur",
            "Namibia": "afk",
            "Nauru": "cha",
            "Nepal": "nep",
            "Netherlands": "dut",
            "New Caledonia": "fre",
            "New Zealand": "eng",
            "Nicaragua": "spa",
            "Niger": "afr",
            "Nigeria": "afr",
            "Niue": "ton",
            "North Korea": "kor",
            "North Macedonia": "mac",
            "Northern Ireland": "iri",
            "Norway": "nor",
            "Oman": "ara",
            "Pakistan": "pas",
            "Palestine": "ara",
            "Palau": "ton",
            "Panama": "spa",
            "Papua New Guinea": "eng",
            "Paraguay": "spa",
            "Peru": "spa",
            "Philippines": "tag",
            "Poland": "pol",
            "Portugal": "por",
            "Puerto Rico": "spa",
            "Qatar": "ara",
            "Republic of Samoa": "sam",
            "Romania": "rmn",
            "Russia": "rus",
            "Rwanda": "kig",
            "Saint Kitts & Nevis": "eng",
            "Saint Lucia": "eng",
            "Saint Vincent & the Grenadines": "eng",
            "Samoa": "sam",
            "San Marino": "ita",
            "Sao Tome & Principe": "afr",
            "Saudi Arabia": "ara",
            "Scotland": "sco",
            "Sealand": "eng",
            "Serbia": "ser",
            "Seychelles": "afr",
            "Sierra Leone": "afr",
            "Singapore": "mly",
            "Slovakia": "slk",
            "Slovenia": "sln",
            "Solomon Islands": "eng",
            "Somalia": "som",
            "South Africa": "afr",
            "South Sudan": "afr",
            "Spain": "spa",
            "Sri Lanka": "tam",
            "Sudan": "afr",
            "Suriname": "dut",
            "Sweden": "swe",
            "Switzerland": "ger",
            "Syria": "ara",
            "Tahiti": "tah",
            "Taiwan": "chi",
            "Tajikistan": "taj",
            "Tanzania": "tum",
            "Thailand": "tha",
            "Timor Leste": "por",
            "Togo": "afr",
            "Tokelau": "fij",
            "Tonga": "ton",
            "Trinidad & Tobago": "eng",
            "Tunisia": "afr",
            "Turkey": "tur",
            "Turkmenistan": "tkm",
            "Turks & Caicos Islands": "eng",
            "Tuvalu": "fij",
            "Uganda": "afr",
            "Ukraine": "ukr",
            "United Arab Emirates": "ara",
            "Uruguay": "spa",
            "US Virgin Islands": "eng",
            "USA": "eng",
            "Uzbekistan": "uzb",
            "Vanuatu": "tah",
            "Venezuela": "spa",
            "Vietnam": "vie",
            "Wales": "wel",
            "Wallis & Futuna": "fre",
            "Zambia": "tum",
            "Zimbabwe": "sho",
            "Aland": "dan",
            "Angola": "afr",
            "Antarctica": "eng",
            "Australia": "eng",
            "Bouvet Island": "fre",
            "Cameroon": "afr",
            "China": "chi",
            "Christmas Island": "eng",
            "Cocos Islands": "eng",
            "Falkland Islands": "ger",
            "French Guiana": "fre",
            "Gambia": "afr",
            "Guernsey": "eng",
            "Heard Island": "eng",
            "Holy See": "eng",
            "Isle of Man": "eng",
            "Japan": "jap",
            "Jersey": "eng",
            "South Korea": "kor",
            "Mayotte": "fre",
            "Mcdonald Islands": "eng",
            "Monaco": "fre",
            "Norfolk Island": "ger",
            "Northern Mariana Islands": "eng",
            "Pitcairn": "eng",
            "Reunion": "fre",
            "Saint Helena": "eng",
            "Saint Pierre & Miquelon": "fre",
            "Senegal": "afr",
            "Sint Maarten": "dut",
            "South Sandwich Islands": "eng",
            "Svalbard": "swe",
            "Western Sahara": "afr",
            "Yemen": "ara"
        }

        country = countries_dict[nationality]
        gender = 'f'

        url = f'https://www.behindthename.com/api/random.json?usage={country}&gender={gender}&randomsurname=yes&number=1&key=ja891397252'

        name_response = requests.get(url)
        time.sleep(1)
        name = 'Player'

        if name_response.status_code == 200:
            name_json = name_response.json()
            name = name_json['names'][0] + " " + name_json['names'][1]

        new_player = Player(team=team.parent_club, feeder_team=team, position=positions[random.randint(0, len(positions) - 1)],
                            name=name, age=age, sex='Female',
                            overall=overall, potential=potential, nationality=nationality, tactic=tactic,
                            wage=50, contract_length=2)

        new_player.save()

        new_notification = notification(team=team.parent_club,
                                        message=f"{team.name}'s level has decreased by {level_decrease}.")
        new_notification.save()

        team.parent_club.new_message = True
        team.parent_club.save()

    return redirect('admin-panel')

def create_youth_players():
    for team in Team.objects.all():
        youth_academy = team.youth_academy

        ya_amounts = {
            1 : 3,
            2 : 3,
            3 : 4,
            4 : 4,
            5 : 5
        }

        ya_ratings = {
            1 : [35, 55],
            2 : [40, 60],
            3 : [50, 65],
            4 : [68, 72],
            5 : [70, 78]
        }

        ya_potentials = {
            1: 78,
            2: 80,
            3: 85,
            4: 88,
            5: 90
        }

        ya_decrease_chances = {
            1: 80,
            2: 70,
            3: 60,
            4: 50,
            5: 40,
        }

        amount = ya_amounts[youth_academy]

        positions = ['GK', 'LWB', 'LB', 'CB', 'RB', 'RWB',
                     'CDM', 'LM', 'CM', 'RM', 'CAM',
                     'LW', 'CF', 'ST', 'RW']

        tactics = ['Gegennaccio', 'Catenaccio', 'Route One', 'Counter Attacking', 'Balanced', 'Control Possession',
                   'Tiki-Taka', 'Gegenpress', 'Wing Play']

        for player in range(amount):
            overall = random.randint(ya_ratings[youth_academy][0], ya_ratings[youth_academy][1])

            potential = random.randint(overall, ya_potentials[youth_academy])

            potential_decrease_chance = random.randint(0, 100)

            if potential_decrease_chance <= ya_decrease_chances[youth_academy]:
                potential -= random.randint(1,10)

            if potential < overall:
                potential += overall + random.randint(0,3)

            feeder_team = Feeder_Team.objects.filter(parent_club=team)

            print(team)
            print(feeder_team)

            feeder_team = feeder_team[0]

            nationality = feeder_team.nation

            tactic = tactics[random.randint(0, len(tactics) - 1)]

            age = random.randint(13, 19)

            countries_dict = {
                "Afghanistan": "pas",
                "Albania": "alb",
                "Algeria": "afr",
                "American Samoa": "smn",
                "Andorra": "cat",
                "Anguilla": "nrm",
                "Antigua & Barbuda": "nrm",
                "Argentina": "spa",
                "Armenia": "arm",
                "Aruba": "cha",
                "Austria": "ger",
                "Azerbaijan": "aze",
                "Bahamas": "cha",
                "Bahrain": "ara",
                "Bangladesh": "ben",
                "Barbados": "nrm",
                "Belarus": "bel",
                "Belgium": "dut",
                "Belize": "cha",
                "Benin": "afr",
                "Bermuda": "nrm",
                "Bhutan": "bhu",
                "Bolivia": "aym",
                "Bonaire": "dut",
                "Bosnia & Herzegovina": "bos",
                "Botswana": "tsw",
                "Brazil": "por",
                "British Virgin Islands": "nrm",
                "Brunei": "mly",
                "Bulgaria": "bul",
                "Burkina Faso": "afr",
                "Burundi": "afr",
                "Cambodia": "khm",
                "Canada": "sio",
                "Cape Verde": "por",
                "Catalonia": "cat",
                "Cayman Islands": "nrm",
                "Central African Republic": "afr",
                "Chad": "afr",
                "Chile": "spa",
                "Colombia": "spa",
                "Comoros": "cmr",
                "Congo": "kon",
                "Cook Islands": "cha",
                "Costa Rica": "spa",
                "Croatia": "cro",
                "Cuba": "spa",
                "Curacao": "fle",
                "Cyprus": "gre",
                "Czech Republic": "cze",
                "Denmark": "dan",
                "Djibouti": "afr",
                "Dominican Republic": "spa",
                "Dominica": "pcd",
                "DR Congo": "kon",
                "Ecuador": "map",
                "Egypt": "cop",
                "El Salvador": "spa",
                "England": "eng",
                "Equatorial Guinea": "afr",
                "Eritrea": "tig",
                "Estonia": "est",
                "Eswatini": "swz",
                "Ethiopia": "tig",
                "Faroe Islands": "fae",
                "Fiji": "fij",
                "Finland": "fin",
                "France": "fre",
                "Gabon": "fre",
                "Georgia": "geo",
                "Germany": "ger",
                "Ghana": "aka",
                "Gibraltar": "geo",
                "Greece": "gre",
                "Greenland": "grn",
                "Grenada": "nrm",
                "Guam": "cha",
                "Guadeloupe": "fre",
                "Guatemala": "spa",
                "Guinea": "afr",
                "Guinea-Bissau": "afr",
                "Guyana": "nrm",
                "Haiti": "fre",
                "Honduras": "spa",
                "Hong Kong": "chi",
                "Hungary": "hun",
                "Iceland": "ice",
                "India": "ind",
                "Indonesia": "ins",
                "Iran": "per",
                "Iraq": "per",
                "Ireland": "iri",
                "Israel": "heb",
                "Italy": "ita",
                "Ivory Coast": "aka",
                "Jamaica": "afr",
                "Jordan": "afr",
                "Kazakhstan": "kaz",
                "Kenya": "luh",
                "Kirain": "ame",
                "Kiribati": "fij",
                "Kosovo": "alb",
                "Kurdistan": "kur",
                "Kuwait": "ara",
                "Kyrgyzstan": "kyr",
                "Laos": "lao",
                "Latvia": "lat",
                "Lebanon": "arm",
                "Lesotho": "sot",
                "Liberia": "afr",
                "Libya": "ara",
                "Liechtenstein": "ger",
                "Lithuania": "lth",
                "Luxembourg": "lim",
                "Macau": "chi",
                "Madagascar": "afr",
                "Malawi": "cew",
                "Malaysia": "mly",
                "Maldives": "dhi",
                "Mali": "som",
                "Malta": "mal",
                "Mapuche": "map",
                "Martinique": "fre",
                "Mauritania": "afr",
                "Mauritius": "afr",
                "Manchuoko": "jap",
                "Marshall Islands": "cha",
                "Mexico": "spa",
                "Micronesia": "fij",
                "Moldova": "mol",
                "Mongolia": "mon",
                "Montenegro": "alb",
                "Montserrat": "nrm",
                "Morocco": "ara",
                "Mozambique": "yao",
                "Myanmar": "bur",
                "Namibia": "afk",
                "Nauru": "cha",
                "Nepal": "nep",
                "Netherlands": "dut",
                "New Caledonia": "fre",
                "New Zealand": "eng",
                "Nicaragua": "spa",
                "Niger": "afr",
                "Nigeria": "afr",
                "Niue": "ton",
                "North Korea": "kor",
                "North Macedonia": "mac",
                "Northern Ireland": "iri",
                "Norway": "nor",
                "Oman": "ara",
                "Pakistan": "pas",
                "Palestine": "ara",
                "Palau": "ton",
                "Panama": "spa",
                "Papua New Guinea": "eng",
                "Paraguay": "spa",
                "Peru": "spa",
                "Philippines": "tag",
                "Poland": "pol",
                "Portugal": "por",
                "Puerto Rico": "spa",
                "Qatar": "ara",
                "Republic of Samoa": "sam",
                "Romania": "rmn",
                "Russia": "rus",
                "Rwanda": "kig",
                "Saint Kitts & Nevis": "eng",
                "Saint Lucia": "eng",
                "Saint Vincent & the Grenadines": "eng",
                "Samoa": "sam",
                "San Marino": "ita",
                "Sao Tome & Principe": "afr",
                "Saudi Arabia": "ara",
                "Scotland": "sco",
                "Sealand": "eng",
                "Serbia": "ser",
                "Seychelles": "afr",
                "Sierra Leone": "afr",
                "Singapore": "mly",
                "Slovakia": "slk",
                "Slovenia": "sln",
                "Solomon Islands": "eng",
                "Somalia": "som",
                "South Africa": "afr",
                "South Sudan": "afr",
                "Spain": "spa",
                "Sri Lanka": "tam",
                "Sudan": "afr",
                "Suriname": "dut",
                "Sweden": "swe",
                "Switzerland": "ger",
                "Syria": "ara",
                "Tahiti": "tah",
                "Taiwan": "chi",
                "Tajikistan": "taj",
                "Tanzania": "tum",
                "Thailand": "tha",
                "Timor Leste": "por",
                "Togo": "afr",
                "Tokelau": "fij",
                "Tonga": "ton",
                "Trinidad & Tobago": "eng",
                "Tunisia": "afr",
                "Turkey": "tur",
                "Turkmenistan": "tkm",
                "Turks & Caicos Islands": "eng",
                "Tuvalu": "fij",
                "Uganda": "afr",
                "Ukraine": "ukr",
                "United Arab Emirates": "ara",
                "Uruguay": "spa",
                "US Virgin Islands": "eng",
                "USA": "eng",
                "Uzbekistan": "uzb",
                "Vanuatu": "tah",
                "Venezuela": "spa",
                "Vietnam": "vie",
                "Wales": "wel",
                "Wallis & Futuna": "fre",
                "Zambia": "tum",
                "Zimbabwe": "sho",
                "Aland": "dan",
                "Angola": "afr",
                "Antarctica": "eng",
                "Australia": "eng",
                "Bouvet Island": "fre",
                "Cameroon": "afr",
                "China": "chi",
                "Christmas Island": "eng",
                "Cocos Islands": "eng",
                "Falkland Islands": "ger",
                "French Guiana": "fre",
                "Gambia": "afr",
                "Guernsey": "eng",
                "Heard Island": "eng",
                "Holy See": "eng",
                "Isle of Man": "eng",
                "Japan": "jap",
                "Jersey": "eng",
                "South Korea": "kor",
                "Mayotte": "fre",
                "Mcdonald Islands": "eng",
                "Monaco": "fre",
                "Norfolk Island": "ger",
                "Northern Mariana Islands": "eng",
                "Pitcairn": "eng",
                "Reunion": "fre",
                "Saint Helena": "eng",
                "Saint Pierre & Miquelon": "fre",
                "Senegal": "afr",
                "Sint Maarten": "dut",
                "South Sandwich Islands": "eng",
                "Svalbard": "swe",
                "Western Sahara": "afr",
                "Yemen": "ara"
            }

            country = countries_dict[nationality]
            gender = 'm'

            url = f'https://www.behindthename.com/api/random.json?usage={country}&gender={gender}&randomsurname=yes&number=1&key=ja891397252'

            name_response = requests.get(url)
            time.sleep(1)
            name = 'Player'

            if name_response.status_code == 200:
                name_json = name_response.json()
                name = name_json['names'][0] + " " + name_json['names'][1]

            new_player = Player(team=team, feeder_team=feeder_team, position=positions[random.randint(0,len(positions)-1)],
                                 name=name, age=age, sex='Male',
                                overall=overall, potential=potential, nationality=nationality, tactic=tactic,
                                wage=50, contract_length=2)

            new_player.save()

            new_notification = notification(team=team,
                                            message=f"{new_player.name} has been added to your D-League team.")
            new_notification.save()

            team.new_message = True
            team.save()

@login_required
def release_player(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        player = Player.objects.get(pk=player_id)
        requested_wage = calculate_wage(player.overall)
        requested_contract_length = random.randint(1, 5)
        player.release_player()
        player.wage = requested_wage
        player.contract_length = requested_contract_length
        player.save()

    return redirect('expired-players')

@login_required
def recall_loan(request):
    if request.method == 'POST':
        team = Team.objects.get(owner=request.user)
        if team.can_transfer:
            player_id = request.POST.get('player_id')
            player = Player.objects.get(pk=player_id)

            loaning_team = Team.objects.get(name=player.loaned_to)

            new_notification = notification(team=loaning_team,
                                            message=f"{player.name} has been recalled from loan.")
            new_notification.save()

            loaning_team.new_message = True
            loaning_team.save()

            player.return_loan()

    return redirect('manage-team')

@login_required
def advance_season(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    players = Player.objects.all()

    for player in players:
        player.overall += random.randint(0,player.team.training_facilties)

        if player.overall > player.potential:
            player.potential = player.overall

        player_potential_growth_chance = random.randint(1, 100)

        if player_potential_growth_chance <= 15 and player.age <= 26:
            player.potential += random.randint(0,3)

        player.age += 1

        player.contract_length -= 1

        if player.contract_length < 0:
            player.contract_length = 0

        skill_point_parameters = {
            1 : [3,7],
            2 : [5,10],
            3 : [10,20],
            4 : [20,35],
            5 : [35,50]
        }

        skill_points = random.randint(skill_point_parameters[player.team.training_facilties][0], skill_point_parameters[player.team.training_facilties][1])

        player.skill_points += skill_points

        player.save()

    create_youth_players()
    return_loans_offseason()
    update_womens_teams_offseason()
    update_scouted_players_offseason()

    return redirect('admin-panel')

@login_required
def team_lineup(request):
    team = Team.objects.get(owner=request.user)
    players = Player.objects.filter(team=team, feeder_team=None, loaned='N/A', free_agent=False)
    loaned_players = Player.objects.filter(loaned_to=team.name, feeder_team=None, free_agent=False)
    players = players.union(loaned_players)

    positions_by_formation = {
        '3-4-3' : ['GK', 'CB', 'CB', 'CB',
                    'LM', 'CM', 'CM', 'RM',
                    'ST', 'ST', 'ST'],

        '3-5-2' : ['GK', 'CB', 'CB', 'CB',
                    'LM', 'CM', 'CDM', 'CM', 'RM',
                    'ST', 'ST'],

        '4-4-2' : ['GK', 'LB', 'CB', 'CB', 'RB',
                   'LM', 'CM', 'CM', 'RM',
                   'ST', 'ST'],

        '4-2-3-1' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CM',
                    'LW', 'CAM', 'RW',
                    'ST'],

        '4-3-3' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CM', 'CM',
                    'LW', 'ST', 'RW'],

        '4-5-1' : ['GK', 'LB', 'CB', 'CB', 'RB',
         'LM', 'CM', 'CDM', 'CM', 'RM',
         'ST'],

        '4-2-2-2' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CDM', 'CDM',
                    'CAM', 'CAM',
                    'ST', 'ST'],

        '4-2-4' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CM',
                    'LW', 'ST', 'ST', 'RW'],

        '4-4-1-1' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'LM', 'CM', 'CM', 'RM',
                    'CAM',
                    'ST'],

        '4-1-2-1-2' : ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CDM', 'CM',
                    'CAM',
                    'ST', 'ST'],

        '5-3-2' : ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'CM', 'CM', 'CM',
                    'ST', 'ST'],

        '5-2-3' : ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'CM', 'CM',
                    'LW', 'ST', 'RW'],

        '5-4-1' : ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'LM', 'CM', 'CM', 'RM',
                    'ST'],

        '5-2-1-2' : ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'CM', 'CM',
                    'CAM',
                    'ST', 'ST']
    }

    positions = positions_by_formation[team.formation]

    lineup_object = lineup.objects.get(team=team)
    team_lineup = lineup_object.get_lineup()

    player_1 = team_lineup[0]
    player_2 = team_lineup[1]
    player_3 = team_lineup[2]
    player_4 = team_lineup[3]
    player_5 = team_lineup[4]
    player_6 = team_lineup[5]
    player_7 = team_lineup[6]
    player_8 = team_lineup[7]
    player_9 = team_lineup[8]
    player_10 = team_lineup[9]
    player_11 = team_lineup[10]
    player_12 = team_lineup[11]
    player_13 = team_lineup[12]
    player_14 = team_lineup[13]
    player_15 = team_lineup[14]
    player_16 = team_lineup[15]
    player_17 = team_lineup[16]
    player_18 = team_lineup[17]
    player_19 = team_lineup[18]
    player_20 = team_lineup[19]
    player_21 = team_lineup[20]
    player_22 = team_lineup[21]
    player_23 = team_lineup[22]

    position_1 = positions[0]
    position_2 = positions[1]
    position_3 = positions[2]
    position_4 = positions[3]
    position_5 = positions[4]
    position_6 = positions[5]
    position_7 = positions[6]
    position_8 = positions[7]
    position_9 = positions[8]
    position_10 = positions[9]
    position_11 = positions[10]

    team_lineup = team_lineup[:11]

    context = {
        'team': team,
        'players' : players,
        'positions' : positions,
        'lineup' : lineup_object,
        'team_lineup' : team_lineup,
        'player_1' : player_1,
        'player_2' : player_2,
        'player_3' : player_3,
        'player_4' : player_4,
        'player_5' : player_5,
        'player_6' : player_6,
        'player_7' : player_7,
        'player_8' : player_8,
        'player_9' : player_9,
        'player_10' : player_10,
        'player_11' : player_11,
        'player_12': player_12,
        'player_13': player_13,
        'player_14': player_14,
        'player_15': player_15,
        'player_16': player_16,
        'player_17': player_17,
        'player_18': player_18,
        'player_19': player_19,
        'player_20': player_20,
        'player_21': player_21,
        'player_22': player_22,
        'player_23': player_23,
        'position_1' : position_1,
        'position_2' : position_2,
        'position_3' : position_3,
        'position_4' : position_4,
        'position_5' : position_5,
        'position_6' : position_6,
        'position_7' : position_7,
        'position_8' : position_8,
        'position_9' : position_9,
        'position_10' : position_10,
        'position_11' : position_11,
    }

    return render(request, 'management/lineup.html', context)

@login_required
def set_formation(request):
    team = Team.objects.get(owner=request.user)

    team.formation = request.POST.get('formation')

    team.save()

    return redirect('lineup')

@login_required
def set_tactic(request):
    team = Team.objects.get(owner=request.user)

    team.tactic = request.POST.get('tactic')

    team.save()

    return redirect('lineup')

@login_required
def set_mentality(request):
    team = Team.objects.get(owner=request.user)

    team.mentality = request.POST.get('mentality')

    team.save()

    return redirect('lineup')

def get_player_rating_by_position(player):
    positions = player.position.split('/')

    ratings = []

    position_rating_changes = {
        "LB": {
            "LB": 0,
            "LWB": 0,
            "CB": 5,
            "RB": 2,
            "RWB": 2,
            "LM": 20,
            "LW": 20,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 20
        },
        "LWB": {
            "LB": 0,
            "LWB": 0,
            "CB": 5,
            "RB": 2,
            "RWB": 2,
            "LM": 3,
            "LW": 3,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 3,
            "RW": 3,
            "CF": 20,
            "ST": 20
        },
        "CB": {
            "LB": 5,
            "LWB": 10,
            "CB": 0,
            "RB": 5,
            "RWB": 10,
            "LM": 20,
            "LW": 20,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 20
        },
        "RB": {
            "LB": 2,
            "LWB": 2,
            "CB": 5,
            "RB": 0,
            "RWB": 0,
            "LM": 20,
            "LW": 20,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 20
        },
        "RWB": {
            "LB": 2,
            "LWB": 2,
            "CB": 5,
            "RB": 0,
            "RWB": 0,
            "LM": 3,
            "LW": 3,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 3,
            "RW": 3,
            "CF": 20,
            "ST": 20
        },
        "LM": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 0,
            "LW": 0,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 2,
            "RW": 2,
            "CF": 20,
            "ST": 20
        },
        "LW": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 0,
            "LW": 0,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 2,
            "RW": 2,
            "CF": 20,
            "ST": 20
        },
        "CM": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 20,
            "LW": 20,
            "CDM": 3,
            "CM": 0,
            "CAM": 3,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 20
        },
        "RM": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 2,
            "LW": 2,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 0,
            "RW": 0,
            "CF": 20,
            "ST": 20
        },
        "RW": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 2,
            "LW": 2,
            "CDM": 20,
            "CM": 20,
            "CAM": 20,
            "RM": 0,
            "RW": 0,
            "CF": 20,
            "ST": 20
        },
        "CDM": {
            "LB": 20,
            "LWB": 20,
            "CB": 3,
            "RB": 20,
            "RWB": 20,
            "LM": 20,
            "LW": 20,
            "CDM": 0,
            "CM": 3,
            "CAM": 5,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 20
        },
        "CAM": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 20,
            "LW": 20,
            "CDM": 5,
            "CM": 3,
            "CAM": 0,
            "RM": 20,
            "RW": 20,
            "CF": 20,
            "ST": 10
        },
        "CF": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 20,
            "LW": 20,
            "CDM": 20,
            "CM": 20,
            "CAM": 1,
            "RM": 20,
            "RW": 20,
            "CF": 0,
            "ST": 0
        },
        "ST": {
            "LB": 20,
            "LWB": 20,
            "CB": 20,
            "RB": 20,
            "RWB": 20,
            "LM": 20,
            "LW": 20,
            "CDM": 20,
            "CM": 20,
            "CAM": 10,
            "RM": 20,
            "RW": 20,
            "CF": 0,
            "ST": 0
        },
    }

    for position in positions:
        if position == 'GK':
            if player.lineup_position != 'GK':
                ratings.append(10)
            else:
                ratings.append(player.overall)
        else:
            ratings.append(player.overall - position_rating_changes[position][player.lineup_position])

    player.lineup_rating = max(ratings)

    tactic_rating_changes = {
        "Balanced" : {
            "Catenaccio" : 0,
            "Gegennaccio" : 0,
            "Route One" : 0,
            "Counter-Attack" : 0,
            "Balanced" : 0,
            "Control Possession" : 0,
            "Tiki-Taka" : 0,
            "Gegenpress" : 0,
            "Wing Play" : 0
        },
        "Catenaccio": {
            "Catenaccio": 2,
            "Gegennaccio": 0,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": -2,
            "Gegenpress": -2,
            "Wing Play": -2
        },
        "Gegennaccio": {
            "Catenaccio": 0,
            "Gegennaccio": 2,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": -2,
            "Gegenpress": -2,
            "Wing Play": -2
        },
        "Route One": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": 2,
            "Counter-Attack": 0,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": -2,
            "Gegenpress": -2,
            "Wing Play": -2
        },
        "Counter Attacking": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": 0,
            "Counter-Attack": 2,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": -2,
            "Gegenpress": -2,
            "Wing Play": -2
        },
        "Control Possession": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": 2,
            "Tiki-Taka": -2,
            "Gegenpress": 0,
            "Wing Play": -2
        },
        "Gegenpress": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": 0,
            "Tiki-Taka": -2,
            "Gegenpress": 2,
            "Wing Play": -2
        },
        "Tiki-Taka": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": 2,
            "Gegenpress": -2,
            "Wing Play": 0
        },
        "Wing Play": {
            "Catenaccio": -2,
            "Gegennaccio": -2,
            "Route One": -2,
            "Counter-Attack": -2,
            "Balanced": -1,
            "Control Possession": -2,
            "Tiki-Taka": 0,
            "Gegenpress": -2,
            "Wing Play": 2
        }
    }

    player.lineup_rating += tactic_rating_changes[player.tactic][player.team.tactic]

    player.save()

def calculate_lineup_ratings(team):
    team_lineup = lineup.objects.get(team=team)
    starting_eleven = team_lineup.get_lineup()
    lineup_overall = 0

    for i in range(11):
        print(starting_eleven[i].lineup_rating)
        lineup_overall += starting_eleven[i].lineup_rating

    lineup_overall /= 11
    lineup_overall = round(lineup_overall)

    team_lineup.overall = lineup_overall
    team_lineup.save()

    return redirect('lineup')

@login_required
def set_lineup(request):
    team = Team.objects.get(owner=request.user)
    team_lineup = lineup.objects.get(team=team)

    player_1_id = request.POST.get('player_1')
    player_2_id = request.POST.get('player_2')
    player_3_id = request.POST.get('player_3')
    player_4_id = request.POST.get('player_4')
    player_5_id = request.POST.get('player_5')
    player_6_id = request.POST.get('player_6')
    player_7_id = request.POST.get('player_7')
    player_8_id = request.POST.get('player_8')
    player_9_id = request.POST.get('player_9')
    player_10_id = request.POST.get('player_10')
    player_11_id = request.POST.get('player_11')
    player_12_id = request.POST.get('player_12')
    player_13_id = request.POST.get('player_13')
    player_14_id = request.POST.get('player_14')
    player_15_id = request.POST.get('player_15')
    player_16_id = request.POST.get('player_16')
    player_17_id = request.POST.get('player_17')
    player_18_id = request.POST.get('player_18')
    player_19_id = request.POST.get('player_19')
    player_20_id = request.POST.get('player_20')
    player_21_id = request.POST.get('player_21')
    player_22_id = request.POST.get('player_22')
    player_23_id = request.POST.get('player_23')

    positions_by_formation = {
        '3-4-3': ['GK', 'CB', 'CB', 'CB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST', 'ST', 'ST'],

        '3-5-2': ['GK', 'CB', 'CB', 'CB',
                  'LM', 'CM', 'CDM', 'CM', 'RM',
                  'ST', 'ST'],

        '4-4-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST', 'ST'],

        '4-2-3-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CM',
                    'LW', 'CAM', 'RW',
                    'ST'],

        '4-3-3': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'CM', 'CM', 'CM',
                  'LW', 'ST', 'RW'],

        '4-5-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'LM', 'CM', 'CDM', 'CM', 'RM',
                  'ST'],

        '4-2-2-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CDM', 'CDM',
                    'CAM', 'CAM',
                    'ST', 'ST'],

        '4-2-4': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'CM', 'CM',
                  'LW', 'ST', 'ST', 'RW'],

        '4-4-1-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'LM', 'CM', 'CM', 'RM',
                    'CAM',
                    'ST'],

        '4-1-2-1-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                      'CM', 'CDM', 'CM',
                      'CAM',
                      'ST', 'ST'],

        '5-3-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'CM', 'CM', 'CM',
                  'ST', 'ST'],

        '5-2-3': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'CM', 'CM',
                  'LW', 'ST', 'RW'],

        '5-4-1': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST'],

        '5-2-1-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'CM', 'CM',
                    'CAM',
                    'ST', 'ST']
    }

    positions = positions_by_formation[team.formation]

    if player_1_id != None:
        team_lineup.player_1 = Player.objects.get(pk=player_1_id)
    if player_2_id != None:
        team_lineup.player_2 = Player.objects.get(pk=player_2_id)
    if player_3_id != None:
        team_lineup.player_3 = Player.objects.get(pk=player_3_id)
    if player_4_id != None:
        team_lineup.player_4 = Player.objects.get(pk=player_4_id)
    if player_5_id != None:
        team_lineup.player_5 = Player.objects.get(pk=player_5_id)
    if player_6_id != None:
        team_lineup.player_6 = Player.objects.get(pk=player_6_id)
    if player_7_id != None:
        team_lineup.player_7 = Player.objects.get(pk=player_7_id)
    if player_8_id != None:
        team_lineup.player_8 = Player.objects.get(pk=player_8_id)
    if player_9_id != None:
        team_lineup.player_9 = Player.objects.get(pk=player_9_id)
    if player_10_id != None:
        team_lineup.player_10 = Player.objects.get(pk=player_10_id)
    if player_11_id != None:
        team_lineup.player_11 = Player.objects.get(pk=player_11_id)
    if player_12_id != None:
        team_lineup.player_12 = Player.objects.get(pk=player_12_id)
    if player_13_id != None:
        team_lineup.player_13 = Player.objects.get(pk=player_13_id)
    if player_14_id != None:
        team_lineup.player_14 = Player.objects.get(pk=player_14_id)
    if player_15_id != None:
        team_lineup.player_15 = Player.objects.get(pk=player_15_id)
    if player_16_id != None:
        team_lineup.player_16 = Player.objects.get(pk=player_16_id)
    if player_17_id != None:
        team_lineup.player_17 = Player.objects.get(pk=player_17_id)
    if player_18_id != None:
        team_lineup.player_18 = Player.objects.get(pk=player_18_id)
    if player_19_id != None:
        team_lineup.player_19 = Player.objects.get(pk=player_19_id)
    if player_20_id != None:
        team_lineup.player_20 = Player.objects.get(pk=player_20_id)
    if player_21_id != None:
        team_lineup.player_21 = Player.objects.get(pk=player_21_id)
    if player_22_id != None:
        team_lineup.player_22 = Player.objects.get(pk=player_22_id)
    if player_23_id != None:
        team_lineup.player_23 = Player.objects.get(pk=player_23_id)

    position_counter = 0
    for player in team_lineup.get_lineup():
        if position_counter < 11:
            player.lineup_position = positions[position_counter]
            player.save()
            get_player_rating_by_position(player)
            if player.name == 'Fortunato Núñez':
                print(player.lineup_position,player.lineup_rating)
            position_counter += 1

    team_lineup.save()

    calculate_lineup_ratings(team)

    return redirect('lineup')

@login_required
def submit_lineup(request):
    team = Team.objects.get(owner=request.user)
    team_lineup = lineup.objects.get(team=team)

    positions_by_formation = {
        '3-4-3': ['GK', 'CB', 'CB', 'CB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST', 'ST', 'ST'],

        '3-5-2': ['GK', 'CB', 'CB', 'CB',
                  'LM', 'CM', 'CDM', 'CM', 'RM',
                  'ST', 'ST'],

        '4-4-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST', 'ST'],

        '4-2-3-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CM', 'CM',
                    'LW', 'CAM', 'RW',
                    'ST'],

        '4-3-3': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'CM', 'CM', 'CM',
                  'LW', 'ST', 'RW'],

        '4-5-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'LM', 'CM', 'CDM', 'CM', 'RM',
                  'ST'],

        '4-2-2-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'CDM', 'CDM',
                    'CAM', 'CAM',
                    'ST', 'ST'],

        '4-2-4': ['GK', 'LB', 'CB', 'CB', 'RB',
                  'CM', 'CM',
                  'LW', 'ST', 'ST', 'RW'],

        '4-4-1-1': ['GK', 'LB', 'CB', 'CB', 'RB',
                    'LM', 'CM', 'CM', 'RM',
                    'CAM',
                    'ST'],

        '4-1-2-1-2': ['GK', 'LB', 'CB', 'CB', 'RB',
                      'CM', 'CDM', 'CM',
                      'CAM',
                      'ST', 'ST'],

        '5-3-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'CM', 'CM', 'CM',
                  'ST', 'ST'],

        '5-2-3': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'CM', 'CM',
                  'LW', 'ST', 'RW'],

        '5-4-1': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                  'LM', 'CM', 'CM', 'RM',
                  'ST'],

        '5-2-1-2': ['GK', 'LWB', 'CB', 'CB', 'CB', 'RWB',
                    'CM', 'CM',
                    'CAM',
                    'ST', 'ST']
    }

    positions = positions_by_formation[team.formation]

    body = f"""
        Tactic: {team.tactic}
        Mentality: {team.mentality}
        Formation: {team.formation}
        
        Starting XI
    """

    position_counter = 0

    for player in team_lineup.get_lineup():
        if player != None:
            if position_counter < 11:
                body += f"""
                    {positions[position_counter]}: {player.name}
                        Duty: {player.duty}
                        Dribbling: {player.dribbling}
                        Shooting: {player.shooting}
                        Risk Taking: {player.risk_taking}
                        Tackling: {player.tackling}
                        Freedom: {player.freedom}
                        
                """
                position_counter += 1
            else:
                if position_counter == 11:
                    body += "Substitutes\n"
                    position_counter += 1
                body += f"""
                    {player.name}
                        Duty: {player.duty}
                        Dribbling: {player.dribbling}
                        Shooting: {player.shooting}
                        Risk Taking: {player.risk_taking}
                        Tackling: {player.tackling}
                        Freedom: {player.freedom}
                        
                """
        else:
            body += "None\n\n"

    msg = EmailMessage()

    msg.set_content(body)
    msg['Subject'] = f'Tactics & Lineup for {team.name}'
    msg['From'] = 'jahirmunozcs@gmail.com'
    msg['To'] = 'eliteworldfantasyleague@gmail.com'

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login('jahirmunozcs@gmail.com', 'sxyi ykav yknv mcbz')
            server.send_message(msg)
        print("Lineup sent!")
    except Exception as e:
        print(e)

    return redirect('lineup')

@login_required
def player_instructions(request):
    player_id = request.POST.get('player_id')
    player = Player.objects.get(id=player_id)

    context = {
        'player': player,
    }

    return render(request, 'management/player-instructions.html', context)

@login_required
def set_player_instructions(request):
    player_id = request.POST.get('player_id')
    player = Player.objects.get(id=player_id)

    player_duty = request.POST.get('duty')
    player_dribbling = request.POST.get('dribbling')
    player_shooting = request.POST.get('shooting')
    player_risk_taking = request.POST.get('risk_taking')
    player_tackling = request.POST.get('tackling')
    player_freedom = request.POST.get('freedom')

    if player_duty != None:
        player.duty = player_duty
    if player_dribbling != None:
        player.dribbling = player_dribbling
    if player_shooting != None:
        player.shooting = player_shooting
    if player_risk_taking != None:
        player.risk_taking = player_risk_taking
    if player_tackling != None:
        player.tackling = player_tackling
    if player_freedom != None:
        player.freedom = player_freedom

    player.save()

    return redirect('lineup')

@login_required
def fix_team_wages(request):
    user = request.user
    if not user.is_superuser:
        return redirect('site-home')

    fix_wages_all()

    return redirect('admin-panel')