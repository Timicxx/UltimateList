from .Helper import *
from .List import *
import configparser


class ListManager:
    def __init__(self):
        self.media_types = {}
        self.setMediaTypes()
        self.loadConstants()

    def loadConstants(self):
        config = configparser.ConfigParser()
        config.read('constants.ini')
        for media, api_key in config["API KEYS"].items():
            for media_name, media_class in self.media_types.items():
                if media_name.lower() == media.lower():
                    media_class.website.api_key = api_key

    def setMediaTypes(self):
        self.media_types[MediaType.ANIME.value] = AnimeList()
        self.media_types[MediaType.MANGA.value] = MangaList()
        self.media_types[MediaType.VISUAL_NOVEL.value] = VisualNovelList()
        self.media_types[MediaType.MOVIE.value] = MovieList()
        self.media_types[MediaType.COMIC.value] = ComicList()
        #self.media_types[MediaType.BOOK.value] = BookList()
        #self.media_types[MediaType.MUSIC.value] = MusicList()
        #self.media_types[MediaType.GAME.value] = GameList()


    def getAllUserLists(self, user_name):
        user_lists = {}

        for media_type, service in self.media_types.items():
            list = service.getUserList(user_name)
            user_lists[media_type] = list
        return user_lists

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
            return -1


class WebsiteManager:
    def __init__(self):
        self.listManager = ListManager()

    def displayEntry(self, media_type, entry_id):
        response = self.listManager.getEntry(media_type, entry_id)
        return response

    def displayUserList(self, media_type, username):
        return self.listManager.getUserList(media_type, username)

    def searchEntry(self, media_type, search_input, page_number, parameters):
        return self.listManager.searchEntry(media_type, search_input, page_number, parameters)

    def getAllUserLists(self, username):
        return self.listManager.getAllUserLists(username)
