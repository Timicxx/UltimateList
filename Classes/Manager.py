import mysql.connector

from .Helper import *
from .List import *

class Manager:
    def __init__(self):
        pass

class ListManager(Manager):
    def __init__(self):
        self.media_types = {}
        self.set_media_types()

    def set_media_types(self):
        self.media_types[MediaType.ANIME] = AnimeList()
        self.media_types[MediaType.MANGA] = MangaList()

    def getAllUserLists(self, user_name):
        user_lists = {}

        for media_type, service in self.media_types.items():
            list = service.getUserList(user_name)
            user_lists[media_type.value] = list

        return user_lists

    def getUserList(self, type, user_name):
        try:
            self.media_types[type]
        except:
            return -1
        user_list = self.media_types[type].getUserList(user_name)
        return user_list


class DatabaseManager(Manager):
    def __init__(self):
        self.db = mysql.connector.connect(host="localhost", user="ultimate", passwd="TimboBimbo!23")
        self.cursor = self.db.cursor()

    def insert_entry(self, entry):
        cmd = "INSERT INTO entries (title, media_type, entry_origin_id, entry_origin_website) VALUES (%s, %s, %i, %s)"
        val = (entry.title, entry.type.value, entry.source_id, entry.source)
