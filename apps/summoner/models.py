from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django.db import models


class Summoner(AbstractBaseUser, PermissionsMixin):
    BR = 'BR'
    EUNE = 'EUNE'
    EUW = 'EUW'
    JP = 'JP'
    KR = 'KR'
    LAN = 'LAN'
    LAS = 'LAS'
    NA = 'NA'
    OCE = 'OCE'
    RU = 'RU'
    TR = 'TR'

    REGION_CHOICES = (
        (BR, 'Brazil'),
        (EUNE, 'EU Nordic & East'),
        (EUW, 'EU West'),
        (JP, 'Japan'),
        (KR, 'Korea'),
        (LAN, 'Latin America North'),
        (LAS, 'Latin America South'),
        (NA, 'North America'),
        (OCE, 'Oceania'),
        (RU, 'Russia'),
        (TR, 'Turkey')
    )

    email = models.EmailField('email', unique=True)
    summoner_name = models.CharField('summoner name', max_length=32)
    region = models.CharField('region', max_length=4, choices=REGION_CHOICES)
    riot_id = models.CharField('Riot summoner ID', max_length=32, blank=True, null=True)

    is_staff = models.BooleanField('is staff', default=False)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        unique_together = (('summoner_name', 'region'), )

    def get_short_name(self):
        return self.summoner_name
