class Entry:
    def __init__(self, title, description, url, entry_id, cover):
        self.title = title
        self.description = description
        self.id = entry_id
        self.url = url
        self.cover = cover

    def listAllExtra(self):
        _extra_dict = {**self.__dict__}
        _new_extra_dict = {}
        del _extra_dict['title'], _extra_dict['description'], _extra_dict['url'], _extra_dict['id'], _extra_dict['cover']
        for name, extra in _extra_dict.items():
            _new_name = name.capitalize().replace('_', ' ')
            _new_extra_dict[_new_name] = extra
        return _new_extra_dict.items()


class Book(Entry):
    def __init__(self, title, description, url, entry_id, cover, publication_year, num_pages, author):
        super().__init__(title, description, url, entry_id, cover)
        self.publication_year = publication_year
        self.number_of_pages = num_pages
        self.author = author


class Movie(Entry):
    def __init__(self, title, description, url, entry_id, cover, genres, rating, runtime, movie_type, released):
        super().__init__(title, description, url, entry_id, cover)
        self.genres = genres
        self.rating = rating
        self.runtime = runtime
        self.type = movie_type
        self.released = released


class Comic(Entry):
    def __init__(self, title, description, url, entry_id, cover, count_of_issues, start_year):
        super().__init__(title, description, url, entry_id, cover)
        self.count_of_issues = count_of_issues
        self.start_year = start_year


class Game(Entry):
    def __init__(self, title, description, url, entry_id, cover, collection, genres, platforms, themes):
        super().__init__(title, description, url, entry_id, cover)
        self.collection = collection
        self.genres = genres
        self.platforms = platforms
        self.themes = themes


class SearchResult:
    def __init__(self, title, cover, entry_id, media_type):
        self.title = title
        self.cover = cover
        self.id = entry_id
        self.media_type = media_type
