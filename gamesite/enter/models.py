from django.db import models
# from users.models import User


class Tournament(models.Model):
    name = models.CharField(max_length=20)
    goals_scored = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    own_goals = models.IntegerField(default=0)
    hatricks = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Country(models.Model):

    class Meta:
        verbose_name_plural = "countries"

    name = models.CharField(max_length=20)
    country_code = models.CharField(max_length=3, default="")
    flag = models.ImageField(upload_to='flags_and_logos')

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

    # Fields
    name = models.CharField(
        max_length=1,
        choices=GROUP_CHOICES
        )
    goals_scored = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Team(models.Model):
    country = models.ForeignKey(
            Country,
            on_delete=models.CASCADE
            )
    logo = models.ImageField(upload_to='flags_and_logos', blank=True, null=True)
    group = models.ForeignKey(
            Group,
            on_delete=models.CASCADE
            )
    goals_scored = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    seconds_to_first_yellow = models.IntegerField(default=5400)
    seconds_to_first_goal = models.IntegerField(default=5400)

    def __str__(self):
        return self.country.name


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    goals_scored = models.IntegerField(default=0)
    team = models.ForeignKey(
            Team,
            on_delete=models.CASCADE
            )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Venue(models.Model):
    name = models.CharField(max_length=20)
    country = models.ForeignKey(
            Country,
            on_delete=models.CASCADE
            )
    city = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name


class Match(models.Model):

    class Meta:
        verbose_name_plural = "matches"

    HOME = "H"
    AWAY = "A"
    DRAW = "D"
    MATCH_RESULT_CHOICES = [
        (HOME, "Home"),
        (AWAY, "Away"),
        (DRAW, "Draw")
    ]

    # Fields
    match_number = models.IntegerField()
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
    ko_time = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES
        )

    def __str__(self):
        return f"Match {self.match_number}: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class GroupMatch(Match):

    class Meta:
        verbose_name_plural = "group matches"

    group = models.ForeignKey(
            Group,
            on_delete=models.CASCADE
            )

    def __str__(self):
        return f"Group {self.group.name}, Match {self.match_number}: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class GroupMatchBet(models.Model):
    HOME = "H"
    AWAY = "A"
    DRAW = "D"
    MATCH_RESULT_CHOICES = [
        (HOME, "Home"),
        (AWAY, "Away"),
        (DRAW, "Draw")
    ]

    # Fields
    bet = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES
        )
    match = models.ForeignKey(
            GroupMatch,
            on_delete=models.CASCADE
            )
    # user = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE
    #     )

    def __str__(self):
        return f"Group {self.match.group.name}, Match {self.match.match_number}: {self.bet}"


class FinalMatch(Match):

    class Meta:
        verbose_name_plural = "final matches"

    FIRST_HALF = "1H"
    SECOND_HALF = "2H"
    FIRST_ET = "1E"
    SECOND_ET = "2E"
    PEN_SHOOTOUT = "PS"
    MATCH_PERIOD_CHOICES = [
        (FIRST_HALF, "First Half"),
        (SECOND_HALF, "Second Half"),
        (FIRST_ET, "First Half of Extra Time"),
        (SECOND_ET, "Second Half of Extra Time"),
        (PEN_SHOOTOUT, "Penality Shootout")
    ]

    EUROPEAN = "EU"
    SOUTH_AMERICAN = "SA"
    OTHER = "OT"
    REF_CONTINENT_CHOICES = [
        (EUROPEAN, "European"),
        (SOUTH_AMERICAN, "South American"),
        (OTHER, "Other Continent")
    ]

    # Fields
    first_goal_period = models.CharField(
        max_length=2,
        choices=MATCH_PERIOD_CHOICES
        )
    own_goal = models.BooleanField(default=False)
    yellow_cards = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    ref_continent = models.CharField(
        max_length=2,
        choices=REF_CONTINENT_CHOICES
        )

    def __str__(self):
        return f"Final: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class Bets(models.Model):
    GROUP_MATCHES = "FM"
    GROUP_WINNERS = "GW"
    TOP_GOALSCORING_GROUP = "TG"
    TOP_GOALSCORING_PLAYER = "TP"
    BEST_TEAMS_SUCCESS = "TS"
    FIFTY_FIFTIES = "FF"
    TOURNAMENT_CHOICES = "TC"
    FINAL_CHOICES = "FC"
    BET_CATEGORY_CHOICES = [
        (GROUP_MATCHES, "Group Matches"),
        (GROUP_WINNERS, "Group Winners"),
        (TOP_GOALSCORING_GROUP, "Top Goalscoring Group"),
        (TOP_GOALSCORING_PLAYER, "Top Goalscoring Player"),
        (BEST_TEAMS_SUCCESS, "Best Teams Success"),
        (FIFTY_FIFTIES, "50/50s"),
        (TOURNAMENT_CHOICES, "Tournament Multiple Choice"),
        (FINAL_CHOICES, "Final Multiple Choice")
    ]

    category = models.CharField(max_length=2, choices=BET_CATEGORY_CHOICES)


class Entry(models.Model):
    date_created = models.DateTimeField()
    date_submitted = models.DateTimeField()
    has_paid = models.BooleanField(default=False)
    has_submitted = models.BooleanField(default=False)
    position = models.IntegerField(blank=True, null=True)
    bets = models.OneToOneField(Bets, on_delete=models.CASCADE)
