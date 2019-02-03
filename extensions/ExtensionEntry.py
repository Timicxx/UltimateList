from modules.Entry import Entry


class VisualNovel(Entry):
    def __init__(self, title, description, url, entry_id, cover, platforms, released):
        super().__init__(title, description, url, entry_id, cover)
        self.platforms = platforms
        self.released = released


class Cartoon(Entry):
    def __init__(self, title, description, url, entry_id, cover, episodes, genres, tags):
        super().__init__(title, description, url, entry_id, cover)
        self.episodes = episodes
        self.genres = genres
        self.tags = tags


class AlternativeComic(Entry):
    def __init__(self, title, description, url, entry_id, cover, chapters, genres, tags):
        super().__init__(title, description, url, entry_id, cover)
        self.chapters = chapters
        self.genres = genres
        self.tags = tags

