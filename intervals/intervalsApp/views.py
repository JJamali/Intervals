from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from intervalsApp.models import User


@api_view(['POST'])
def create_user(request):  # user is symbolic representation of current user being processed
    if request.method == 'POST':
        username = request.data['username']
        user = User(username=username)
        user.save()
        return Response(status=status.HTTP_201_CREATED)
