from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email: str, name: str, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve shot name of user"""
        return self.name

    def __str__(self):
        """Return string representation of our user"""
        return self.email


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


class Topic(models.Model):
    """Topic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        """Return the model as a string"""
        return self.name


class Subtopic(models.Model):
    """Subtopic"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    html = models.CharField(max_length=1024, blank=True)
    """topic = models.ManyToManyField(Topic)"""
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)

    def __str__(self):
        """Return the model as a string"""
        return self.name


class Question(models.Model):
    """Question"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE)
    dependencies = models.ManyToManyField(Subtopic)
    question = models.CharField(max_length=1024)
    correctAnswers = models.CharField(max_length=255)
    validation = models.CharField(max_length=255, blank=True)
    appendix = models.CharField(max_length=255, blank=True)
    hint = models.CharField(max_length=1024, blank=True)
    imageSrc = models.CharField(max_length=1024, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.question


class Answer(models.Model):
    """Answer"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    duration = models.DecimalField(max_digits=8, decimal_places=2) #in seconds
    answers = models.CharField(max_length=1024)

    #Fields set after correction
    correct = models.BooleanField(blank=True)
    skipped = models.BooleanField(blank=True)
    comment = models.CharField(max_length=1024)

    def __str__(self):
        """Return the model as a string"""
        return self.answers


class Test(models.Model):
    """Generic test"""
    user_profile = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE
    )
    questions = models.ManyToManyField(Question)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=1024, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.title


class CompletedTest(models.Model):
    """Completed test"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    answers = models.ManyToManyField(Answer, blank=True)
    state = models.CharField(max_length=255, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    duration = models.DecimalField(max_digits=8, decimal_places=2, blank=True) #in seconds
    comment = models.CharField(max_length=1024, blank=True)
    recommendedSubtopics = models.ManyToManyField(Subtopic, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return "Test started on " + self.created_on.__str__() + "."


class TheoryPage(models.Model):
    """Theory page"""
    user_profile = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, blank=True)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=255)
    html = models.CharField(max_length=1024, blank=True)
    test = models.ForeignKey(Test, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        """Return the model as a string"""
        return self.title



