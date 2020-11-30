from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=3, default="")

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Group(models.Model):
    GROUP_A = "A"
    GROUP_B = "B"
    GROUP_C = "C"
    GROUP_D = "D"
    GROUP_E = "E"
    GROUP_F = "F"
    GROUP_CHOICES = [
        (GROUP_A, "Group A"),
        (GROUP_B, "Group B"),
        (GROUP_C, "Group C"),
        (GROUP_D, "Group D"),
        (GROUP_E, "Group E"),
        (GROUP_F, "Group F")
    ]

    name = models.CharField(
        max_length=1,
        choices=GROUP_CHOICES
        )
    team_1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="group_team_1"
        )
    team_2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="group_team_2"
        )
    team_3 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="group_team_3"
        )
    team_4 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="group_team_4"
        )
    winner = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="group_winner",
        blank=True,
        null=True
        )

    def __str__(self):
        return self.name


class GroupMatch(models.Model):
    HOME = "H"
    AWAY = "A"
    DRAW = "D"
    MATCH_RESULT_CHOICES = [
        (HOME, "Home"),
        (AWAY, "Away"),
        (DRAW, "Draw")
    ]

    home_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="match_home_team"
        )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="match_away_team"
        )
    game_number = models.IntegerField()
    ko_time = models.DateTimeField()
    location = models.ForeignKey(Venue, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES
        )

    def __str__(self):
        return f"Game {self.game_number}: {self.home_team.country_code} v {self.away_team.country_code}"


class GroupMatchBet(models.Model):
    HOME = "H"
    AWAY = "A"
    DRAW = "D"
    MATCH_RESULT_CHOICES = [
        (HOME, "Home"),
        (AWAY, "Away"),
        (DRAW, "Draw")
    ]

    bet = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES
        )
    def __str__(self):
        return f"Game {self.game_number}: {self.bet}"
