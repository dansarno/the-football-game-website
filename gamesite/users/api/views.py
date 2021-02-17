from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from users.models import Profile
from .serializers import ProfileSerializer


class ProfileDataView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        entry = models.Entry.objects.filter(profile=request.user.profile)[1]
        scorelog_qs = [scorelog['score'] for scorelog in entry.score_logs.values('score')]
        positionlog_qs = [positionlog['position'] for positionlog in entry.position_logs.values('position')]
        labels = [scorelog['called_bet__date'] for scorelog in entry.score_logs.values('called_bet__date')]

        data = {
            'id': entry.id,
            'current score': entry.current_score,
            'current position': entry.current_position,
            'scores': scorelog_qs,
            'positions': positionlog_qs,
            'labels': labels,
        }
        return Response(data)


@api_view(['GET'])
def profile_detail(request, username):
    try:
        profile = Profile.objects.get(user__username=username)
    except Profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
