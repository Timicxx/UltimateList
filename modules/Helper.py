import json
from enum import Enum


class MediaType(Enum):
    ANIME = "Anime"                # CURRENTLY IMPLEMENTING
    MANGA = "Manga"                # CURRENTLY IMPLEMENTING
    LIGHT_NOVEL = "Light Novel"    # NOT YET IMPLEMENTED
    VISUAL_NOVEL = "Visual Novel"  # NOT YET IMPLEMENTED
    COMIC = "Comic"                # NOT YET IMPLEMENTED
    MOVIE = "Movie"                # NOT YET IMPLEMENTED
    TV_SHOW = "TV Show"            # NOT YET IMPLEMENTED
    GAME = "Game"                  # NOT YET IMPLEMENTED
    BOOK = "Book"                  # NOT YET IMPLEMENTED
    MUSIC = "Music"                # NOT YET IMPLEMENTED


def dataToJson(data, file_name):
    with open(file_name, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except Exception as e:
            print(e)
            f.write(json.dumps(data))
    return
