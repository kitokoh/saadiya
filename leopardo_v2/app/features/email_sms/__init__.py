from .email_sms_model import EmailSmsModel
from .email_sms_widget import EmailSmsWidget
from .email_sms_controller import EmailSmsController

def create_email_sms_feature():
    model = EmailSmsModel()
    view = EmailSmsWidget()
    controller = EmailSmsController(model, view)
    return view, controller
