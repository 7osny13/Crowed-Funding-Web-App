from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.six import text_type
from django.contrib.auth.models import User


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # return str(user.pk) + str(timestamp) + str(user.is_active)
        # return super()._make_hash_value(user, timestamp)
        return (text_type(user.is_active) + text_type(user.pk)+text_type( timestamp))

token_generator = AppTokenGenerator()