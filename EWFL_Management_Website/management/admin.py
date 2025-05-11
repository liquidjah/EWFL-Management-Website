from django.contrib import admin
from .models import Team, Player, Scouted_Player, Feeder_Team, lineup, offer

admin.site.register(Team)
admin.site.register(Player)
admin.site.register(Scouted_Player)
admin.site.register(Feeder_Team)
admin.site.register(offer)
admin.site.register(lineup)