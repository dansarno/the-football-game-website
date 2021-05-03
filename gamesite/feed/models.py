from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from enter.models import CalledBet
from polymorphic.models import PolymorphicModel
from django.urls import reverse


class Sticker(models.Model):
    name = models.CharField(max_length=100)
    sticker_picture = models.ImageField(upload_to='sticker_pics')

    def __str__(self):
        return f"{self.name}"


class Post(models.Model):
    USER_POST = "U"
    BET_POST = "B"
    MATCH_POST = "M"
    TYPE_CHOICES = [
        (USER_POST, "User Post"),
        (BET_POST, "Called Bet Post"),
        (MATCH_POST, "Match Result Post")
    ]
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pinned = models.BooleanField(default=False)
    sticker = models.ForeignKey(
        Sticker, on_delete=models.CASCADE, blank=True, null=True)
    post_type = models.CharField(
        max_length=1, choices=TYPE_CHOICES, blank=True, null=True)
    called_bet = models.OneToOneField(
        CalledBet, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'"{self.title}" by {self.author.username}'

    def get_absolute_url(self):
        return reverse('feed:detail', kwargs={'pk': self.pk})


class MatchResultPost(models.Model):
    match = models.ForeignKey(
        'enter.GroupMatchOutcome', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Result: {self.match.match.home_team} vs {self.match.match.away_team} ({self.match.choice})'
