from django.db import models
from django.utils import timezone
from users.models import Profile
from polymorphic.models import PolymorphicModel


class Outcome(PolymorphicModel):
    choice_group = models.ForeignKey(
        'ChoiceGroup', on_delete=models.CASCADE, null=True)
    winning_amount = models.IntegerField()

    # def __str__(self):
    #     return f"{self}"


class Entry(models.Model):

    class Meta:
        verbose_name_plural = "entries"

    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    has_submitted = models.BooleanField(default=False)
    current_position = models.IntegerField(blank=True, null=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='entries')
    current_score = models.IntegerField(default=0)
    bets = models.ManyToManyField(Outcome, through='Bet')
    label = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        if self.label:
            return f"{self.profile.user.username}'s entry {self.label}"
        else:
            return f"{self.profile.user.username}'s entry"


class ScoreLog(models.Model):
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name='score_logs')
    called_bet = models.ForeignKey('CalledBet', on_delete=models.CASCADE)
    score = models.IntegerField()


class PositionLog(models.Model):
    entry = models.ForeignKey(
        Entry, on_delete=models.CASCADE, related_name='position_logs')
    called_bet = models.ForeignKey('CalledBet', on_delete=models.CASCADE)
    position = models.IntegerField()


class Bet(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    success = models.BooleanField(blank=True, null=True)
    called_bet = models.ForeignKey(
        'CalledBet', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.outcome} by {self.entry}"


class GameCategory(models.Model):
    title = models.CharField(max_length=20)
    order = models.IntegerField()

    class Meta:
        verbose_name_plural = "game categories"

    def __str__(self):
        return self.title


class ChoiceGroup(models.Model):
    game_category = models.ForeignKey(
        GameCategory, on_delete=models.CASCADE, blank=True, null=True)
    order = models.IntegerField()
    when_called = models.DateTimeField()

    def __str__(self):
        return f"Choice Group ({self.order})"


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
    logo = models.ImageField(
        upload_to='flags_and_logos', blank=True, null=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    is_top_team = models.BooleanField(default=False)
    goals_scored = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    seconds_to_first_yellow = models.IntegerField(default=5400)
    seconds_to_first_goal = models.IntegerField(default=5400)

    def __str__(self):
        return self.country.name


class GroupWinnerOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.group.name}, {self.team.country.name} = {self.winning_amount}"


class TopGoalScoringGroupOutcome(Outcome):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Top Scoring: Group {self.group.name} = {self.winning_amount}"


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


class TopGoalScoringPlayerOutcome(Outcome):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name} = {self.winning_amount}"


class ToReachSemiFinalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To reach semi-final: {self.team.country.country_code} = {self.winning_amount}"


class ToReachFinalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To reach final: {self.team.country.country_code} = {self.winning_amount}"


class ToWinOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To win: {self.team.country.country_code} = {self.winning_amount}"


class HighestScoringTeamOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Highest scoring team: {self.team.country.country_code} = {self.winning_amount}"


class MostYellowCardsOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Most yellow cards: {self.team.country.country_code} = {self.winning_amount}"


class FastestYellowCardsOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Fastest yellow card: {self.team.country.country_code} = {self.winning_amount}"


class FastestGoalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Fastest goal: {self.team.country.country_code} = {self.winning_amount}"


class FiftyFiftyQuestion(models.Model):
    question = models.CharField(max_length=100)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.question


class FiftyFiftyOutcome(Outcome):
    fifty_fifty = models.ForeignKey(
        FiftyFiftyQuestion, on_delete=models.CASCADE)
    choice = models.BooleanField()

    def __str__(self):
        return f"{self.fifty_fifty.question}, {self.choice} = {self.winning_amount}"


class TournamentGoalsOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total goals: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Total goals: {self.min_value} - {self.max_value}" \
                f" = {self.winning_amount}"
        elif self.max_value:
            return f"Total goals: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Total goals: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


class TournamentRedCardsOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total red cards: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Total red cards: {self.min_value} - {self.max_value}" \
                   f" = {self.winning_amount}"
        elif self.max_value:
            return f"Total red cards: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Total red cards: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


class TournamentOwnGoalsOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total own goals: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Total own goals: {self.min_value} - {self.max_value}" \
                   f" = {self.winning_amount}"
        elif self.max_value:
            return f"Total own goals: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Total own goals: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


class TournamentHattricksOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total hattricks: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Total hattricks: {self.min_value} - {self.max_value}" \
                   f" = {self.winning_amount}"
        elif self.max_value:
            return f"Total hattricks: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Total hattricks: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


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
        related_name="match_home_team",
        blank=True,
        null=True
    )
    away_team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="match_away_team",
        blank=True,
        null=True
    )
    ko_time = models.DateTimeField()
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES,
        blank=True
    )

    def __str__(self):
        return f"Match {self.match_number}"


class GroupMatch(Match):

    class Meta:
        verbose_name_plural = "group matches"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.group.name}, Match {self.match_number}: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class GroupMatchOutcome(Outcome):
    match = models.ForeignKey(GroupMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=1, choices=GroupMatch.MATCH_RESULT_CHOICES)

    def __str__(self):
        return f"Group {self.match.group.name}, Match {self.match.match_number}: {self.choice} = {self.winning_amount}"


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
        max_length=2, choices=MATCH_PERIOD_CHOICES, blank=True, null=True)
    own_goal = models.BooleanField(default=False)
    yellow_cards = models.IntegerField(default=0, blank=True, null=True)
    goals = models.IntegerField(default=0, blank=True, null=True)
    ref_continent = models.CharField(
        max_length=2, choices=REF_CONTINENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return "Final match"


class FinalFirstGoalOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=2, choices=FinalMatch.MATCH_PERIOD_CHOICES)

    def __str__(self):
        return f"{self.choice} = {self.winning_amount}"

    def verbose_outcome(self):
        return dict(FinalMatch.MATCH_PERIOD_CHOICES)[self.choice]


class FinalOwnGoalOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    choice = models.BooleanField()

    def __str__(self):
        return f"{self.choice} = {self.winning_amount}"

    def verbose_outcome(self):
        if self.choice:
            return "Yes there will be"
        else:
            return "No there won't be"


class FinalYellowCardsOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Final yellows: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Final yellows: {self.min_value} - {self.max_value}" \
                   f" = {self.winning_amount}"
        elif self.max_value:
            return f"Final yellows: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Final yellows: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


class FinalRefContinentOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=2, choices=FinalMatch.REF_CONTINENT_CHOICES)

    def __str__(self):
        return f"{self.choice} = {self.winning_amount}"

    def verbose_outcome(self):
        return dict(FinalMatch.REF_CONTINENT_CHOICES)[self.choice]


class FinalGoalsOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Final goals: {self.min_value} = {self.winning_amount}"
        elif self.min_value and self.max_value:
            return f"Final goals: {self.min_value} - {self.max_value}" \
                   f" = {self.winning_amount}"
        elif self.max_value:
            return f"Final goals: {self.max_value} or fewer" \
                   f" = {self.winning_amount}"
        else:
            return f"Final goals: {self.min_value} or more" \
                   f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"


class CalledBet(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.outcome}"


class CalledBetStats(models.Model):
    called_bet = models.OneToOneField(CalledBet, on_delete=models.CASCADE)
    num_correct = models.IntegerField(null=True, blank=True)
    num_incorrect = models.IntegerField(null=True, blank=True)
