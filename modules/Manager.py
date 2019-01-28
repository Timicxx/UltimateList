from .Helper import *
from .List import *
import configparser


class ListManager:
    def __init__(self):
        self.media_types = {}
        self.setMediaTypes()
        self.loadAPIKeys()

    def loadAPIKeys(self):
        config = configparser.ConfigParser()
        config.read('constants.ini')
        for media, api_key in config["API KEYS"].items():
            for media_name, media_class in self.media_types.items():
                if media_name.lower() == media.lower():
                    media_class.website.api_key = api_key

    def setMediaTypes(self):
        self.media_types[MediaType.MOVIE.value] = MovieList()
        self.media_types[MediaType.COMIC.value] = ComicList()
        self.media_types[MediaType.GAME.value] = GameList()
        self.media_types[MediaType.BOOK.value] = BookList()
        #self.media_types[MediaType.MUSIC.value] = MusicList()

    def getAllUserLists(self, user_name):
        user_lists = {}

        for media_type, service in self.media_types.items():
            list = service.getUserList(user_name)
            user_lists[media_type] = list
        return user_lists

    def getUserList(self, media_type, user_name):
        try:
            if media_type in list(self.media_types.keys()):
                user_list = self.media_types[media_type].getUserList(user_name)
            else:
                return self.getAllUserLists(user_name)
            return user_list
        except Exception as e:
            print("getUserList: ", e)
            return { 'return': 'Exception occured at: getUserList in class: ListManager' }

    def getEntry(self, media_type, entry_id, parameters):
        try:
            if media_type in list(self.media_types.keys()):
                entry = self.media_types[media_type].getEntry(entry_id)
                return entry
            return -1
        except Exception as e:
            print("getEntry: ", e)
            return {'return': 'Exception occured at: getEntry in class: ListManager'}

    def searchEntry(self, media_type, search_input, page_number, parameters):
        search_result = {}
        try:
            if media_type in list(self.media_types.keys()):
                search_result = self.media_types[media_type].searchEntry(search_input, page_number, parameters)
                search_result = {media_type: search_result}
                return search_result
            for media_name, media in self.media_types.items():
                _search_result = media.searchEntry(search_input, page_number, parameters)
                search_result[media_name] = _search_result
            return search_result
        except Exception as e:
            print("searchEntry: ", e)
            return {'return': 'Exception occured at: searchEntry in class: ListManager'}


class WebsiteManager:
    def __init__(self):
        self.listManager = ListManager()

    def displayEntry(self, media_type, entry_id, parameters):
        media_type = media_type.capitalize()

        return self.listManager.getEntry(media_type, entry_id, parameters)

    def displayUserList(self, parameters, username):
        media_type = parameters.get('media', '*').capitalize()

        return self.listManager.getUserList(media_type, username)

    def searchEntry(self, parameters):
        media_type = parameters.get('media', '*').capitalize()
        search_input = parameters.get('q')
        page_number = int(parameters.get('page', 1))

        return self.listManager.searchEntry(media_type, search_input, page_number, parameters)
