import requests

from django.conf import settings

from .exceptions import APIError

# Dictionary to map methods to their API versions
method_versions = {
    'champion': '1.2',
    'championmastery': '',
    'current-game': '1.0',
    'featured-games': '1.0',
    'game': '1.3',
    'league': '2.5',
    'lol-static-data': '1.2',
    'lol-status': '1.0',
    'match': '2.2',
    'matchlist': '2.2',
    'stats': '1.3',
    'summoner': '1.4',
    'tournament': '1'
}


class RequestHandler(object):
    region = ''
    default_payload = {'api_key': settings.RIOT_API_KEY}

    def __init__(self, region):
        self.region = region

    def _build_url(self, method, endpoint):
        try:
            version = method_versions[method]
        except KeyError:
            raise Exception('No API version is defined for method {method}'.format(
                method=method,
            ))

        return '{base_url}/v{version}/{method}/{endpoint}'.format(
            base_url=self.base_url,
            version=version,
            method=method,
            endpoint=endpoint,
        )

    @property
    def base_url(self):
        return 'https://{region}.api.pvp.net/api/lol/{region}'.format(
            region=self.region.lower(),
        )

    def request(self, url, extra_payload={}):
        payload = self.default_payload
        payload.update(extra_payload)

        response = requests.get(url, params=payload)

        if not response.ok:
            raise APIError(response=response)

        return response


class StaticDataHandler(RequestHandler):
    @property
    def base_url(self):
        return 'https://global.api.pvp.net/api/lol/static-data/{region}'.format(
            region=self.region.lower(),
        )

    def _build_url(self, method, endpoint):
        version = method_versions['lol-static-data']

        return '{base_url}/v{version}/{method}/{endpoint}'.format(
            base_url=self.base_url,
            version=version,
            method=method,
            endpoint=endpoint,
        )


class SummonerInterface(RequestHandler):
    method = 'summoner'

    def get_by_name(self, name):
        endpoint = 'by-name/{name}'.format(name=name)

        url = self._build_url(self.method, endpoint)

        response = self.request(url)
        return response

    def get_by_id(self, summoner_id):
        endpoint = '{summoner_id}'.format(summoner_id=summoner_id)

        url = self._build_url(self.method, endpoint)

        response = self.request(url)
        return response


class GameInterface(RequestHandler):
    method = 'game'

    def get_recent_by_summoner_id(self, summoner_id):
        endpoint = 'by-summoner/{summoner_id}/recent'.format(
            summoner_id=summoner_id
        )

        url = self._build_url(self.method, endpoint)

        response = self.request(url)
        return response


class StaticChampionInterface(StaticDataHandler):
    method = 'champion'

    def get_by_id(self, champion_id):
        endpoint = '{0}'.format(champion_id)

        url = self._build_url(self.method, endpoint)

        response = self.request(url)
        return response
