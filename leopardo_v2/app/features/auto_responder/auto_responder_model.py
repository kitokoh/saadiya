class AutoResponderModel:
    def __init__(self):
        self.responses = {}

    def add_response(self, keyword, response):
        self.responses[keyword] = response

    def get_response(self, keyword):
        return self.responses.get(keyword, "I don't have a response for that.")
