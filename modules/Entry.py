from .Helper import MediaType


class Entry:
    def __init__(self, entry_title, source_url, entry_type):
        self.title = entry_title
        self.type = entry_type
        self.source_url = source_url
        self.is_adult = False
