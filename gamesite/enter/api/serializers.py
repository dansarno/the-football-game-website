from rest_framework import serializers
from enter import models
from users.models import Profile
from django.contrib.auth.models import User


class CalledBetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.CalledBet
        fields = ['outcome', 'date']


class BetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)
    called_bet = CalledBetSerializer(read_only=True)

    class Meta:
        model = models.Bet
        fields = ['success', 'outcome', 'called_bet']


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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'team']


class EntrySerializer(serializers.ModelSerializer):
    score_logs = ScoreLogSerializer(many=True, read_only=True)
    position_logs = PositionLogSerializer(many=True, read_only=True)
    profile = ProfileSerializer(read_only=True)
    score_logs = serializers.SerializerMethodField('get_last_five_score_logs')
    position_logs = serializers.SerializerMethodField('get_last_five_position_logs')
    form = serializers.SerializerMethodField('get_last_five_bets')

    class Meta:
        model = models.Entry
        fields = ['id', 'label', 'profile', 'current_score', 'current_position', 'score_logs', 'position_logs', 'form']

    def get_last_five_score_logs(self, obj):
        score_logs = models.ScoreLog.objects.filter(entry=obj).order_by('-called_bet__date')[:5]
        serializer = ScoreLogSerializer(instance=reversed(score_logs), many=True)
        return serializer.data

    def get_last_five_position_logs(self, obj):
        position_logs = models.PositionLog.objects.filter(entry=obj).order_by('-called_bet__date')[:5]
        serializer = PositionLogSerializer(instance=reversed(position_logs), many=True)
        return serializer.data

    def get_last_five_bets(self, obj):
        recent_bets = models.Bet.objects.filter(entry=obj).exclude(success__isnull=True).order_by('-called_bet__date')[:5]
        serializer = BetSerializer(instance=reversed(recent_bets), many=True)
        return serializer.data
