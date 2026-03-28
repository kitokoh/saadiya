from .competitor_analysis_model import CompetitorAnalysisModel
from .competitor_analysis_widget import CompetitorAnalysisWidget

class CompetitorAnalysisController:
    def __init__(self, model: CompetitorAnalysisModel, view: CompetitorAnalysisWidget):
        self.model = model
        self.view = view
        self.connect_signals()

    def connect_signals(self):
        pass
