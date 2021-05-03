from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.viewsets import ReadOnlyModelViewSet
from django.core.cache import cache
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from users.models import Profile, Prize
from .serializers import ProfileHistorySerializer, ProfilePerformanceSerializer, \
    PrizeSerializer, ProfilePositionHistorySerializer


@api_view(['GET'])
def all_entries_history(request):
    try:
        profiles = Profile.objects.all()
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfilePositionHistorySerializer(profiles, many=True)
        return Response(serializer.data)


class AllHistoryViewSet(ReadOnlyModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = ProfilePositionHistorySerializer

    def list(self, request):
        cache_key = f"all_history_list"

        data = cache.get(cache_key)
        if data:
            return Response(data)

        response = super().list(request)
        cache.set(cache_key, response.data)
        return response


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
