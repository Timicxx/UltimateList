from .Website import Website


class ListManager:
    def __init__(self):
        self.list = {}

    def addToList(self, entry):
        self.list[entry.key] = entry.value
