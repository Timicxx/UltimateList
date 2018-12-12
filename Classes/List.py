import requests
import json

from .Website import Website
from .Helper import MediaType


class List:
    def __init__(self, website):
        self.website = website

class GloblaList(List):
    def __init__(self):
        self.global_list = {}

class AnimeList(List):
    def __init__(self):
        _website = Website("AniList", MediaType.ANIME, "https://anilist.co", "https://graphql.anilist.co")
        super().__init__(_website)

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
                                }
                                episodes
                                coverImage {
                                    large
                                }
                                isFavourite
                                isAdult
                                genres
                                tags {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        '''

        variables = {
            'name': user_name
        }

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except:
            return response.text

class MangaList(List):
    def __init__(self):
        _website = Website("AniList", MediaType.MANGA, "https://anilist.co", "https://graphql.anilist.co")
        super().__init__(_website)

    def getUserList(self, user_name):
        query = '''
            query ($name: String) {
                MediaListCollection (userName: $name, type: MANGA) {
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
                                }
                                chapters
                                coverImage {
                                    large
                                }
                                isFavourite
                                isAdult
                                genres
                                tags {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        '''

        variables = {
            'name': user_name
        }

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})

        try:
            return response.json()
        except:
            return response.text
