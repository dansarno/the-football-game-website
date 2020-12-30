from django.db import models
from django.utils import timezone
from users.models import Profile


class Entry(models.Model):

    class Meta:
        verbose_name_plural = "entries"

    date_created = models.DateTimeField(default=timezone.now)
    date_submitted = models.DateTimeField(blank=True, null=True)
    has_paid = models.BooleanField(default=False)
    has_submitted = models.BooleanField(default=False)
    position = models.IntegerField(blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Entry {self.id}: {self.profile.user.username}"


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


class GroupWinnerOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"Group {self.group.name}, {self.team.country.name} = {self.winning_amount}"


class GroupWinnerBet(models.Model):
    bet = models.ForeignKey(GroupWinnerOutcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.bet.group.name}, {self.bet.team.country.name} by {self.entry.profile.user.username}"


class TopGoalScoringGroupOutcome(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"Group {self.group.name} = {self.winning_amount}"


class TopGoalscoringGroupBet(models.Model):
    bet = models.ForeignKey(TopGoalScoringGroupOutcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.bet.group.name} by {self.entry.profile.user.username}"


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


class TopGoalScoringPlayerOutcome(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.player.first_name} {self.player.last_name}, {self.winning_amount}"


class TopGoalscoringPlayerBet(models.Model):
    bet = models.ForeignKey(TopGoalScoringPlayerOutcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bet.player.first_name} {self.bet.player.last_name}"


class ToReachSemiFinalOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class ToReachFinalOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class ToWinOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class HighestScoringTeamOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class MostYellowCardsOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class FastestYellowCardsOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class FastestGoalOutcome(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, limit_choices_to={'is_top_team': True})
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.team.country.country_code} = {self.winning_amount}"


class BestTeamsSuccessBetGroup(models.Model):
    to_reach_semi_final_bet = models.ForeignKey(ToReachSemiFinalOutcome, on_delete=models.CASCADE)
    to_reach_final_bet = models.ForeignKey(ToReachFinalOutcome, on_delete=models.CASCADE,)
    to_win_bet = models.ForeignKey(ToWinOutcome, on_delete=models.CASCADE)
    highest_scoring_team_bet = models.ForeignKey(HighestScoringTeamOutcome, on_delete=models.CASCADE)
    most_yellow_cards_bet = models.ForeignKey(MostYellowCardsOutcome, on_delete=models.CASCADE)
    fastest_yellow_card_bet = models.ForeignKey(FastestYellowCardsOutcome, on_delete=models.CASCADE)
    fastest_tournament_goal_bet = models.ForeignKey(FastestGoalOutcome, on_delete=models.CASCADE)
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Top teams bets by {self.entry.profile.user.username}"


class FiftyFiftyQuestion(models.Model):
    question = models.CharField(max_length=100)

    def __str__(self):
        return self.question


class FiftyFiftyOutcome(models.Model):
    fifty_fifty = models.ForeignKey(FiftyFiftyQuestion, on_delete=models.CASCADE)
    outcome = models.BooleanField()
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.fifty_fifty.question}, {self.outcome} = {self.winning_amount}"


class FiftyFiftyBet(models.Model):
    bet = models.ForeignKey(FiftyFiftyOutcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.bet.fifty_fifty.question}, {self.bet.outcome}  by {self.entry.profile.user.username}"


class TournamentGoalsOutcome(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} goals: {self.min_value} - {self.max_value}" \
               f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        else:
            return f"{self.min_value} to {self.max_value}"


class TournamentRedCardsOutcome(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} red cards: {self.min_value} - {self.max_value}" \
               f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        else:
            return f"{self.min_value} to {self.max_value}"


class TournamentOwnGoalsOutcome(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} own goals: {self.min_value} - {self.max_value}" \
               f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        else:
            return f"{self.min_value} to {self.max_value}"


class TournamentHattricksOutcome(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.tournament.name} hattricks: {self.min_value} - {self.max_value}" \
               f" = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        else:
            return f"{self.min_value} to {self.max_value}"


class TournamentBetGroup(models.Model):
    total_goals_bet = models.ForeignKey(TournamentGoalsOutcome, on_delete=models.CASCADE)
    total_red_cards_bet = models.ForeignKey(TournamentRedCardsOutcome, on_delete=models.CASCADE)
    total_own_goals_bet = models.ForeignKey(TournamentOwnGoalsOutcome, on_delete=models.CASCADE)
    total_hattricks_bet = models.ForeignKey(TournamentHattricksOutcome, on_delete=models.CASCADE)
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Tournament bets by {self.entry.profile.user.username}"


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
        return f"Match {self.match_number}: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class GroupMatch(Match):

    class Meta:
        verbose_name_plural = "group matches"

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return f"Group {self.group.name}, Match {self.match_number}: {self.home_team.country.country_code} vs. {self.away_team.country.country_code}"


