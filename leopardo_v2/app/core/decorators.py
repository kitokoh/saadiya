from functools import wraps
from PyQt5.QtWidgets import QMessageBox
from ..services.service_container import container

def pro_feature(feature_level):
    def decorator(func):
        @wraps(func)
        def wrapper(main_window, *args, **kwargs):
            auth_service = container.get('auth_service')
            if auth_service.has_access(feature_level):
                return func(main_window, *args, **kwargs)
            else:
                QMessageBox.warning(main_window, "Upgrade Required", f"This feature is only available for {feature_level} users. Please upgrade your plan to access it.")
        return wrapper
    return decorator
