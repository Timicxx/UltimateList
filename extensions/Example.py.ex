class ExampleList():
    def __init__(self, website, output_format='.json'):
        self.website = website
        self.output_format = output_format
        self.limit = 10

    def getUserList(self, user_name):
        response = {
            "return": "User List Response"
        }
        return response

    def getEntry(self, entry_id):
        response = {
            "return": "Entry Response"
        }
        return response

    def searchEntry(self, search_input, page_number, parameters):
        response = {
            "return": "Search Result Response"
        }
        return response
