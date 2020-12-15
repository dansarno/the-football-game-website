from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from enter.models import Match


class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'"{self.title}" by {self.author.username}'

    def get_absolute_url(self):
        return reverse('feed:detail', kwargs={'pk': self.pk})


class MatchResultPost(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Result: {self.match.home_team} vs {self.match.away_team} ({self.match.result})'
