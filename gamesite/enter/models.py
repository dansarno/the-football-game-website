from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from users.models import Profile
from polymorphic.models import PolymorphicModel


def restrict_number_of_entries(value):
    if Entry.objects.filter(profile__id=value).count() >= 3:
        raise ValidationError("Profile already has maximum number of entries (3)")



class Outcome(PolymorphicModel):
    choice_group = models.ForeignKey(
        'ChoiceGroup', on_delete=models.CASCADE, null=True)
    winning_amount = models.IntegerField()


class Entry(models.Model):

    class Meta:
        verbose_name_plural = "entries"

    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    date_submitted = models.DateTimeField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    has_submitted = models.BooleanField(default=False)
    current_position = models.IntegerField(blank=True, null=True)
    current_team_position = models.IntegerField(blank=True, null=True)
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='entries', validators=(restrict_number_of_entries,))
    current_score = models.IntegerField(default=0)
    correct_bets = models.IntegerField(default=0)
    bets = models.ManyToManyField(Outcome, through='Bet')
    label = models.CharField(max_length=1, blank=True, null=True)

    def __str__(self):
        if self.label:
            return f"{self.profile.user.username}'s entry {self.label}"
        else:
            return f"{self.profile.user.username}'s entry"

    def get_absolute_url(self):
        return reverse('enter:view_entry', kwargs={'entry_id': self.id})

    def save(self, *args, **kwargs):
        if not self.pk and self.profile.entries.all().count() >= 3:
            raise ValidationError('Profile already has maximum number of entries (3)')
        return super(Entry, self).save(*args, **kwargs)


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

    def get_prev_position_log(self):
        return PositionLog.objects.filter(
            entry=self.entry, called_bet__date__lt=self.called_bet.date).order_by('-called_bet__date').first()


class Bet(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    success = models.BooleanField(blank=True, null=True)
    called_bet = models.ForeignKey(
        'CalledBet', on_delete=models.SET_NULL, blank=True, null=True)
    updated_on = models.DateTimeField(blank=True, null=True)

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

    @property
    def short_choice(self):
        if self.country.country_code == 'OTH':
            return "Other"
        else:
            return self.country.country_code


class GroupWinnerOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.group.name} Winner → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"To Win {self.group.name}"

    @property
    def short_choice(self):
        return self.team.short_choice


class TopGoalScoringGroupOutcome(Outcome):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Top Scoring Group → {self.group.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Top Scoring Group"

    @property
    def short_choice(self):
        return self.group.name


class Player(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    order = models.IntegerField(blank=True, null=True)
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class TopGoalScoringPlayerOutcome(Outcome):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"Top Goalscorer → {self.short_choice} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Top Goalscorer"

    @property
    def short_choice(self):
        if self.player.first_name.lower() == "other" and self.player.last_name.lower() == "player":
            return "Other"
        else:
            return f"{self.player.first_name[0].upper()}. {self.player.last_name}"


class ToReachSemiFinalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To Reach Semis → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"To Reach Semis"

    @property
    def short_choice(self):
        return self.team.short_choice


class ToReachFinalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To Reach Final → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"To Reach Final"

    @property
    def short_choice(self):
        return self.team.short_choice


class ToWinOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"To Win → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"To Win"

    @property
    def short_choice(self):
        return self.team.short_choice


class HighestScoringTeamOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Highest Scoring Team → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Highest Scoring Team"

    @property
    def short_choice(self):
        return self.team.short_choice


class MostYellowCardsOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Most Yellows → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Most Yellows"

    @property
    def short_choice(self):
        return self.team.short_choice


class FastestYellowCardsOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Fastest Yellow → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Fastest Yellow"

    @property
    def short_choice(self):
        return self.team.short_choice


class FastestGoalOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Fastest Goal → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Fastest Goal"

    @property
    def short_choice(self):
        return self.team.short_choice


class MostCleanSheetsOutcome(Outcome):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={
                             'is_top_team': True})

    def __str__(self):
        return f"Most Clean Sheets → {self.team.country.name} ({self.winning_amount})"

    @property
    def short_question(self):
        return f"Most Clean Sheets"

    @property
    def short_choice(self):
        return self.team.short_choice


class FiftyFiftyQuestion(models.Model):
    question = models.CharField(max_length=100)
    brief_question = models.CharField(max_length=100, blank=True, null=True)
    order = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.question


class FiftyFiftyOutcome(Outcome):
    fifty_fifty = models.ForeignKey(
        FiftyFiftyQuestion, on_delete=models.CASCADE)
    choice = models.BooleanField()

    def __str__(self):
        return f"{self.fifty_fifty} → {self.choice} ({self.winning_amount})"

    @property
    def short_question(self):
        return self.fifty_fifty.brief_question

    @property
    def short_choice(self):
        if self.choice:
            return "Yes"
        else:
            return "No"


class TournamentGoalsOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total Goals → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Total Goals → {self.min_value} - {self.max_value}" \
                f" ({self.winning_amount})"
        elif self.max_value:
            return f"Total Goals → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Total Goals → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Total Goals"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


class TournamentPenaltiesOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total Pens → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Total Pens → {self.min_value} - {self.max_value}" \
                   f" ({self.winning_amount})"
        elif self.max_value:
            return f"Total Pens → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Total Pens → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Total Pens"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


class TournamentOwnGoalsOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Total Own Goals → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Total Own Goals → {self.min_value} - {self.max_value}" \
                   f" ({self.winning_amount})"
        elif self.max_value:
            return f"Total Own Goals → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Total Own Goals → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Total OGs"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


class TournamentGoalsInAGameOutcome(Outcome):
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Most Goals in a Single Game → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Most Goals in a Single Game → {self.min_value} - {self.max_value}" \
                   f" ({self.winning_amount})"
        elif self.max_value:
            return f"Most Goals in a Single Game → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Most Goals in a Single Game → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Goals in a Game"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


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
    result = models.CharField(
        max_length=1,
        choices=MATCH_RESULT_CHOICES,
        blank=True
    )

