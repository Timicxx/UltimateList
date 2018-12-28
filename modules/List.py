import requests
from .Source import Source
from .Helper import MediaType


class List:
    def __init__(self, website):
        self.website = website


class AnimeList(List):
    def __init__(self):
        _website = Source("AniList", MediaType.ANIME, "https://anilist.co", "https://graphql.anilist.co")
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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text

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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text

    def searchEntry(self, search_input, page_number):
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
            'perPage': 10
        }

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text


class MangaList(List):
    def __init__(self):
        _website = Source("AniList", MediaType.MANGA, "https://anilist.co", "https://graphql.anilist.co")
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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})

        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text

    def getEntry(self, entry_id):
        query = '''
            query ($id: Int) {
                Media (id: $id, type: MANGA) {
                    id
                    title {
                        romaji
                    }
                    description
                    chapters
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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text

    def searchEntry(self, search_input, page_number):
        query = '''
            query ($id: Int, $page: Int, $perPage: Int, $search: String) {
                Page (page: $page, perPage: $perPage) {
                    pageInfo {
                        total
                        currentPage
                        perPage
                    }
                    media (id: $id, type: MANGA, search: $search) {
                        id
                        title {
                            romaji
                        }
                        description
                        chapters
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
            'perPage': 10
        }

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            return response.json()
        except Exception as e:
            print(e)
            return response.text
