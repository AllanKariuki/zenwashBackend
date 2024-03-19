import datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from .models import CustomToken

def expired_in(token):
    """Time left to live for token"""
    elapsed_time = timezone.now()-token.created
    time_left = timedelta(seconds = settings.TOKEN_LIFESPAN) - elapsed_time
    return time_left

def has_token_expired(token):
    """check whether token has expired"""
    return expired_in(token) < timedelta(seconds=0)

def expired_token_handler(token):
    """Delete expired token and return boolean value of whether token is expired or not"""

    is_expired = has_token_expired(token)
    if is_expired:
        token.delete()
    return is_expired, token

class CustomAuthentication(TokenAuthentication):
    """Custom authentication class"""

    def authenticate_credentials(self, key):
        try:
            token = CustomToken.objects.get(key)
        except CustomToken.DoesNotExist:
            raise AuthenticationFailed({'details':'Token you are using is invalid', 'code':600})

        self.is_expired, self.token = expired_token_handler(token)

        if self.is_expired:
            raise AuthenticationFailed({'details':'Token you are using has expired', 'code' : 600})

        if not self.token.user.is_active:
            raise AuthenticationFailed({'details' : 'The user you are using is currently inactive kindly activate their account',
                                        'code': 603})

        return (self.token.user, self.token)