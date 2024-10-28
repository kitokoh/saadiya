# __init__.py
from fastapi import APIRouter

router = APIRouter()

from .user_controller import router as user_router
from .instance_controller import router as instance_router
from .license_controller import router as license_router
from .media_controller import router as media_router
from .group_controller import router as group_router
from .facebook_user_controller import router as facebook_user_router
from .alert_controller import router as alert_router
from .audit_log_controller import router as audit_log_router
from .quota_controller import router as quota_router
from .backup_log_controller import router as backup_log_router
from .user_role_controller import router as user_role_router
from .email_session_controller import router as email_session_router
from .user_session_controller import router as user_session_router
from .contact_controller import router as contact_router
from .instance_user_controller import router as instance_user_router
from .group_user_controller import router as group_user_router

router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(instance_router, prefix="/instances", tags=["Instances"])
router.include_router(license_router, prefix="/licenses", tags=["Licenses"])
router.include_router(media_router, prefix="/media", tags=["Media"])
router.include_router(group_router, prefix="/groups", tags=["Groups"])
router.include_router(facebook_user_router, prefix="/facebook_users", tags=["Facebook Users"])
router.include_router(alert_router, prefix="/alerts", tags=["Alerts"])
router.include_router(audit_log_router, prefix="/audit_logs", tags=["Audit Logs"])
router.include_router(quota_router, prefix="/quotas", tags=["Quotas"])
router.include_router(backup_log_router, prefix="/backup_logs", tags=["Backup Logs"])
router.include_router(user_role_router, prefix="/user_roles", tags=["User Roles"])
router.include_router(email_session_router, prefix="/email_sessions", tags=["Email Sessions"])
router.include_router(user_session_router, prefix="/user_sessions", tags=["User Sessions"])
router.include_router(contact_router, prefix="/contacts", tags=["Contacts"])
router.include_router(instance_user_router, prefix="/instance_users", tags=["Instance Users"])
router.include_router(group_user_router, prefix="/group_users", tags=["Group Users"])
