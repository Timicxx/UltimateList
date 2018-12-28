from modules.Helper import *
from modules.Manager import *
from modules.Entry import *


def main():
    debug()
    while True:
        pass


def debug():
    list_manager = ListManager()
    anime_user_list = list_manager.getUserList(MediaType.ANIME.value, "Tymec")
    anime_entry = list_manager.getEntry(MediaType.ANIME.value, 74)
    anime_search_result = list_manager.searchEntry(MediaType.ANIME.value, "Akira", 1)

    manga_user_list = list_manager.getUserList(MediaType.MANGA.value, "Tymec")
    manga_entry = list_manager.getEntry(MediaType.MANGA.value, 101475)
    manga_search_result = list_manager.searchEntry(MediaType.MANGA.value, "Neverland", 1)

    dataToJson(anime_user_list, "debug/anime_user_list.json")
    dataToJson(anime_entry, "debug/anime_entry.json")
    dataToJson(anime_search_result, "debug/anime_search_result.json")

    dataToJson(manga_user_list, "debug/manga_user_list.json")
    dataToJson(manga_entry, "debug/manga_entry.json")
    dataToJson(manga_search_result, "debug/manga_search_result.json")


if __name__ is __name__:
    main()
