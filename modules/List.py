import requests
from xmljson import badgerfish as bf
from xml.etree.ElementTree import fromstring
import ujson
from .Source import Source
from .Entry import *


class List:
    def __init__(self, website, output_format='json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10


class MovieList(List):
    def __init__(self, api_key=None):
        _website = Source("OMDb", "Movie", "http://www.omdbapi.com/", "http://www.omdbapi.com/", api_key)
        super().__init__(_website)

    def responseToResult(self, response):
        _result = []
        for entry in response:
            _entry = SearchResult(
                entry["Title"],
                entry["Poster"] if entry["Poster"] != "N/A" else "https://u.nu/idkcover",
                entry.get("imdbID").replace('tt', ''),
                "Movie"
            )
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = Movie(
            response.get("Title"),
            response.get("Plot"),
            f'https://www.imdb.com/title/{ response.get("imdbID") }',
            response.get("imdbID").replace('tt', ''),
            response.get("Poster", 'https://u.nu/idkcover'),
            response.get("Genre"),
            response.get("Metascore"),
            response.get("Runtime"),
            response.get("Type"),
            response.get("Released")
        )
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
        if len(search_input) < 3:
            return {'return': 'Search query too short', 'reason': 'Search query has to be longer than 3 characters'}
        variables = {
            'apikey': self.website.api_key,
            'r': self.output_format,
            's': search_input,
            'page': page_number
        }
        response = requests.get(self.website.api_url, params=variables).json()
        if response['Response'] == 'False':
            return []
        return self.responseToResult(response['Search'])


class ComicList(List):
    def __init__(self, api_key=None):
        _website = Source("ComicVine", "Comic", "https://comicvine.gamespot.com", "https://api.comicvine.com", api_key)
        super().__init__(_website)

    def responseToResult(self, response):
        _result = []
        for entry in response:
            _entry = SearchResult(
                entry["name"],
                entry.setdefault("image", {"thumb_url": "https://u.nu/idkcover"})["thumb_url"],
                entry.get("id"),
                "Comic"
            )
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = Comic(
            response['name'],
            response.get("description"),
            response.get("site_detail_url", '#'),
            response.get("id"),
            response.setdefault("image", {"medium_url": "https://u.nu/idkcover"})["medium_url"],
            response.get("count_of_issues"),
            response.get("start_year")
        )
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
            'page': page_number,
            'limit': self.limit
        }
        headers = {
            'User-Agent': 'UltimateList/1.0 pls do not ban'
        }

        response = requests.get(f"{ self.website.api_url }/search/", params=variables, headers=headers).json()
        return self.responseToResult(response['results'])
        

class GameList(List):
    def __init__(self, api_key=None):
        _website = Source("IGDB", "Game", "https://igdb.com", "https://api-v3.igdb.com", api_key)
        super().__init__(_website)

    def responseToResult(self, response):
        _result = []
        for entry in response:
            entry = entry["game"]
            _entry = SearchResult(
                entry["name"],
                entry.setdefault("cover", {"url": "https://u.nu/idkcover"})["url"],
                entry.get("id"),
                "Game"
            )
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = Game(
            response["name"],
            response.get("summary"),
            response.get("url", '#'),
            response.get("id"),
            response.setdefault("cover", {"url": "https://u.nu/idkcover"})["url"],
            response.setdefault("collection", {"name": None, "url": None}),
            [genre["name"] for genre in response.get("genres", [])],
            [platform["name"] for platform in response.get("platforms", [])],
            [theme["name"] for theme in response.get("themes", [])]
        )
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
        _website = Source("Goodreads", "Book", "https://www.goodreads.com", "https://www.goodreads.com", api_key)
        super().__init__(_website, 'xml')

    def responseToResult(self, response):
        _result = []
        for entry in response:
            entry = entry["best_book"]
            _entry = SearchResult(
                entry["title"]["$"],
                entry["image_url"]["$"],
                entry['id']['$'],
                "Book"
            )
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = Book(
            response['title']['$'],
            response['description']['$'],
            response['url']['$'],
            response['id']['$'],
            response['image_url']['$'],
            response['publication_year']['$'],
            response['num_pages']['$'],
            response['authors']['author'][0]['name']['$']
        )
        return _entry
    
    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

    def getEntry(self, entry_id):
        variables = {
            'key': self.website.api_key,
            'id': entry_id,
            'format': self.output_format
        }
        response = requests.get(f"{self.website.api_url}/book/show", params=variables).text
        response = ujson.loads(ujson.dumps(bf.data(fromstring(response))))
        response = response['GoodreadsResponse']['book']
        return self.responseToEntry(response)

    def searchEntry(self, search_input, page_number, parameters):
        variables = {
            'key': self.website.api_key,
            'search[field]': 'title',
            'q': search_input,
            'page': page_number
        }
        response = requests.get(f"{self.website.api_url}/search/index.xml", params=variables).text
        response = ujson.loads(ujson.dumps(bf.data(fromstring(response))))
        response = response['GoodreadsResponse']['search']['results']['work']
        return self.responseToResult(response)
        
