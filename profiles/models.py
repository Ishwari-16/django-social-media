from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
      User = models.OneToOneField(
            User,
            on_delete=models.CASCADE
           # related_name="profile"
      )
