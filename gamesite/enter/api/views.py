from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from users.models import Team
from .serializers import LeaderboardEntrySerializer, SidebarEntrySerializer, CalledBetStatsSerializer, CalledBetWinnersAndLosersSerializer, TeamSerializer, CalledBetSerializer, SimpleEntrySerializer
from django.conf import settings
from datetime import datetime


@api_view(['GET'])
def teams_detail(request):
    try:
        teams = Team.objects.all()
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class EntriesViewSet(ReadOnlyModelViewSet):
    queryset = models.Entry.objects.filter(has_submitted=True)
    serializer_class = LeaderboardEntrySerializer

    # @method_decorator(cache_page(60*60*2))
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)

    def list(self, request):
        cache_key = "entries_list"

        data = cache.get(cache_key)
        # if cached data exists and the game has started, use the cached data
        if data:  # and datetime.now() > settings.GAME_DEADLINE:
            return Response(data)

        response = super().list(request)
        cache.set(cache_key, response.data)
        return response


class SimpleEntriesViewSet(ReadOnlyModelViewSet):
    queryset = models.Entry.objects.filter(has_submitted=True)
    serializer_class = SimpleEntrySerializer


@api_view(['GET'])
def entries_detail(request):
    try:
        entries = models.Entry.objects.filter(has_submitted=True)
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def my_entries_detail(request):
    try:
        my_entries = models.Entry.objects.filter(
            profile=request.user.profile, has_submitted=True)
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SidebarEntrySerializer(my_entries, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def called_bets(request):
    try:
        called_bets = models.CalledBet.objects.all().order_by('date')
    except models.CalledBet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalledBetSerializer(called_bets, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def called_bet_stats(request, called_bet_id):
    try:
        stats = models.CalledBetStats.objects.get(called_bet__id=called_bet_id)
    except models.CalledBetStats.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalledBetStatsSerializer(stats)
        return Response(serializer.data)


@api_view(['GET'])
def called_bet_position_changes(request, called_bet_id):
    try:
        called_bet = models.CalledBet.objects.get(id=called_bet_id)
    except models.CalledBet.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CalledBetWinnersAndLosersSerializer(called_bet)
        return Response(serializer.data)
