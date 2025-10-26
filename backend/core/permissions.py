from django.core.exceptions import PermissionDenied

def is_admin(user):
    return user.is_authenticated and getattr(getattr(user,"profileuser",None),"role",None)=="admin"
