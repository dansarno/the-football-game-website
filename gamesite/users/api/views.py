from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from users.models import Profile, Prize
from .serializers import ProfileHistorySerializer, ProfilePerformanceSerializer,  PrizeSerializer, EntryHistorySerializer


@api_view(['GET'])
def all_entries_history(request):
    try:
        entries = models.Entry.objects.all()
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntryHistorySerializer(entries, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def profile_history(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileHistorySerializer(profile)
        return Response(serializer.data)


@api_view(['GET'])
def profile_performance(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfilePerformanceSerializer(profile)
        return Response(serializer.data)


@api_view(['GET'])
def winning_positions(request):
    positions = Prize.objects.all()

    if request.method == 'GET':
        serializer = PrizeSerializer(positions, many=True)
        return Response(serializer.data)
