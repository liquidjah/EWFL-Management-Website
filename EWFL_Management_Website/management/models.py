import random
import time
import requests
import json
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, unique=True)
    logo = models.ImageField(default='default-logo.png', upload_to='team_logos')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    stadium = models.IntegerField(default=1000)
    scout = models.IntegerField(default=1)
    training_facilties = models.IntegerField(default=1)
    youth_academy = models.IntegerField(default=1)
    merchandise = models.IntegerField(default=1)

    director_of_football = models.IntegerField(default=0)
    assistant_manager = models.IntegerField(default=0)
    goalkeeping_coach = models.IntegerField(default=0)
    defending_coach = models.IntegerField(default=0)
    midfield_coach = models.IntegerField(default=0)
    attacking_coach = models.IntegerField(default=0)
    set_piece_coach = models.IntegerField(default=0)
    physiotherapist = models.IntegerField(default=0)

    transfer_budget = models.FloatField(default=5.0)
    facilities_budget = models.FloatField(default=5.0)
    wage_budget_total = models.IntegerField(default=5000)
    wage_budget_spent = models.IntegerField(default=0)
    wage_budget_remaining = models.IntegerField(default=0)

    scout_reports_remaining = models.IntegerField(default=10)

    can_transfer = models.BooleanField(default=False)

    new_message = models.BooleanField(default=False)

    tactic = models.CharField(max_length=64, default="Balanced")
    mentality = models.CharField(max_length=64, default="Balanced")
    formation = models.CharField(max_length=64, default="4-4-2")

    def upgrade_stadium(self):
        if self.facilities_budget >= 5.0:
            self.stadium += 1000
            self.facilities_budget -= 5.0
            self.save()

    def upgrade_scout(self):
        costs = {
            1: 0,
            2: 10,
            3: 30,
            4: 50,
            5: 100
        }

        if self.scout < 5:
            if self.facilities_budget >= costs[self.scout+1]:
                self.scout += 1
                self.facilities_budget -= costs[self.scout]
                self.save()

    def upgrade_training_facilities(self):
        costs = {
            1: 0,
            2: 10,
            3: 80,
            4: 150,
            5: 200
        }

        if self.training_facilties < 5:
            if self.facilities_budget >= costs[self.training_facilties + 1]:
                self.training_facilties += 1
                self.facilities_budget -= costs[self.training_facilties]
                self.save()

    def upgrade_youth_academy(self):
        costs = {
            1: 0,
            2: 10,
            3: 80,
            4: 150,
            5: 200
        }

        if self.youth_academy < 5:
            if self.facilities_budget >= costs[self.youth_academy + 1]:
                self.youth_academy += 1
                self.facilities_budget -= costs[self.youth_academy]
                self.save()

    def upgrade_merchandise(self):
        costs = {
            1: 0,
            2: 10,
            3: 80,
            4: 150,
            5: 200
        }

        if self.merchandise < 5:
            if self.facilities_budget >= costs[self.merchandise + 1]:
                self.merchandise += 1
                self.facilities_budget -= costs[self.merchandise]
                self.save()

    def upgrade_director_of_football(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.director_of_football < 5:
            if self.facilities_budget >= costs[self.director_of_football+1]:
                self.director_of_football += 1
                self.facilities_budget -= costs[self.director_of_football]
                self.save()

    def upgrade_assistant_manager(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.assistant_manager < 5:
            if self.facilities_budget >= costs[self.assistant_manager+1]:
                self.assistant_manager += 1
                self.facilities_budget -= costs[self.assistant_manager]
                self.save()

    def upgrade_goalkeeping_coach(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.goalkeeping_coach < 5:
            if self.facilities_budget >= costs[self.goalkeeping_coach+1]:
                self.goalkeeping_coach += 1
                self.facilities_budget -= costs[self.goalkeeping_coach]
                self.save()

    def upgrade_defending_coach(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.defending_coach < 5:
            if self.facilities_budget >= costs[self.defending_coach+1]:
                self.defending_coach += 1
                self.facilities_budget -= costs[self.defending_coach]
                self.save()

    def upgrade_midfield_coach(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.midfield_coach < 5:
            if self.facilities_budget >= costs[self.midfield_coach+1]:
                self.midfield_coach += 1
                self.facilities_budget -= costs[self.midfield_coach]
                self.save()

    def upgrade_attacking_coach(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.attacking_coach < 5:
            if self.facilities_budget >= costs[self.attacking_coach+1]:
                self.attacking_coach += 1
                self.facilities_budget -= costs[self.attacking_coach]
                self.save()

    def upgrade_set_piece_coach(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.set_piece_coach < 5:
            if self.facilities_budget >= costs[self.set_piece_coach+1]:
                self.set_piece_coach += 1
                self.facilities_budget -= costs[self.set_piece_coach]
                self.save()

    def upgrade_physiotherapist(self):
        costs = {
            1: 10,
            2: 20,
            3: 30,
            4: 40,
            5: 50
        }

        if self.physiotherapist < 5:
            if self.facilities_budget >= costs[self.physiotherapist+1]:
                self.physiotherapist += 1
                self.facilities_budget -= costs[self.physiotherapist]
                self.save()

    def deposit_transfer_budget(self, amount):
        self.transfer_budget += amount
        self.save()

    def deposit_facilities_budget(self, amount):
        self.facilities_budget += amount
        self.save()

    def deposit_wage_budget(self, amount):
        self.wage_budget_total += amount
        self.wage_budget_remaining = self.wage_budget_total - self.wage_budget_spent
        self.save()

    def withdraw_transfer_budget(self, amount):
        self.transfer_budget -= amount
        self.save()

    def withdraw_facilities_budget(self, amount):
        self.facilities_budget -= amount
        self.save()

    def withdraw_wage_budget(self, amount):
        self.wage_budget_total -= amount
        self.wage_budget_remaining = self.wage_budget_total - self.wage_budget_spent
        self.save()

    def __str__(self):
        return self.name

class Feeder_Team(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, default='GFL Feeder Team')
    parent_club = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='parent_club')
    level = models.IntegerField(default=40)
    nation = models.CharField(max_length=64, default='England')
    team_type = models.CharField(max_length=64, default='youth')

    def __str__(self):
        return self.name

    def invest(self, amount):
        team = self.parent_club
        if team.facilities_budget >= amount and amount > 0:
            team.facilities_budget -= amount
            team.save()
            self.level += random.randint(0,amount)
            self.save()

class Player(models.Model):
    id = models.IntegerField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    feeder_team = models.ForeignKey(Feeder_Team, on_delete=models.CASCADE, related_name='feeder_players', blank=True, null=True)
    position = models.CharField(max_length=64)
    name = models.CharField(max_length=64, default='Player')
    age = models.IntegerField()
    sex = models.CharField(max_length=64, default='Male')
    overall = models.IntegerField()
    potential = models.IntegerField()
    nationality = models.CharField(max_length=64)
    tactic = models.CharField(max_length=64)
    wage = models.IntegerField()
    contract_length = models.IntegerField()
    skill_points = models.IntegerField(default=0)
    traits = models.CharField(max_length=1024, default='')
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    motm = models.IntegerField(default=0)
    loaned = models.CharField(max_length=5, default="N/A")
    loaned_to = models.CharField(max_length=64, default="N/A")
    loaned_wage = models.IntegerField(default=0)
    training = models.BooleanField(default=False)
    training_position = models.CharField(max_length=64, default="N/A")
    training_tactic = models.CharField(max_length=64, default="N/A")
    training_position_time = models.IntegerField(default=0)
    training_position_chance = models.IntegerField(default=0)
    training_tactic_time = models.IntegerField(default=0)
    training_tactic_chance = models.IntegerField(default=0)
    out_of_league_loan = models.BooleanField(default=False)
    free_agent = models.BooleanField(default=False)

    lineup_position = models.CharField(max_length=64, default="N/A")
    lineup_rating = models.IntegerField(default=0)

    duty = models.CharField(max_length=64, default='Support')
    dribbling = models.CharField(max_length=64, default='Balanced')
    shooting = models.CharField(max_length=64, default='Balanced')
    risk_taking = models.CharField(max_length=64, default='Balanced')
    tackling = models.CharField(max_length=64, default='Balanced')
    freedom = models.CharField(max_length=64, default='Balanced')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('player-detail', kwargs={'pk': self.pk})

    def sell_player(self, value):
        value = float(value)
        team = Team.objects.get(name=self.team)
        team.transfer_budget += value
        team.wage_budget_spent -= self.wage
        team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
        team.save()
        self.delete()

    def release_player(self):
        team = Team.objects.get(name=self.team)
        team.wage_budget_spent -= self.wage
        team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
        team.save()
        self.free_agent = True
        self.feeder_team = None
        self.loaned = 'N/A'
        self.loaned_to = 'N/A'
        self.loaned_wage = 0
        self.save()

    def return_loan(self):
        parent_club = self.team
        loaning_club = Team.objects.get(name=self.loaned_to)
        parent_club.wage_budget_spent += self.loaned_wage
        parent_club.wage_budget_remaining = parent_club.wage_budget_total - parent_club.wage_budget_spent
        parent_club.save()
        loaning_club.wage_budget_spent -= self.loaned_wage
        loaning_club.wage_budget_remaining = loaning_club.wage_budget_total - loaning_club.wage_budget_spent
        loaning_club.save()
        self.loaned = 'N/A'
        self.loaned_to = 'N/A'
        self.loaned_wage = 0
        self.save()

    def send_to_feeder_team(self, team):
        self.feeder_team = team
        self.save()

    def promote_to_senior_team(self):
        self.feeder_team = None
        self.save()

class Scouted_Player(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.CharField(max_length=64)
    position = models.CharField(max_length=3)
    name = models.CharField(max_length=64, default='Player')
    age = models.IntegerField()
    overall = models.IntegerField()
    potential = models.IntegerField()
    nationality = models.CharField(max_length=64)
    tactic = models.CharField(max_length=64)
    wage = models.IntegerField()
    contract_length = models.IntegerField()
    skill_points = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    motm = models.IntegerField(default=0)
    value = models.FloatField(default=0.0)
    can_be_loaned = models.BooleanField(default=False)
    loaned_wage = models.IntegerField(default=0)
    loaned = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def sign(self):
        team = Team.objects.get(name=self.team)
        if team.transfer_budget >= self.value and team.wage_budget_remaining >= self.wage:
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

            country = countries_dict[self.nationality]
            gender = 'm'

            url = f'https://www.behindthename.com/api/random.json?usage={country}&gender={gender}&randomsurname=yes&number=1&key=ja891397252'

            name_response = requests.get(url)
            time.sleep(1)
            name = ''

            if name_response.status_code == 200:
                name_json = name_response.json()
                name = name_json['names'][0] + " " + name_json['names'][1]
            else:
                name = 'Player'

            self.name = name

            player = Player(pk=self.id, team=team, position=self.position, name=self.name, age=self.age, overall=self.overall, potential=self.potential, nationality=self.nationality, tactic=self.tactic,
                            wage=self.wage, contract_length=self.contract_length, skill_points=self.skill_points, goals=self.goals, assists=self.assists, motm=self.motm)
            player.save()
            team.wage_budget_spent += player.wage
            team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
            team.transfer_budget -= self.value
            team.save()

            self.delete()

    def loan(self):
        team = Team.objects.get(name=self.team)
        if team.wage_budget_remaining >= self.loaned_wage:
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

            country = countries_dict[self.nationality]
            gender = 'm'

            url = f'https://www.behindthename.com/api/random.json?usage={country}&gender={gender}&randomsurname=yes&number=1&key=ja891397252'

            name_response = requests.get(url)
            time.sleep(1)
            name = ''

            if name_response.status_code == 200:
                name_json = name_response.json()
                name = name_json['names'][0] + " " + name_json['names'][1]
            else:
                name = 'Player'

            self.name = name

            player = Player(pk=self.id, team=team, position=self.position, name=self.name, age=self.age,
                            overall=self.overall, potential=self.potential, nationality=self.nationality,
                            tactic=self.tactic,
                            wage=self.loaned_wage, contract_length=1, skill_points=self.skill_points,
                            goals=self.goals, assists=self.assists, motm=self.motm, out_of_league_loan=True)
            player.save()
            team.wage_budget_spent += player.wage
            team.wage_budget_remaining = team.wage_budget_total - team.wage_budget_spent
            team.save()

            self.loaned = True
            self.save()

class offer(models.Model):
    id = models.AutoField(primary_key=True)
    team_from = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_from')
    team_to = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_to')
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_offered')
    amount = models.FloatField()
    accepted = models.CharField(max_length=10, default='Pending')
    type = models.CharField(max_length=10, default='Transfer')

    def remove(self):
        self.delete()

    def reject(self):
        self.accepted = 'Rejected'
        self.save()

    def accept(self):
        self.accepted = 'Accepted'
        player = self.player
        player.team = self.team_from
        player.save()
        team_to = self.team_to
        team_to.transfer_budget += self.amount
        team_to.wage_budget_spent -= player.wage
        team_to.wage_budget_remaining = team_to.wage_budget_total - team_to.wage_budget_spent
        team_to.save()
        team_from = self.team_from
        team_from.transfer_budget -= self.amount
        team_from.wage_budget_spent += player.wage
        team_from.wage_budget_remaining = team_from.wage_budget_total - team_from.wage_budget_spent
        team_from.save()

        self.save()

    def accept_loan(self):
        self.accepted = 'Accepted'
        player = self.player
        player.loaned = 'out'
        player.loaned_to = self.team_from.name
        player.loaned_wage = self.amount
        player.save()
        team_to = self.team_to
        team_to.wage_budget_spent -= player.loaned_wage
        team_to.wage_budget_remaining = team_to.wage_budget_total - team_to.wage_budget_spent
        team_to.save()
        team_from = self.team_from
        team_from.wage_budget_spent += player.loaned_wage
        team_from.wage_budget_remaining = team_from.wage_budget_total - team_from.wage_budget_spent
        team_from.save()

        self.save()

class notification(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_notification')
    message = models.CharField(max_length=10, default='')

    def remove(self):
        self.delete()

class lineup(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_lineup')
    overall = models.IntegerField(default=0)
    player_1 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_1', blank=True, null=True)
    player_2 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_2', blank=True, null=True)
    player_3 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_3', blank=True, null=True)
    player_4 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_4', blank=True, null=True)
    player_5 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_5', blank=True, null=True)
    player_6 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_6', blank=True, null=True)
    player_7 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_7', blank=True, null=True)
    player_8 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_8', blank=True, null=True)
    player_9 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_9', blank=True, null=True)
    player_10 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_10', blank=True, null=True)
    player_11 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_11', blank=True, null=True)
    player_12 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_12', blank=True, null=True)
    player_13 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_13', blank=True, null=True)
    player_14 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_14', blank=True, null=True)
    player_15 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_15', blank=True, null=True)
    player_16 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_16', blank=True, null=True)
    player_17 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_17', blank=True, null=True)
    player_18 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_18', blank=True, null=True)
    player_19 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_19', blank=True, null=True)
    player_20 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_20', blank=True, null=True)
    player_21 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_21', blank=True, null=True)
    player_22 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_22', blank=True, null=True)
    player_23 = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='player_23', blank=True, null=True)

    def __str__(self):
        return self.team.name + " lineup"

    def get_lineup(self):
        team_lineup = []

        team_lineup.append(self.player_1)
        team_lineup.append(self.player_2)
        team_lineup.append(self.player_3)
        team_lineup.append(self.player_4)
        team_lineup.append(self.player_5)
        team_lineup.append(self.player_6)
        team_lineup.append(self.player_7)
        team_lineup.append(self.player_8)
        team_lineup.append(self.player_9)
        team_lineup.append(self.player_10)
        team_lineup.append(self.player_11)
        team_lineup.append(self.player_12)
        team_lineup.append(self.player_13)
        team_lineup.append(self.player_14)
        team_lineup.append(self.player_15)
        team_lineup.append(self.player_16)
        team_lineup.append(self.player_17)
        team_lineup.append(self.player_18)
        team_lineup.append(self.player_19)
        team_lineup.append(self.player_20)
        team_lineup.append(self.player_21)
        team_lineup.append(self.player_22)
        team_lineup.append(self.player_23)

        return team_lineup