class GroupMatchOutcome(models.Model):
    match = models.ForeignKey(GroupMatch, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=1, choices=GroupMatch.MATCH_RESULT_CHOICES)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"Group {self.match.group.name}, Match {self.match.match_number}: {self.outcome} = {self.winning_amount}"


class GroupMatchBet(models.Model):
    bet = models.ForeignKey(GroupMatchOutcome, on_delete=models.CASCADE)
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"Bet ({self.bet.outcome}) on {self.bet.match.home_team.country.country_code} vs " \
               f"{self.bet.match.away_team.country.country_code} by {self.entry.profile.user.username}"


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
    first_goal_period = models.CharField(max_length=2, choices=MATCH_PERIOD_CHOICES, blank=True, null=True)
    own_goal = models.BooleanField(default=False)
    yellow_cards = models.IntegerField(default=0, blank=True, null=True)
    goals = models.IntegerField(default=0, blank=True, null=True)
    ref_continent = models.CharField(max_length=2, choices=REF_CONTINENT_CHOICES, blank=True, null=True)

    def __str__(self):
        return "Final match"


class FinalFirstGoalOutcome(models.Model):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=2, choices=FinalMatch.MATCH_PERIOD_CHOICES)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.outcome} = {self.winning_amount}"

    def verbose_outcome(self):
        return dict(FinalMatch.MATCH_PERIOD_CHOICES)[self.outcome]


class FinalOwnGoalOutcome(models.Model):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    outcome = models.BooleanField()
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.outcome} = {self.winning_amount}"

    def verbose_outcome(self):
        if self.outcome:
            return "Yes there will be"
        else:
            return "No there won't be"


class FinalYellowCardsOutcome(models.Model):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        if self.is_highest_value:
            return f"Final yellows: {self.min_value} or more = {self.winning_amount}"
        elif self.max_value == self.min_value:
            return f"Final yellows: {self.min_value} = {self.winning_amount}"
        else:
            return f"Final yellows: {self.min_value} to {self.max_value} = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        elif self.max_value == self.min_value:
            return self.min_value
        else:
            return f"{self.min_value} to {self.max_value}"


class FinalRefContinentOutcome(models.Model):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=2, choices=FinalMatch.REF_CONTINENT_CHOICES)
    winning_amount = models.IntegerField()

    def __str__(self):
        return f"{self.outcome} = {self.winning_amount}"

    def verbose_outcome(self):
        return dict(FinalMatch.REF_CONTINENT_CHOICES)[self.outcome]


class FinalGoalsOutcome(models.Model):
    final = models.ForeignKey(FinalMatch, on_delete=models.CASCADE)
    min_value = models.IntegerField()
    max_value = models.IntegerField()
    is_highest_value = models.BooleanField(default=False)
    winning_amount = models.IntegerField()

    def __str__(self):
        if self.is_highest_value:
            return f"Final goals: {self.min_value} or more = {self.winning_amount}"
        elif self.max_value == self.min_value:
            return f"Final goals: {self.min_value} = {self.winning_amount}"
        else:
            return f"Final goals: {self.min_value} to {self.max_value} = {self.winning_amount}"

    def verbose_outcome(self):
        if self.is_highest_value:
            return f"{self.min_value} or more"
        elif self.max_value == self.min_value:
            return self.min_value
        else:
            return f"{self.min_value} to {self.max_value}"


class FinalBetGroup(models.Model):
    final_first_goal_bet = models.ForeignKey(FinalFirstGoalOutcome, on_delete=models.CASCADE)
    final_own_goals_bet = models.ForeignKey(FinalOwnGoalOutcome, on_delete=models.CASCADE)
    final_yellow_cards_bet = models.ForeignKey(FinalYellowCardsOutcome, on_delete=models.CASCADE)
    final_ref_continent_bet = models.ForeignKey(FinalRefContinentOutcome, on_delete=models.CASCADE)
    final_goals_bet = models.ForeignKey(FinalGoalsOutcome, on_delete=models.CASCADE)
    entry = models.OneToOneField(Entry, on_delete=models.CASCADE)

    def __str__(self):
        return f"Final bets by {self.entry.profile.user.username}"


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
