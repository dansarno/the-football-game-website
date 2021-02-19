from rest_framework import serializers
from enter import models
from users.models import Profile
from django.contrib.auth.models import User


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

    class Meta:
        model = models.Entry
        fields = ['id', 'profile', 'current_score', 'current_position', 'score_logs', 'position_logs']
