from django.db import models
from django.contrib.auth.models import User
from random import randint


def generate_random_code():
    return ''.join([f"{randint(0, 9)}" for _ in range(0, 10)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"Profile: {self.user.username}"


class AccessCode(models.Model):
    code = models.CharField(max_length=10, default=generate_random_code)
    remaining = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"Code: {self.code} ({self.remaining})"
