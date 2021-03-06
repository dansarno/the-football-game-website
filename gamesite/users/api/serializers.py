from rest_framework import serializers
from enter import models
from users.models import Profile, Prize


class CalledBetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)
    date = serializers.DateTimeField()

    class Meta:
        model = models.CalledBet
        fields = ['outcome', 'date']


class ScoreLogSerializer(serializers.ModelSerializer):
    called_bet = CalledBetSerializer(read_only=True)

    class Meta:
        model = models.ScoreLog
        fields = ['score', 'called_bet']


class PositionLogSerializer(serializers.ModelSerializer):
    called_bet = CalledBetSerializer(read_only=True)

    class Meta:
        model = models.PositionLog
        fields = ['position', 'called_bet']


class PositionLogOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.PositionLog
        fields = ['position',]


class EntryHistorySerializer(serializers.ModelSerializer):
    score_logs = ScoreLogSerializer(many=True, read_only=True)
    position_logs = PositionLogSerializer(many=True, read_only=True)

    class Meta:
        model = models.Entry
        fields = [
            'id',
            'label',
            'current_score',
            'current_position',
            'score_logs',
            'position_logs'
        ]


class EntryPositionHistorySerializer(serializers.ModelSerializer):
    position_logs = PositionLogOnlySerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = [
            'label',
            'current_position',
            'username',
            'position_logs'
        ]

    def get_username(self, obj):
        return obj.profile.user.username


class EntryPerformanceSerializer(serializers.ModelSerializer):
    performance = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = [
            'id',
            'label',
            'performance',
        ]

    def get_performance(self, obj):
        performance = []
        game_categories = models.GameCategory.objects.all()
        for category in game_categories:
            choice_groups = models.ChoiceGroup.objects.filter(
                game_category=category)
            total_bets = choice_groups.count()
            if not total_bets:
                continue
            percentage_success = dict()
            percentage_success['game_category'] = category.title
            winning_bets = 0
            score = 0
            total_score = 0
            total_bets = 0
            any_called = False
            for choice_group in choice_groups:
                bet_in_same_group = models.Bet.objects.filter(
                    entry=obj, outcome__choice_group=choice_group).first()
                if bet_in_same_group.success is not None:
                    total_bets += 1
                    total_score += bet_in_same_group.outcome.winning_amount
                    any_called = True
                if bet_in_same_group.success:
                    winning_bets += 1
                    score += bet_in_same_group.outcome.winning_amount
            if any_called:
                percentage_wins = (winning_bets / total_bets) * 100
                percentage_score = (score / total_score) * 100
                percentage_success['percentage_wins'] = percentage_wins
                percentage_success['percentage_score'] = percentage_score
                performance.append(percentage_success)
        return performance


class ProfileHistorySerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'entries']

    def get_username(self, obj):
        return obj.user.username

    def get_entries(self, obj):
        valid_entries = models.Entry.objects.filter(
            profile=obj, has_submitted=True)
        serializer = EntryHistorySerializer(
            instance=valid_entries, many=True, read_only=True)
        return serializer.data


class ProfilePositionHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    entries = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'entries']

    def get_entries(self, obj):
        valid_entries = models.Entry.objects.filter(
            profile=obj, current_position__lte=20, has_submitted=True)
        serializer = EntryPositionHistorySerializer(
            instance=valid_entries, many=True, read_only=True)
        return serializer.data


class ProfilePerformanceSerializer(serializers.ModelSerializer):
    entries = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['entries']

    def get_entries(self, obj):
        valid_entries = models.Entry.objects.filter(
            profile=obj, has_submitted=True)
        serializer = EntryPerformanceSerializer(
            instance=valid_entries, many=True, read_only=True)
        return serializer.data


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ['position', 'winning_amount', 'band']
