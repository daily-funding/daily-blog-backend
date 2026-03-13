from django.contrib.auth import get_user_model


def create_user(username="test user", password="test password"):
    User = get_user_model()
    return User.objects.create_user(
        username=username,
        password=password,
    )
