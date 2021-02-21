from rest_framework import serializers
from enter import models
from users.models import Profile


class CalledBetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)

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


class EntrySerializer(serializers.ModelSerializer):
    score_logs = ScoreLogSerializer(many=True, read_only=True)
    position_logs = PositionLogSerializer(many=True, read_only=True)

    class Meta:
        model = models.Entry
        fields = ['id', 'label', 'current_score', 'current_position', 'score_logs', 'position_logs']


class ProfileSerializer(serializers.ModelSerializer):
    entries = EntrySerializer(many=True, read_only=True)

    class Meta:
        model = Profile
        fields = ['entries']
