class ContentGeneratorController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
