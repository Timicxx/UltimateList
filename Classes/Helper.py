import json
from enum import Enum

class MediaType(Enum):
    ANIME = "ANIME"                # CURRENTLY IMPLEMENTING
    MANGA = "MANGA"                # CURRENTLY IMPLEMENTING
    LIGHT_NOVEL = "LIGHT_NOVEL"    # NOT YES IMPLEMENTED
    VISUAL_NOVEL = "VISUAL_NOVEL"  # NOT YES IMPLEMENTED
    COMIC = "COMIC"                # NOT YES IMPLEMENTED
    MOVIE = "MOVIE"                # NOT YES IMPLEMENTED
    TV_SHOW = "TV_SHOW"            # NOT YES IMPLEMENTED
    GAME = "GAME"                  # NOT YES IMPLEMENTED
    BOOK = "BOOK"                  # NOT YES IMPLEMENTED

def dataToJson(data, file_name):
    with open(file_name, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except:
            f.write(json.dumps(data))
    return
