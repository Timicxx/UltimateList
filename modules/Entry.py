from .Helper import MediaType


class Entry:
    def __init__(self, title, description, url, cover):
        self.title = title
        self.description = description
        self.url = url
        self.cover = cover


class Book(Entry):
    def __init__(self, title, description, url, cover):
        super().__init__(title, description, url, cover)


class Music(Entry):
    def __init__(self, title, description, url, cover):
        super().__init__(title, description, url, cover)


class Movie(Entry):
    def __init__(self, title, description, url, cover, genres, rating, runtime, movie_type, released):
        super().__init__(title, description, url, cover)
        self.genres = genres
        self.rating = rating
        self.runtime = runtime
        self.type = movie_type
        self.released = released


class Comic(Entry):
    def __init__(self, title, description, url, cover, count_of_issues, start_year):
        super().__init__(title, description, url, cover)
        self.count_of_issues = count_of_issues
        self.start_year = start_year


class Game(Entry):
    def __init__(self, title, description, url, cover, collection, genres, platforms, themes):
        super().__init__(title, description, url, cover)
        self.collection = collection
        self.genres = genres
        self.platforms = platforms
        self.themes = themes


class SearchResult:
    def __init__(self, title, cover, url, media_type):
        self.title = title
        self.cover = cover
        self.url = url
        self.media_type = media_type
