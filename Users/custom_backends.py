from rest_framework import authentication
from django.contrib.auth.backends import AllowAllUsersModelBackend, BaseBackend
from django.contrib.auth import get_user_model
from Users.constants import EMAIL_PATTERN, INVALID_EMAIL_FORMAT

from regex_validations import RegexValidation
from django.db.models import Q
User = get_user_model()





class EmailorUsername(authentication.BaseAuthentication):
    """
    This is a ModelBacked that allows authentication with either a username or an email address.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))
        except User.DoesNotExist:
            return None
        else:
            if user.check_password(password):
                return user
        return None

class EmailBackend(AllowAllUsersModelBackend):
    """
    This is a ModelBacked that allows authentication with either a username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.get_user(kwargs={"email": username})
        except User.DoesNotExist:
            return None
        else:
            if user and user.check_password(password):
                return user
        return None
