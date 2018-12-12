from Classes.Helper import *
from Classes.Manager import ListManager, DatabaseManager

def main():
    list_manager = ListManager()
    user_lists = list_manager.getAllUserLists("Tymec")
    user_list = list_manager.getUserList(MediaType.ANIME, "Tymec")
    dataToJson(user_lists, "Debug/user_lists.json")
    dataToJson(user_list, "Debug/user_list.json")

if __name__ is __name__:
    db = DatabaseManager()
    #main()
