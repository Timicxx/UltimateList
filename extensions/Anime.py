import requests
import re
from modules.Entry import *
from extensions.ExtensionEntry import *


class AnimeList:
    def __init__(self, website, output_format='.json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10

    def responseToResult(self, response):
        _result = []
        for entry in response:
            _entry = SearchResult(
                entry["title"]["romaji"],
                entry["coverImage"]["large"],
                entry["id"],
                "Anime"
            )
            _result.append(_entry)
        return _result

    def responseToEntry(self, response):
        _entry = Anime(
            response["title"]["romaji"],
            re.sub('<.*?>', '', response["description"]) if response["description"] is not None else "No data",
            response["siteUrl"],
            response["id"],
            response["coverImage"]["large"],
            response["episodes"],
            ', '.join(response["genres"]),
            ', '.join([tag['name'] for tag in response["tags"]])
        )
        return _entry

    def getUserList(self, user_name):
        query = '''
            query ($name: String) {
                MediaListCollection (userName: $name, type: ANIME) {
                    lists {
                        name
                        status
                        entries {
                            progress
                            score
                            media {
                                id
                                title {
                                    romaji
                                    english
                                    native
                                }
                                episodes
                                format
                                status
                                coverImage {
                                    large
                                }
                                isAdult
                                genres
                                tags {
                                    name
                                }
                                siteUrl
                            }
                        }
                    }
                }
            }
        '''

        variables = {
            'name': user_name
        }

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables}).json()

        return response["data"]["MediaListCollection"]['lists']

    def getEntry(self, entry_id):
        query = '''
            query ($id: Int) {
                Media (id: $id, type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    episodes
                    format
                    status
                    coverImage {
                        large
                    }
                    isAdult
                    genres
                    tags {
                        name
                    }
                    siteUrl
                }
            }
        '''

        variables = {
            'id': entry_id
        }

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables}).json()

        return self.responseToEntry(response["data"]["Media"])

    def searchEntry(self, search_input, page_number, parameters):
        query = '''
            query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        currentPage
                        perPage
                    }
                    media (id: $id, type: ANIME, search: $search) {
                        id
                        title {
                            romaji
                            english
                            native
                        }
                        description
                        episodes
                        format
                        status
                        coverImage {
                            large
                        }
                        isAdult
                        genres
                        tags {
                            name
                        }
                        siteUrl
                    }
                }
            }
        '''

        variables = {
            'search': search_input,
            'page': page_number,
            'perPage': self.limit
        }

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables}).json()

        return self.responseToResult(response["data"]["Page"]["media"])
