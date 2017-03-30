from __future__ import unicode_literals

from datetime import datetime

from .request_handler import SummonerInterface, GameInterface, StaticChampionInterface


class APIObject(object):
    success = True

    def __init__(self, json):
        self.json_data = json
        self._initiate_object()

    def _initiate_object(self):
        """
        Use this function as follows:

        # 'games' can also be a summoner name or other identifier
        self.data = self.json['games']

        # set attributes. E.g. self.id = self.data.get('id')
        for key, value in self.data.iteritems():
            setattr(self, key, value)
        """
        raise NotImplementedError()


class RiotSummoner(APIObject):

    def _initiate_object(self):
        self.id = self.json_data.get('id')
        self.name = self.json_data.get('name')

    @classmethod
    def by_summoner_name(cls, name, region):
        interface = SummonerInterface(region)
        response = interface.get_by_name(name)
        json = response.json()

        return cls(json[name.lower()])

    @classmethod
    def by_riot_id(cls, riot_id, region):
        interface = SummonerInterface(region)
        response = interface.get_by_id(riot_id)
        json = response.json()

        return cls(json[riot_id])


class RiotGame(APIObject):

    def _initiate_object(self):
        stats = self.json_data.get('stats')
        epoch_seconds = self.json_data.get('createDate') / 1000.0

        self.id = self.json_data.get('gameId')
        self.champion_id = self.json_data.get('championId')
        self.created = datetime.fromtimestamp(epoch_seconds)
        self.game_type = self.json_data.get('subType')

        self.win = stats.get('win')
        self.kills = stats.get('championsKilled', 0)
        self.deaths = stats.get('numDeaths', 0)
        self.assists = stats.get('assists', 0)
        self.minions_killed = stats.get('minionsKilled', 0)

    @classmethod
    def recent_for_summoner(cls, summoner_id, region):
        # Returns a list of recent games for this summoner id

        interface = GameInterface(region)
        response = interface.get_recent_by_summoner_id(summoner_id)
        json = response.json()
        games = []

        for game in json['games']:
            games.append(cls(game))

        return games


class RiotChampion(APIObject):

    def _initiate_object(self):
        self.id = self.json_data.get('id')
        self.name = self.json_data.get('key')

    @classmethod
    def by_id(cls, champion_id, region):
        interface = StaticChampionInterface(region)
        response = interface.get_by_id(champion_id)
        json = response.json()

        return cls(json)
