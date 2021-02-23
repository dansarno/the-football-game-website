from django.db import models
from django.contrib.auth.models import User
from random import randint
from PIL import Image


def generate_random_code():
    return ''.join([f"{randint(0, 9)}" for _ in range(0, 10)])


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(default='default.jpg', upload_to='profile_pics')
    team = models.ForeignKey('Team', on_delete=models.SET_NULL, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(max_length=160, blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)


class Team(models.Model):
    name = models.CharField(max_length=30)
    position = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class AccessCode(models.Model):
    code = models.CharField(max_length=10, default=generate_random_code)
    remaining = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"Code: {self.code} ({self.remaining})"
