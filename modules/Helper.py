import json
from enum import Enum


class MediaType(Enum):
    MOVIE = "Movie"
    COMIC = "Comic"
    BOOK = "Book"
    GAME = "Game"
    MUSIC = "Music"


def dataToJson(data, file_name):
    with open(file_name, 'w') as f:
        try:
            json.dump(data, f, indent=4)
        except Exception as e:
            print(e)
            f.write(json.dumps(data))
    return
