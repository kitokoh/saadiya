from .competitor_analysis_model import CompetitorAnalysisModel
from .competitor_analysis_widget import CompetitorAnalysisWidget
from .competitor_analysis_controller import CompetitorAnalysisController

def create_competitor_analysis_feature():
    model = CompetitorAnalysisModel()
    view = CompetitorAnalysisWidget()
    controller = CompetitorAnalysisController(model, view)
    return view, controller
