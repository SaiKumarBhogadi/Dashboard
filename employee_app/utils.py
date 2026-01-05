from employee_app.permission_defaults import ROLE_PERMISSIONS


def has_permission(user, module, action='view'):
    # 🔥 Super admin always allowed
    if user.is_superuser or user.role == 'super_admin':
        return True

    if not user.is_authenticated:
        return False

    # Use user.permissions if exists, else fallback to role defaults
    permissions = user.permissions or ROLE_PERMISSIONS.get(user.role, {})

    return permissions.get(module, {}).get(action, False)

# employee_app/utils.py
from .models import Notification

def create_notification(recipient, ntype, title, message, link=None):
    """
    Creates an in-app notification for a logged-in user (CustomUser).
    """
    if recipient and recipient.is_active:
        Notification.objects.create(
            recipient=recipient,
            notification_type=ntype,
            title=title,
            message=message,
            link=link,
        )
