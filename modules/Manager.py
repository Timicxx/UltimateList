from .List import *
import configparser
import glob
import os
import sys
import json


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
        self.media_types["Movie"] = MovieList()
        self.media_types["Comic"] = ComicList()
        self.media_types["Game"] = GameList()
        self.media_types["Book"] = BookList()
        #self.media_types["Music] = MusicList()

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
        self.extensionManager = ExtensionManager(self.listManager)
        self.admin_list = ['Tymec']

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


class ExtensionManager:
    def __init__(self, list_manager, extension_folder="extensions"):
        self.listManager = list_manager
        self.extensions = {
            'Enabled': {},
            'Disabled': {}
        }
        self.loadExtensions(extension_folder)

    def loadExtensions(self, extension_folder):
        sys.path.insert(0, extension_folder)
        for extension in glob.glob(f"{ extension_folder }\\*.json"):
            filename = os.path.splitext(extension)[0].split('\\')[-1]

            with open(extension, 'rb') as f:
                _info = json.load(f)

            module = __import__(filename)
            self.extensions['Disabled'][_info['Name']] = getattr(module, f"{_info['Name'].replace(' ', '')}List")

    def enableExtension(self, extension):
        if extension not in self.extensions['Disabled']:
            return -1
        self.listManager.media_types[extension] = self.extensions['Disabled'][extension]
        self.extensions['Enabled'][extension] = self.extensions['Disabled'][extension]
        del self.extensions['Disabled'][extension]

    def disableExtension(self, extension):
        if extension not in self.extensions['Enabled']:
            return -1
        del self.listManager.media_types[extension]
        self.extensions['Enabled'][extension] = self.extensions['Disabled'][extension]
        del self.extensions['Enabled'][extension]
