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
    position_logs = PositionLogSerializer(many=True, read_only=True)

    class Meta:
        model = models.Entry
        fields = [
            'id',
            'label',
            'position_logs'
        ]


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
        for category in models.GameCategory.objects.all():
            choice_groups = models.ChoiceGroup.objects.filter(
                game_category=category)
            total_bets = choice_groups.count()
            if not total_bets:
                continue
            percentage_success = dict()
            percentage_success['game_category'] = category.title
            winning_bets = 0
            any_called = False
            for choice_group in choice_groups:
                bet_in_same_group = models.Bet.objects.filter(
                    entry=obj, outcome__choice_group=choice_group).first()
                if bet_in_same_group.success is not None:
                    any_called = True
                if bet_in_same_group.success:
                    winning_bets += 1
            percentage_wins = (winning_bets / total_bets) * 100
            percentage_success['percentage_wins'] = percentage_wins
            if any_called:
                performance.append(percentage_success)
        return performance


class ProfileHistorySerializer(serializers.ModelSerializer):
    entries = EntryHistorySerializer(many=True, read_only=True)
    username = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['username', 'entries']

    def get_username(self, obj):
        return obj.user.username


class ProfilePositionHistorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    entries = EntryPositionHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'entries']


class ProfilePerformanceSerializer(serializers.ModelSerializer):
    entries = EntryPerformanceSerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['entries']


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ['position', 'winning_amount', 'band']