    def __str__(self):
        return f"Match {self.match_number}"

    @property
    def short_question(self):
        return f"{self.home_team.short_choice} v {self.away_team.short_choice}"


class GroupMatch(Match):

    class Meta:
        verbose_name_plural = "group matches"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.group.name}, Match {self.match_number}: {self.home_team.country.country_code} v {self.away_team.country.country_code}"


class GroupMatchOutcome(Outcome):
    match = models.ForeignKey(GroupMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=1, choices=GroupMatch.MATCH_RESULT_CHOICES)

    def __str__(self):
        return f"Match {self.match.match_number}, {self.short_question} → {self.verbose_outcome()} ({self.winning_amount})"

    @property
    def short_question(self):
        return self.match.short_question

    def verbose_outcome(self):
        return dict(Match.MATCH_RESULT_CHOICES)[self.choice]

    @property
    def short_choice(self):
        return self.choice


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
        (FIRST_ET, "First Half of ET"),
        (SECOND_ET, "Second Half of ET"),
        (PEN_SHOOTOUT, "Penalty Shootout")
    ]
    SHORT_MATCH_PERIOD_CHOICES = [
        (FIRST_HALF, "1st Half"),
        (SECOND_HALF, "2nd Half"),
        (FIRST_ET, "1st ET"),
        (SECOND_ET, "2nd ET"),
        (PEN_SHOOTOUT, "Pens")
    ]

    ENGLAND = "ENG"
    SPAIN = "ESP"
    ITALY = "ITA"
    GERMANY = "GER"
    OTHER = "OTH"
    REF_COUNTRY_CHOICES = [
        (ENGLAND, "English"),
        (SPAIN, "Spanish"),
        (ITALY, "Italian"),
        (GERMANY, "German"),
        (OTHER, "Other")
    ]
    SHORT_REF_COUNTRY_CHOICES = [
        (ENGLAND, "ENG"),
        (SPAIN, "ESP"),
        (ITALY, "ITA"),
        (GERMANY, "GER"),
        (OTHER, "OTH")
    ]

    # Fields
    first_goal_period = models.CharField(
        max_length=2, choices=MATCH_PERIOD_CHOICES, blank=True, null=True)
    own_goal = models.BooleanField(default=False)
    yellow_cards = models.IntegerField(default=0, blank=True, null=True)
    goals = models.IntegerField(default=0, blank=True, null=True)
    ref_country = models.CharField(
        max_length=3, choices=REF_COUNTRY_CHOICES, blank=True, null=True)

    def __str__(self):
        return "Final match"


class FinalFirstGoalOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=2, choices=FinalMatch.MATCH_PERIOD_CHOICES)

    def __str__(self):
        return f"First Final Goal → {self.short_choice} ({self.winning_amount})"

    def verbose_outcome(self):
        return dict(FinalMatch.MATCH_PERIOD_CHOICES)[self.choice]

    @property
    def short_question(self):
        return "First Final Goal"

    @property
    def short_choice(self):
        return dict(FinalMatch.SHORT_MATCH_PERIOD_CHOICES)[self.choice]


class FinalYellowCardsOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Final Yellows → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Final Yellows → {self.min_value} - {self.max_value}" \
                   f" ({self.winning_amount})"
        elif self.max_value:
            return f"Final Yellows → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Final Yellows → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Final Yellows"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


class FinalRefCountryOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    choice = models.CharField(
        max_length=3, choices=FinalMatch.REF_COUNTRY_CHOICES)

    def __str__(self):
        return f"Final Ref → {self.short_choice} ({self.winning_amount})"

    def verbose_outcome(self):
        return dict(FinalMatch.REF_COUNTRY_CHOICES)[self.choice]

    @property
    def short_question(self):
        return "Final Ref"

    @property
    def short_choice(self):
        return dict(FinalMatch.SHORT_REF_COUNTRY_CHOICES)[self.choice]


class FinalGoalsOutcome(Outcome):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField(blank=True, null=True)
    max_value = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"Final Goals → {self.min_value} ({self.winning_amount})"
        elif self.min_value and self.max_value:
            return f"Final Goals → {self.min_value} - {self.max_value}" \
                   f" ({self.winning_amount})"
        elif self.max_value:
            return f"Final Goals → {self.max_value} or fewer" \
                   f" ({self.winning_amount})"
        else:
            return f"Final Goals → {self.min_value} or more" \
                   f" ({self.winning_amount})"

    def verbose_outcome(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value} to {self.max_value}"
        elif self.max_value:
            return f"{self.max_value} or fewer"
        else:
            return f"{self.min_value} or more"

    @property
    def short_question(self):
        return "Final Goals"

    @property
    def short_choice(self):
        if self.min_value == self.max_value and self.min_value is not None:
            return f"{self.min_value}"
        elif self.min_value and self.max_value:
            return f"{self.min_value}-{self.max_value}"
        elif self.max_value:
            return f"<{self.max_value}"
        else:
            return f">{self.min_value}"


class CalledBet(models.Model):
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.outcome}"


class CalledBetStats(models.Model):
    called_bet = models.OneToOneField(CalledBet, on_delete=models.CASCADE)
    num_correct = models.IntegerField(null=True, blank=True)
    num_incorrect = models.IntegerField(null=True, blank=True)
