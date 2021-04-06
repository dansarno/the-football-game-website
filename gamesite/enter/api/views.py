from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from .serializers import LeaderboardEntrySerializer, SidebarEntrySerializer, CalledBetStatsSerializer, CalledBetWinnersAndLosersSerializer


@api_view(['GET'])
def entries_detail(request):
    try:
        entries = models.Entry.objects.all()
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = LeaderboardEntrySerializer(entries, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def my_entries_detail(request):
    try:
        my_entries = models.Entry.objects.filter(
            profile=request.user.profile).all()
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SidebarEntrySerializer(my_entries, many=True)
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
