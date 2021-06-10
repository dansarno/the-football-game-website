from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from random import randint
from PIL import Image


def generate_random_code():
    return ''.join([f"{randint(0, 9)}" for _ in range(0, 10)])


class _Image(Image.Image):

    def crop_to_aspect(self, aspect, divisor=1, alignx=0.5, aligny=0.5):
        """Crops an image to a given aspect ratio.
        Args:
            aspect (float): The desired aspect ratio.
            divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
            alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
            aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
        Returns:
            Image: The cropped Image object.
        """
        if self.width / self.height > aspect / divisor:
            newwidth = int(self.height * (aspect / divisor))
            newheight = self.height
        else:
            newwidth = self.width
            newheight = int(self.width / (aspect / divisor))
        img = self.crop((alignx * (self.width - newwidth),
                         aligny * (self.height - newheight),
                         alignx * (self.width - newwidth) + newwidth,
                         aligny * (self.height - newheight) + newheight))
        return img

Image.Image.crop_to_aspect = _Image.crop_to_aspect


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        default='default.jpg', upload_to='profile_pics')
    team = models.ForeignKey(
        'Team', on_delete=models.SET_NULL, blank=True, null=True)
    bio = models.TextField(max_length=160, blank=True, null=True)
    access_code = models.ForeignKey("AccessCode", blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Profile: {self.user.username}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            cropped = img.crop_to_aspect(1)
            cropped.thumbnail(output_size, Image.ANTIALIAS)
            cropped.save(self.profile_picture.path)

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})


class Team(models.Model):
    name = models.CharField(max_length=30)
    position = models.IntegerField(blank=True, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Prize(models.Model):
    TOP = "T"
    MIDDLE = "M"
    BOTTOM = "B"
    BAND_CHOICES = [
        (TOP, "Top"),
        (MIDDLE, "Middle"),
        (BOTTOM, "Bottom")
    ]
    winning_amount = models.DecimalField(max_digits=6, decimal_places=2)
    position = models.IntegerField()
    band = models.CharField(max_length=1, choices=BAND_CHOICES)

    def __str__(self):
        return f"{self.position} ({self.get_band_display()} Prize) : £{self.winning_amount}"


class AccessCode(models.Model):
    code = models.CharField(max_length=10, default=generate_random_code)
    remaining = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f"Code: {self.code} ({self.remaining})"
