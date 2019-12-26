from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, is_superuser=0, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The username must be set'))
#        email = self.normalize_email(email)
        user = self.model(username=username, is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """

        return self.create_user(username, password, is_superuser=1, **extra_fields)

    def get_profile_picture_path(instance, filename):
        return instance.username + '/profile.png'
