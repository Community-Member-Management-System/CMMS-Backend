from .models import User


def is_new_user(user: User):
    return not user.nick_name
