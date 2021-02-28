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


class CategorySerializer(serializers.ModelSerializer):
    # title = serializers.CharField(read_only=True)
    percentage_wins = serializers.SerializerMethodField(source='get_percentage_wins')

    class Meta:
        model = models.GameCategory
        fields = ['title', 'percentage_wins']

    def get_percentage_wins(self, obj):
        choice_groups = models.ChoiceGroup.objects.filter(game_category=obj)
        total_bets = choice_groups.count()
        # print(self)
        if not total_bets:
            return -1
        winning_bets = 0
        for choice_group in choice_groups:
            if models.Bet.objects.filter(entry=models.Entry.objects.first(), outcome__choice_group=choice_group)[0].success:
                winning_bets += 1
        percentage_wins = (winning_bets / total_bets) * 100
        return percentage_wins


class EntrySerializer(serializers.ModelSerializer):
    score_logs = ScoreLogSerializer(many=True, read_only=True)
    position_logs = PositionLogSerializer(many=True, read_only=True)
    percentage_success = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = [
            'id',
            'label',
            'current_score',
            'current_position',
            'percentage_success',
            'score_logs',
            'position_logs'
        ]

    def get_percentage_success(self, obj):
        serializer = CategorySerializer(models.GameCategory.objects.all(), many=True)
        print(obj.id)
        return serializer.data


class ProfileSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['entries']


class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prize
        fields = ['position', 'winning_amount', 'band']
