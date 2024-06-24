from django.contrib.auth.models import AbstractUser
from django.db import models

from ..core.models import BaseModel

# Create your models here.


class User(AbstractUser, BaseModel):
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

