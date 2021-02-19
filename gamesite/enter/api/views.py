from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework import authentication, permissions
from rest_framework.decorators import api_view
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from enter import models
from .serializers import EntrySerializer


@api_view(['GET'])
def entries_detail(request):
    try:
        entries = models.Entry.objects.all()
    except models.Entry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = EntrySerializer(entries, many=True)
        return Response(serializer.data)
