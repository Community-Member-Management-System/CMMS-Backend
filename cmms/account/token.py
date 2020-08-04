from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .utils import is_new_user


def get_tokens_for_user(user: User):
    refresh = RefreshToken.for_user(user)
    refresh['new'] = is_new_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
