from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# imagekit
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill



User = settings.AUTH_USER_MODEL
# Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female','Female'),
    ('Other', 'Other')
)



class User(AbstractUser):
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)

    # USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username',]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
