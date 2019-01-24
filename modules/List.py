import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import ujson
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

    def responseToResult(self, response):
        _result = []
        for entry in response:
            _entry = {
                'title': entry["Title"],
                'cover': entry.get("Poster", 'https://u.nu/idkcover'),
                'url': entry.get("site_detail_url", '#'),
                'media_type': MediaType.MOVIE
            }
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = {
            'title': response.get("Title"),
            'description': response.get("Plot"),
            'cover': response.get("Poster", 'https://u.nu/idkcover'),
            'url': f'https://www.imdb.com/title/{ response.get("imdbID") }',
            'genres': response.get("Genre"),
            'rating': response.get("Metascore"),
            'runtime': response.get("Runtime"),
            'type': response.get("Type"),
            'released': response.get("Released")
        }
        return _entry

    def getUserList(self, user_name):
        return {'return': 'Not implemented yet', 'reason': 'API does not support this feature'}

    def getEntry(self, entry_id):
        variables = {
            'apikey': self.website.api_key,
            'r': self.output_format,
            'i': f'tt{ entry_id }',
            'plot': 'full'
        }
        response = requests.get(self.website.api_url, params=variables).json()
        return self.responseToEntry(response)

    def searchEntry(self, search_input, page_number, parameters):
        variables = {
            'apikey': self.website.api_key,
            'r': self.output_format,
            's': search_input,
            'page': page_number
        }
        response = requests.get(self.website.api_url, params=variables).json()
        return self.responseToResult(response['Search'])


class ComicList(List):
    def __init__(self, api_key=None):
        _website = Source("ComicVine", MediaType.COMIC, "https://comicvine.gamespot.com", "https://api.comicvine.com", api_key)
        super().__init__(_website)

    def responseToResult(self, response):
        _result = []
        for entry in response:
            _entry = {
                'title': entry["name"],
                'cover': entry.setdefault("image", {"thumb_url": "https://u.nu/idkcover"})["thumb_url"],
                'url': entry.get("site_detail_url", '#'),
                'media_type': MediaType.COMIC
            }
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        response = response[0]
        _entry = {
            'title': response['name'],
            'description': response.get("description"),
            'cover': response.setdefault("image", {"medium_url": "https://u.nu/idkcover"})["medium_url"],
            'url': response.get("site_detail_url", '#'),
            'count_of_issues': response.get("count_of_issues"),
            'start_year': response.get("start_year")
        }
        return _entry

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

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
        return self.responseToEntry(response['results'][0])

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
        return self.responseToResult(response['results'])
        

class GameList(List):
    def __init__(self, api_key=None):
        _website = Source("IGDB", MediaType.GAME, "https://igdb.com", "https://api-v3.igdb.com", api_key)
        super().__init__(_website)
        self.limit = 10

    def responseToResult(self, response):
        _result = []
        for entry in response:
            entry = entry["game"]
            _entry = {
                'title': entry["name"],
                'cover': entry.setdefault("cover", {"url": "https://u.nu/idkcover"})["url"],
                'url': entry.get("url", '#'),
                'media_type': MediaType.GAME
            }
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = {
            'title': response["name"],
            'description': response.get("summary"),
            'cover': response.setdefault("cover", {"url": "https://u.nu/idkcover"})["url"],
            'url': response.get("url", '#'),
            'collection': response.setdefault("collection", {"name": None, "url": None}),
            'genres': [genre["name"] for genre in response.get("genres", [])],
            'platforms': [platform["name"] for platform in response.get("platforms", [])],
            'themes': [theme["name"] for theme in response.get("themes", [])]
        }
        return _entry

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

    def getEntry(self, entry_id):
        url = f"{self.website.api_url}/games"
        data = f'''
                    fields name, summary, genres.name, collection.name, 
                    collection.url, platforms.name, platforms.category, 
                    themes.name, cover.url, url;
                    where id = { entry_id };
                '''
        header = {'user-key': self.website.api_key}
        response = requests.get(url, headers=header, data=data).json()
        return self.responseToEntry(response[0])

    def searchEntry(self, search_input, page_number, parameters):
        url = f"{ self.website.api_url }/search"
        page_number = self.limit * (page_number - 1)
        data = f'''
            fields game.name, game.summary, game.cover.url, game.url;
            search "{ search_input }";
            where game != null;
            offset { page_number };
            limit { self.limit };
        '''
        header = {'user-key': self.website.api_key}
        response = requests.get(url, headers=header, data=data).json()
        return self.responseToResult(response)


class BookList(List):
    def __init__(self, api_key=None):
        _website = Source("Goodreads", MediaType.BOOK, "https://www.goodreads.com", "https://www.goodreads.com", api_key)
        super().__init__(_website, 'xml')

    def responseToResult(self, response):
        response = response['GoodreadsResponse']['search']['results']['work']
        print(response)
        _result = {

        }
        return _result

    def responseToEntry(self, response):
        return {'return': 'Not yet implemented'}
    
    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

    def getEntry(self, entry_id):
        return { 'return': 'Not yet implemented' }
        response = ujson.loads(ujson.dumps(bf.data(fromstring(response))))

    def searchEntry(self, search_input, page_number, parameters):
        variables = {
            'key': self.website.api_key,
            'search[field]': 'title',
            'q': search_input,
            'page': page_number
        }
        response = requests.get(f"{self.website.api_url}/search/index.xml", params=variables).text
        response = ujson.loads(ujson.dumps(bf.data(fromstring(response))))
        return self.responseToResult(response)
        

class MusicList(List):
    def __init__(self, api_key=None):
        _website = Source("Spotify", MediaType.MUSIC, "https://spotify.com", "https://api.spotify.com", api_key)
        super().__init__(_website)

    def responseToResult(self, response):
        return {'return': 'Not yet implemented'}

    def responseToEntry(self, response):
        return {'return': 'Not yet implemented'}

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

    def getEntry(self, entry_id):
        return { 'return': 'Not yet implemented' }

    def searchEntry(self, search_input, page_number, parameters):
        return { 'return': 'Not yet implemented' }
