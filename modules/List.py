import requests
import socket
import ssl
import json
from .Source import Source
from .Helper import MediaType


class List:
    def __init__(self, website, output_format='json'):
        self.website = website
        self.output_format = output_format


class MovieList(List):
    def __init__(self, api_key=None):
        _website = Source("OMDb", MediaType.MOVIE, "http://www.omdbapi.com/", "http://www.omdbapi.com/", api_key)
        super().__init__(_website)

    def responseToEntry(self, response):
        pass

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
            's': search_input,
            'page': page_number
        }
        response = requests.get(self.website.api_url, params=variables).json()
        return response


class ComicList(List):
    def __init__(self, api_key=None):
        _website = Source("ComicVine", MediaType.COMIC, "https://comicvine.gamespot.com", "https://api.comicvine.com", api_key)
        super().__init__(_website)

    def responseToEntry(self, response):
        pass

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented' }

    def getEntry(self, entry_id):
        variables = {
            'api_key': self.website.api_key,
            'format': self.output_format,
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
            'format': self.output_format,
            'query': search_input,
            'resources': 'volume',
            'page': page_number
        }
        headers = {
            'User-Agent': 'UltimateList/1.0 pls do not ban'
        }

        response = requests.get(f"{ self.website.api_url }/search/", params=variables, headers=headers).json()
        return response
        

class GameList(List):
    def __init__(self, api_key=None):
        _website = Source("IGDB", MediaType.GAME, "https://igdb.com", "https://api-v3.igdb.com", api_key)
        super().__init__(_website)
        self.limit = 10
    
    def transformResponse(self, response):
        _new_response = []
        for entry in response:
            entry = entry["game"]
            _new_entry = {
                'title': entry["name"],
                'description': entry.get("summary"),
                'cover': entry.setdefault("cover", {"url": ""})["url"],
                'url': entry["url"]
            }
            _new_response.append(_new_entry)
        return _new_response
    
    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented' }

    def getEntry(self, entry_id):
        url = f"{self.website.api_url}/games"
        data = f'''
                    fields name, summary, genres.name, cover.url, url;
                    where id = { entry_id };
                '''
        header = {'user-key': self.website.api_key}
        response = requests.get(url, headers=header, data=data).json()
        return self.transformResponse(response)

    def searchEntry(self, search_input, page_number, parameters):
        url = f"{ self.website.api_url }/search"
        page_number = self.limit * (page_number - 1)
        data = f'''
            fields game.name, game.summary, game.cover.url, game.genres.name, game.url;
            search "{ search_input }";
            where game != null;
            offset { page_number };
            limit { self.limit };
        '''
        header = {'user-key': self.website.api_key}
        response = requests.get(url, headers=header, data=data).json()
        return self.transformResponse(response)


class BookList(List):
    def __init__(self, api_key=None):
        _website = Source("Goodreads", MediaType.BOOK, "https://www.goodreads.com", "https://www.goodreads.com", api_key)
        super().__init__(_website, 'xml')
    
    def responseToEntry(self, response):
        return {'return': 'Not yet implemented'}
    
    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented' }

    def getEntry(self, entry_id):
        return { 'return': 'Not yet implemented' }

    def searchEntry(self, search_input, page_number, parameters):
        return { 'return': 'Not yet implemented' }
        

class MusicList(List):
    def __init__(self, api_key=None):
        _website = Source("Spotify", MediaType.MUSIC, "https://spotify.com", "https://api.spotify.com", api_key)
        super().__init__(_website)

    def responseToEntry(self, response):
        return {'return': 'Not yet implemented'}

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented' }

    def getEntry(self, entry_id):
        return { 'return': 'Not yet implemented' }

    def searchEntry(self, search_input, page_number, parameters):
        return { 'return': 'Not yet implemented' }
