import requests
import socket
import ssl
import json
from .Source import Source
from .Helper import MediaType


class List:
    def __init__(self, website):
        self.website = website


class MovieList(List):
    def __init__(self, api_key=None):
        _website = Source("OMDb", MediaType.MOVIE, "http://www.omdbapi.com/", "http://www.omdbapi.com/", api_key)
        super().__init__(_website)

    def getUserList(self, user_name):
        return {'return': "Not implemented yet"}

    def getEntry(self, entry_id):
        variables = {
            'apikey': self.website.api_key,
            'i': f"tt{ entry_id }"
        }
        response = requests.get(self.website.api_url, params=variables).json()
        return response

    def searchEntry(self, search_input, page_number, parameters):
        variables = {
            'apikey': self.website.api_key,
            's': search_input
        }
        response = requests.get(self.website.api_url, params=variables).json()
        return response


class ComicList(List):
    def __init__(self, api_key=None):
        _website = Source("ComicVine", MediaType.COMIC, "https://comicvine.gamespot.com", "https://api.comicvine.com", api_key)
        super().__init__(_website)

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented' }

    def getEntry(self, entry_id):
        variables = {
            'api_key': self.website.api_key,
            'format': 'json',
            'filter': f'id:{entry_id}'
        }
        headers = {
            'User-Agent': 'UltimateList/1.0 pls do not ban'
        }

        response = requests.get(f"{self.website.api_url}/volumes/", params=variables, headers=headers).json()
        return response['results'][0]

    def searchEntry(self, search_input, page_number, parameters):
        variables = {
            'api_key': self.website.api_key,
            'format': 'json',
            'query': search_input,
            'resources': 'volume',
            'page': page_number
        }
        headers = {
            'User-Agent': 'UltimateList/1.0 pls do not ban'
        }

        response = requests.get(f"{ self.website.api_url }/search/", params=variables, headers=headers).json()
        return response
