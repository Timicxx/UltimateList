class AnimeList():
    def __init__(self, website, output_format='.json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10

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

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables})
        try:
            _response = response.json()
            return _response["data"]["MediaListCollection"]
        except Exception as e:
            print("getUserList: ", e)
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

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables})
        try:
            _response = response.json()
            return _response["data"]["Media"]
        except Exception as e:
            print("getEntry: ", e)
            return response.text

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
            'perPage': 10
        }

        response = requests.post(self.website.api_url, json={'query': query, 'variables': variables})
        try:
            _response = response.json()
            return _response["data"]["Page"]["media"]
        except Exception as e:
            print(e)
            return response.text()