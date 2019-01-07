from .Helper import *
from .List import *
<<<<<<< HEAD
=======
import configparser
>>>>>>> master


class ListManager:
    def __init__(self):
        self.media_types = {}
        self.setMediaTypes()

    def setMediaTypes(self):
        self.media_types[MediaType.ANIME.value] = AnimeList()
        self.media_types[MediaType.MANGA.value] = MangaList()
<<<<<<< HEAD
=======
        self.media_types[MediaType.VISUAL_NOVEL.value] = VisualNovelList()
        #self.media_types[MediaType.MOVIE.value] = MovieList()
        #self.media_types[MediaType.BOOK.value] = BookList()
        #self.media_types[MediaType.MUSIC.value] = MusicList()
        #self.media_types[MediaType.TV_SHOW.value] = TVShowList()
        #self.media_types[MediaType.GAME.value] = GameList()

>>>>>>> master

    def getAllUserLists(self, user_name):
        user_lists = {}

        for media_type, service in self.media_types.items():
            list = service.getUserList(user_name)
            user_lists[media_type] = list
        return user_lists

<<<<<<< HEAD
    def getUserList(self, type, user_name):
        try:
            user_list = self.media_types[type].getUserList(user_name)
            return user_list
        except Exception as e:
            print(e)
            return -1

    def getEntry(self, type, entry_id):
        try:
            entry = self.media_types[type].getEntry(entry_id)
            return entry
        except Exception as e:
            print(e)
            return -1

    def searchEntry(self, type, search_input, page_number):
        try:
            search_result = self.media_types[type].searchEntry(search_input, page_number)
            return search_result
        except Exception as e:
            print(e)
=======
    def getUserList(self, media_type, user_name):
        try:
            user_list = self.media_types[media_type].getUserList(user_name)
            return user_list
        except Exception as e:
            print("getUserList: ", e)
            return -1

    def getEntry(self, media_type, entry_id):
        try:
            entry = self.media_types[media_type].getEntry(entry_id)
            return entry
        except Exception as e:
            print("getEntry: ", e)
            return -1

    def searchEntry(self, media_type, search_input, page_number, parameters):
        try:
            search_result = self.media_types[media_type].searchEntry(search_input, page_number, parameters)
            return search_result
        except Exception as e:
            print("searchEntry: ", e)
>>>>>>> master
            return -1


class WebsiteManager:
    def __init__(self):
        self.listManager = ListManager()
<<<<<<< HEAD

    def displayEntry(self, media_type, entry_id):
        response = self.listManager.getEntry(media_type, entry_id)
        return response["data"]["Media"]
=======
        self.loadConstants()

    def loadConstants(self):
        config = configparser.ConfigParser()
        config.read('constants.ini')
        for media_api, api_key in config["API KEYS"].items():
            for media_name, media in self.listManager.media_types.items():
                if media_name.lower() == media_api.lower():
                    media.website.query_url += api_key

    def displayEntry(self, media_type, entry_id):
        response = self.listManager.getEntry(media_type, entry_id)
        return response
>>>>>>> master

    def displayUserList(self, media_type, username):
        return self.listManager.getUserList(media_type, username)

<<<<<<< HEAD
    def searchEntry(self, media_type, search_input, page_number):
        return self.listManager.searchEntry(media_type, search_input, page_number)
=======
    def searchEntry(self, media_type, search_input, page_number, parameters):
        return self.listManager.searchEntry(media_type, search_input, page_number, parameters)
>>>>>>> master

    def getAllUserLists(self, username):
        return self.listManager.getAllUserLists(username)
