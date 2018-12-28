import requests
import socket
import ssl
import json
from .Source import Source
from .Helper import MediaType


class List:
    def __init__(self, website):
        self.website = website


class AnimeList(List):
    def __init__(self):
        _website = Source("AniList", MediaType.ANIME, "https://anilist.co/", "https://graphql.anilist.co")
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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
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

        response = requests.post(self.website.query_url, json={'query': query, 'variables': variables})
        try:
            _response = response.json()
            return _response["data"]["Page"]["media"]
        except Exception as e:
            print("searchEntry: ", e)
            return response.text


class MangaList(List):
    def __init__(self):
        _website = Source("AniList", MediaType.MANGA, "https://anilist.co/", "https://graphql.anilist.co")
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
            _response = response.json()
            return _response["data"]["MediaListCollection"]
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
            _response = response.json()
            return _response["data"]["Media"]
        except Exception as e:
            print(e)
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
            _response = response.json()
            return _response["data"]["Page"]["media"]
        except Exception as e:
            print(e)
            return response.text


class MovieList(List):
    def __init__(self):
        _website = Source("OMDb", MediaType.MOVIE, "http://www.omdbapi.com/", "http://www.omdbapi.com/?apikey=")
        super().__init__(_website)

    def getUserList(self, user_name):
        pass

    def getEntry(self, entry_id):
        pass

    def searchEntry(self, search_input, page_number, parameters):
        pass


class VisualNovelList(List):
    def __init__(self):
        _website = Source("vndb", MediaType.VISUAL_NOVEL, "https://vndb.org/", "api.vndb.org:19535")
        super().__init__(_website)
        self.ip = self.website.query_url.split(':')[0]
        self.port = int(self.website.query_url.split(':')[1])
        self.logged_in = False
        self.clientvars = {'protocol': 1, 'clientver': 0.1, 'client': 'UltimatList'}
        self.data_buffer = bytes(1024)
        self.sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
        self.sslcontext.verify_mode = ssl.CERT_REQUIRED
        self.sslcontext.check_hostname = True
        self.sslcontext.load_default_certs()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sslwrap = self.sslcontext.wrap_socket(self.socket, server_hostname=self.ip)
        self.sslwrap.connect((self.ip, self.port))
        self._login()

    def getUserList(self, user_name):
        pass

    def getEntry(self, entry_id):
        response = self._send_command('get', "vn basic,details (id=%d)" % entry_id)
        return response

    def searchEntry(self, search_input, page_number, parameters):
        response = self._send_command('get', "vn basic,details (title~\"%s\") {\"page\": %d}" % (search_input, page_number))
        return response

    def _send_command(self, command, args=None):
        if args:
            final_command = command + ' ' + args + '\x04'
        else:
            final_command = command + '\x04'
        self.sslwrap.sendall(final_command.encode('utf-8'))

        return self._recv_data()

    def _recv_data(self):
        temp = ""
        while True:
            self.data_buffer = self.sslwrap.recv(1024)

            if '\x04' in self.data_buffer.decode('utf-8', 'ignore'):
                temp += self.data_buffer.decode('utf-8', 'ignore')
                temp.replace("\\", '')
                break
            else:
                temp += self.data_buffer.decode('utf-8', 'ignore')
                self.data_buffer = bytes(1024)
        temp = temp.replace('\x04', '')
        if 'ok' in temp and not self.logged_in:
            self.logged_in = True
            return temp
        else:
            return json.loads(str(temp.split(' ', 1)[1]))

    def _login(self):
        self._send_command('login', json.dumps(self.clientvars))
