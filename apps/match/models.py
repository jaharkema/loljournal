from __future__ import unicode_literals

from django.db import models
from apps.api.models import RiotChampion


class Match(models.Model):

    riot_id = models.CharField('Riot match ID', max_length=50)
    summoner = models.ForeignKey('summoner.Summoner', related_name='matches')
    notes = models.TextField(help_text='Add notes for this match. What went well? How can you improve?', null=True)

    # API Fields
    win = models.BooleanField('win', default=False)
    champion_id = models.IntegerField('champion id', null=True)
    champion_name = models.CharField('champion name', null=True, max_length=50)
    created = models.DateTimeField('created', null=True)
    kills = models.IntegerField('kills', default=0)
    deaths = models.IntegerField('deaths', default=0)
    assists = models.IntegerField('assists', default=0)
    minions = models.IntegerField('cs', default=0)
    game_type = models.CharField('game type', max_length=50, null=True)

    class Meta:
        verbose_name = "Match"
        verbose_name_plural = "Matches"
        ordering = ['-created']

    def __str__(self):
        return self.riot_id

    def champion(self):
        if hasattr(self, '_champion'):
            return self._champion

        # PLEASE NOTE: This adds to the API request rate limit
        self._champion = RiotChampion.by_id(self.champion_id)
