from .Helper import *
from .List import *


class ListManager:
    def __init__(self):
        self.media_types = {}
        self.setMediaTypes()

    def setMediaTypes(self):
        self.media_types[MediaType.ANIME.value] = AnimeList()
        self.media_types[MediaType.MANGA.value] = MangaList()

    def getAllUserLists(self, user_name):
        user_lists = {}

        for media_type, service in self.media_types.items():
            list = service.getUserList(user_name)
            user_lists[media_type] = list
        return user_lists

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
            return -1


class WebsiteManager:
    def __init__(self):
        self.listManager = ListManager()

    def displayEntry(self, media_type, entry_id):
        response = self.listManager.getEntry(media_type, entry_id)
        return response["data"]["Media"]

    def displayUserList(self, media_type, username):
        return self.listManager.getUserList(media_type, username)

    def searchEntry(self, media_type, search_input, page_number):
        return self.listManager.searchEntry(media_type, search_input, page_number)

    def getAllUserLists(self, username):
        return self.listManager.getAllUserLists(username)
