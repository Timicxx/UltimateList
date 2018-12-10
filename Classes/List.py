import requests
import json

from .Website import Website
from .Helper import MediaType


class List():
    def __init__(self, website):
        self.website = website


class AnimeList(List):
    def __init__(self):
        _website = Website("AniList", MediaType.ANIME, "https://anilist.co", "https://graphql.anilist.co")
        super().__init__(_website)
    
    def getUserList(userName):
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
            'name': userName
        }

        response = requests.post(self.website.url, json={'query': query, 'variables': variables})
        
        # Dump response for debugging purpose
        # with open("Debug//out.json", 'w') as f:
        #     json.dump(response.json(), f, indent=4)
        
        return response.json()