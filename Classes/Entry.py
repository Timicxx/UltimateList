from .Helper import MediaType

class Entry:
    def __init__(self, entry_id, entry_name, entry_type):
        self.id = entry_id
        self.name = entry_name
        self.type = entry_type

        
class Anime(Entry):
    def __init__(self, entry_id, entry_name, entry_status, entry_progress, entry_episodes, entry_score, entry_cover_image, entry_genres, entry_tags):
        super().__init__(entry_id, entry_name, MediaType.ANIME)
        self.status = entry_status
        self.progress = entry_progress
        self.episodes = entry_episodes
        self.score = entry_score
        self.cover_image = entry_cover_image
        self.genres = entry_genres
        self.tags = entry_tags