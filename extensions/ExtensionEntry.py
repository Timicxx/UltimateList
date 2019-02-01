from modules.Entry import Entry


class VisualNovel(Entry):
    def __init__(self, title, description, url, entry_id, cover, platforms, released):
        super().__init__(title, description, url, entry_id, cover)
        self.platforms = platforms
        self.released = released
