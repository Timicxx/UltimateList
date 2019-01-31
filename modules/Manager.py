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


class ExtensionManager:
    def __init__(self, extension_folder="extensions"):
        self.extensions = {
            'Enabled': {},
            'Disabled': {}
        }
        self.loadExtensions(extension_folder)

    def loadExtensions(self, extension_folder):
        sys.path.insert(0, extension_folder)
        for extension in glob.glob(f"{ extension_folder }\\*.json"):
            _filename = os.path.splitext(extension)[0].split('\\')[-1]

            with open(extension, 'rb') as f:
                _info = json.load(f)

            module = __import__(_filename)
            extension_class = getattr(module, f"{_info['Name'].replace(' ', '')}List")

            _website = Source(
                _info['Name'],
                _info['Name'],
                _info['URL'],
                _info['API URL'],
                _info['API Key']
            )

            self.extensions['Disabled'][_info['Name']] = extension_class(_website)

    def disableExtensions(self, media_list):
        _new_media_list = media_list
        for media in _new_media_list:
            if media in self.extensions['Disabled']:
                del _new_media_list[media]
        return _new_media_list

    def enableExtensions(self, media_list):
        _new_media_list = media_list
        for extension in self.extensions['Enabled']:
            _new_media_list[extension] = self.extensions['Enabled'][extension]
        return _new_media_list

    def toggleExtensions(self, media_list, extensions_to_toggle):
        self.extensions['Disabled'] = {
            **self.extensions['Enabled'],
            **self.extensions['Disabled']
        }
        self.extensions['Enabled'] = {}
        for extension in extensions_to_toggle:
            if extension in self.extensions['Disabled']:
                self.extensions['Enabled'][extension] = self.extensions['Disabled'][extension]
                del self.extensions['Disabled'][extension]
        _new_media_list = self.disableExtensions(media_list)
        _new_media_list = self.enableExtensions(media_list)
        return _new_media_list


class WebsiteManager:
    def __init__(self):
        self.listManager = ListManager()
        self.extensionManager = ExtensionManager()
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

    def toggleExtensions(self, extensions_to_toggle):
        self.listManager.media_types = self.extensionManager.toggleExtensions(self.listManager.media_types, extensions_to_toggle)
        print(self.extensionManager.extensions)
        print(self.listManager.media_types)
