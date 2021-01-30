from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from PIL import Image, ImageDraw, ImageFont
import random


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        create_default_profile_picture(instance)
        Profile.objects.create(user=instance)  # profile_picture="_______"


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()


def create_default_profile_picture(user):
    W, H = (300, 300)
    initials = (user.first_name[0] + user.last_name[0]).upper()

    profile_picture = Image.new('RGBA', (W, H), color=0)
    d = ImageDraw.Draw(profile_picture)

    f_co = (random.randint(0, 255), random.randint(150, 255), random.randint(150, 255))
    t_co = (random.randint(0, 255), random.randint(150, 255), random.randint(150, 255))

    opposite_direction = False
    if random.random() > 0.5:
        opposite_direction = True

    for i, color in enumerate(_interpolate(f_co, t_co, profile_picture.width * 2)):
        if opposite_direction:
            d.line([(i, 0), (0, i)], tuple(color), width=1)
        else:
            d.line([(profile_picture.width - i, 0), (profile_picture.width, i)], tuple(color), width=1)

    fnt = ImageFont.truetype(r'C:\Users\dts\AppData\Local\Microsoft\Windows\Fonts\coolvetica.ttf', 220)
    w, h = d.textsize(initials, font=fnt)
    d.text(((W - w) / 2, (H - h) / 2 - 30), initials, font=fnt, fill=(255, 255, 255))

    profile_picture.save("test.png", "PNG")


def _interpolate(f_co, t_co, interval):
    det_co = [(t - f) / interval for f, t in zip(f_co, t_co)]
    for i in range(interval):
        yield [round(f + det * i) for f, det in zip(f_co, det_co)]
