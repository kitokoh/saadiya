import json
from PyQt5.QtCore import QObject, pyqtSlot

class ActionHandler(QObject):
    """Handler for JavaScript to Python actions"""
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    @pyqtSlot(str)
    def handleAction(self, action_data):
        """Handle actions sent from JavaScript"""
        try:
            data = json.loads(action_data)
            if hasattr(self.parent, 'execute_action'):
                self.parent.execute_action(data)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
        except Exception as e:
            print(f"Error processing action: {e}")
