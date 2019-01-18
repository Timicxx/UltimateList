import json
from enum import Enum


class MediaType(Enum):
    ANIME = "Anime"                 # IMPLEMENTED
    MANGA = "Manga"                 # IMPLEMENTED
    VISUAL_NOVEL = "Visual Novel"   # IMPLEMENTED
    MOVIE = "Movie"                 # PARTIALLY IMPLEMENTED
    COMIC = "Comic"                 # PARTIALLY IMPLEMENTED
    BOOK = "Book"                   # NOT YET IMPLEMENTED
    GAME = "Game"                   # NOT YET IMPLEMENTED
    MUSIC = "Music"                 # NOT YET IMPLEMENTED


def dataToJson(data, file_name):
    with open(file_name, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except Exception as e:
            print(e)
            f.write(json.dumps(data))
    return
