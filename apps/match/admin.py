from django.contrib import admin
from .models import Match


class MatchAdmin(admin.ModelAdmin):
    pass


admin.site.register(Match, MatchAdmin)
