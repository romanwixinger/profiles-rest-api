from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, username: str, name: str, password=None, entitled_features=None):
        """Create a new user profile"""
        if entitled_features is None:
            entitled_features = ["joker_feature",
                                 "Einschätzungstest",
                                 "Dashboard",
                                 "Theorie",
                                 "Aufgaben"]
        if not username:
            raise ValueError('User must have a username')

        username = username.lower()
        username = "".join(username.split())
        user = self.model(username=username, name=name, entitled_features=entitled_features)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(username, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


def get_default_entitled_features():
    return ['joker_feature',
            'Einschätzungstest',
            'Dashboard',
            'Theorie',
            'Aufgaben']


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    username = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    entitled_features = models.TextField(default='joker_feature,Einschätzungstest,Dashboard,Theorie,Aufgaben',
                                         blank=True)

    objects = UserProfileManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve shot name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.username


class ProfileFeedItem(models.Model):
    """Profile status update"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text
