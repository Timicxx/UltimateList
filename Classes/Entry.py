from .Helper import MediaType


class Entry:
    def __init__(self, entry_id, entry_title, entry_type, source):
        self.id = 0
        self.title = entry_title
        self.type = entry_type
        self.source_id = entry_id
        self.source = source


class Anime(Entry):
    def __init__(self, entry_id, entry_title, entry_status, entry_progress, entry_episodes, entry_score, entry_cover_image, entry_genres, entry_tags, source):
        super().__init__(entry_id, entry_title, MediaType.ANIME, source)
        self.status = entry_status
        self.progress = entry_progress
        self.episodes = entry_episodes
        self.score = entry_score
        self.cover_image = entry_cover_image
        self.genres = entry_genres
        self.tags = entry_tags


class Manga(Entry):
    def __init__(self, entry_id, entry_title, entry_status, entry_progress, entry_chapters, entry_score, entry_cover_image, entry_genres, entry_tags, source):
        super().__init__(entry_id, entry_title, MediaType.MANGA, source)
        self.status = entry_status
        self.progress = entry_progress
        self.chapters = entry_chapters
        self.score = entry_score
        self.cover_image = entry_cover_image
        self.genres = entry_genres
        self.tags = entry_tags

