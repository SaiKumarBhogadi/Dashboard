from django.http import HttpResponseForbidden

def has_permission(user, module, action='view'):
    if not user.is_authenticated:
        return False
    return user.permissions.get(module, {}).get(action, False)
