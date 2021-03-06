from rest_framework import serializers
from enter import models
from users.models import Profile, Team
from django.contrib.auth.models import User
from django.db.models import Max


class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = ['id', 'name', 'score', 'position']


class CalledBetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)
    post_url = serializers.SerializerMethodField()
    winning_amount = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    question = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()

    class Meta:
        model = models.CalledBet
        fields = ['date', 'outcome', 'post_url', 'winning_amount', 'category', 'question', 'choice']

    def get_post_url(self, obj):
        return obj.post.get_absolute_url()

    def get_question(self, obj):
        return obj.outcome.short_question

    def get_choice(self, obj):
        return obj.outcome.short_choice

    def get_winning_amount(self, obj):
        return obj.outcome.winning_amount

    def get_category(self, obj):
        return obj.outcome.choice_group.game_category.title


class BetSerializer(serializers.ModelSerializer):
    outcome = serializers.StringRelatedField(read_only=True)
    called_bet = CalledBetSerializer(read_only=True)

    class Meta:
        model = models.Bet
        fields = ['success', 'outcome', 'called_bet']


class UpcomingBetSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    choice = serializers.SerializerMethodField()
    winning_amount = serializers.SerializerMethodField()

    class Meta:
        model = models.Bet
        fields = ['question', 'choice', 'winning_amount']

    def get_question(self, obj):
        return obj.outcome.short_question

    def get_choice(self, obj):
        return obj.outcome.short_choice

    def get_winning_amount(self, obj):
        return obj.outcome.winning_amount


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
    profile_url = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['user', 'profile_picture', 'profile_url', 'team']

    def get_profile_url(self, obj):
        return obj.get_absolute_url()


class SimpleEntrySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = ['id', 'label', 'view_url', 'profile']

    def get_view_url(self, obj):
        return obj.get_absolute_url()


class LeaderboardEntrySerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    position_logs = serializers.SerializerMethodField(
        'get_last_two_position_logs')
    form = serializers.SerializerMethodField('get_last_five_bets')
    upcoming = serializers.SerializerMethodField('get_upcoming_bets')
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = ['id', 'label', 'view_url', 'profile', 'current_score', 'correct_bets',
                  'current_position', 'current_team_position', 'position_logs', 'form', 'upcoming']

    def get_view_url(self, obj):
        return obj.get_absolute_url()

    def get_last_five_score_logs(self, obj):
        score_logs = models.ScoreLog.objects.filter(
            entry=obj).order_by('-called_bet__date')[:5]
        serializer = ScoreLogSerializer(
            instance=reversed(score_logs), many=True)
        return serializer.data

    def get_last_two_position_logs(self, obj):
        position_logs = models.PositionLog.objects.filter(
            entry=obj).order_by('-called_bet__date')[:2]
        serializer = PositionLogSerializer(
            instance=reversed(position_logs), many=True)
        return serializer.data

    def get_last_five_bets(self, obj):
        recent_bets = models.Bet.objects.filter(entry=obj).exclude(
            success__isnull=True).order_by('-updated_on')[:5]
        serializer = BetSerializer(instance=reversed(recent_bets), many=True)
        return serializer.data

    def get_upcoming_bets(self, obj):
        next_bets = models.Bet.objects.filter(entry=obj).exclude(
            success__isnull=False).order_by('outcome__choice_group__when_called', 'outcome__choice_group__order')[:3]
        serializer = UpcomingBetSerializer(instance=next_bets, many=True)
        return serializer.data


class SidebarEntrySerializer(serializers.ModelSerializer):
    top_score = serializers.SerializerMethodField()
    last_place = serializers.SerializerMethodField()
    form = serializers.SerializerMethodField('get_last_five_bets')
    view_url = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = ['id', 'label', 'view_url', 'top_score', 'last_place',
                  'current_score', 'current_position', 'form']

    def get_view_url(self, obj):
        return obj.get_absolute_url()

    def get_last_five_bets(self, obj):
        recent_bets = models.Bet.objects.filter(entry=obj).exclude(
            success__isnull=True).order_by('-updated_on')[:5]
        serializer = BetSerializer(instance=reversed(recent_bets), many=True)
        return serializer.data

    def get_top_score(self, obj):
        top_score = models.Entry.objects.all().aggregate(Max('current_score'))
        return top_score['current_score__max']

    def get_last_place(self, obj):
        last_place = models.Entry.objects.all().aggregate(Max('current_position'))
        return last_place['current_position__max']


class EntryChangesSerializer(serializers.ModelSerializer):
    profile = serializers.SerializerMethodField()

    class Meta:
        model = models.Entry
        fields = ['label', 'profile']

    def get_profile(self, obj):
        serializer = ProfileSerializer(instance=obj.profile)
        return serializer.data


class PositionLogChangeSerializer(serializers.ModelSerializer):
    entry = serializers.SerializerMethodField()
    previous_position = serializers.SerializerMethodField()
    new_position = serializers.SerializerMethodField()
    position_change = serializers.SerializerMethodField()

    class Meta:
        model = models.PositionLog
        fields = ['entry', 'previous_position',
                  'new_position', 'position_change']

    def get_entry(self, obj):
        serializer = EntryChangesSerializer(instance=obj.entry)
        return serializer.data

    def get_previous_position(self, obj):
        prev_pos_log = obj.get_prev_position_log()
        if prev_pos_log:
            return obj.get_prev_position_log().position
        else:
            return None

    def get_new_position(self, obj):
        return obj.position

    def get_position_change(self, obj):
        prev_pos_log = obj.get_prev_position_log()
        if prev_pos_log:
            return obj.get_prev_position_log().position - obj.position
        else:
            return None


class CalledBetWinnersAndLosersSerializer(serializers.ModelSerializer):
    biggest_winners = serializers.SerializerMethodField()
    biggest_losers = serializers.SerializerMethodField()

    class Meta:
        model = models.CalledBet
        fields = ['biggest_winners', 'biggest_losers']

    def get_biggest_winners(self, obj):
        biggest_winners = self.calc_winners_or_losers(obj, 20, False)
        serializer = PositionLogChangeSerializer(
            instance=biggest_winners, many=True)
        return serializer.data

    def get_biggest_losers(self, obj):
        biggest_losers = self.calc_winners_or_losers(obj, 20, True)
        serializer = PositionLogChangeSerializer(
            instance=biggest_losers, many=True)
        return serializer.data

    @staticmethod
    def calc_winners_or_losers(obj, num_entries, reverse=False):
        deltas_arr = []
        for position_log in models.PositionLog.objects.filter(called_bet=obj):
            deltas = {}
            if position_log.get_prev_position_log():
                deltas['change'] = position_log.position - \
                    position_log.get_prev_position_log().position
            else:
                deltas['change'] = position_log.position
            deltas['entry'] = position_log.entry
            deltas['username'] = position_log.entry.profile.user.username
            deltas['position_log'] = position_log
            deltas_arr.append(deltas)
        if reverse:
            filtered_deltas_arr = [d for d in deltas_arr if d['change'] >= 0]
        else:
            filtered_deltas_arr = [d for d in deltas_arr if d['change'] <= 0]
        sorted_deltas_arr = sorted(filtered_deltas_arr, key=lambda k:
                                   k['change'], reverse=reverse)[:num_entries]
        print(sorted_deltas_arr)
        return [deltas['position_log'] for deltas in sorted_deltas_arr]


class CalledBetStatsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CalledBetStats
        fields = ['num_correct', 'num_incorrect']
