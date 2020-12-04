from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"Profile: {self.user.username}"


class AccessCode(models.Model):
    code = models.CharField(max_length=6)
    remaining = models.PositiveSmallIntegerField(default=5)

    def __str__(self):
        return f"Code: {self.code} ({self.remaining})"
