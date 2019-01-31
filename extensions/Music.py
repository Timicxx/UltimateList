class MusicList():
    def __init__(self, website, output_format='.json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10

    def responseToResult(self, response):
        return response

    def responseToEntry(self, response):
        return response

    def getUserList(self, user_name):
        return { 'return': 'Not yet implemented', 'reason': 'API does not support this feature' }

    def getEntry(self, entry_id):
        response = { 'return': 'Not yet implemented' }
        return self.responseToEntry(response)

    def searchEntry(self, search_input, page_number, parameters):
        response = { 'return': 'Not yet implemented' }
        return self.responseToResult(response)