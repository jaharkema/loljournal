from django.contrib import admin
from .models import Summoner


class SummonerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Summoner, SummonerAdmin)
