from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken, ProfileSerializer
from .question_generator import create_random_question
from .game_logic import handle_answer
from django.contrib.auth import authenticate, login
from .models import Question, RecentResults, IntervalsProfile
from django.contrib.auth import logout


# User

# current_user handles requests pertaining to the current user
@api_view(['POST', 'GET'])
def current_user(request):

    if request.method == 'POST':
        if request.user.is_authenticated:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'GET':
        print('user', request.user)
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Quiz section

# Send question information
@api_view(['GET'])
def question(request):

    if request.method == 'GET':
        # Calls function from question_generator.py to create question
        current_user = request.user
        given_level = request.GET.get('level', default=current_user.profile.level)

        RecentResults.objects.get_or_create(profile=current_user.profile, level=given_level)
        # Update current_level
        current_user.current_level = given_level
        current_user.save()

        if given_level < 0 or given_level > current_user.profile.level:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        question_data = create_random_question(current_user, given_level)
        return Response(question_data, status=status.HTTP_201_CREATED)


# Return result
@api_view(['POST'])
def answer_check(request):

    if request.method == 'POST':

        # Receives user's guess from frontend
        guess = request.data["guess"]

        # Fetches question from database
        try:
            current_question = request.user.profile.question
        except Question.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        correct = current_question.correct_answer == guess

        handle_answer(request.user, correct)
        return Response({"correct": correct, "correct_answer": current_question.correct_answer}, status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)


# Handles logging out
# Throws no errors if user was not logged in
@api_view(['POST'])
def logout_view(request):
    logout(request)
    return Response(status=status.HTTP_200_OK)
    # Redirect to a success page.


@api_view(['GET'])
def global_stats(request):
    """Returns global stats for user. Global stats are the user's stats across all levels.

    Does not modify any data in database - model is not saved."""

    if request.user.is_authenticated:
        profile: IntervalsProfile = request.user.profile

        global_correct = 0
        global_answered = 0

        for r in profile.all_recent_results().values():
            global_correct += r.total_correct
            global_answered += r.total_completed

        print(global_correct, global_answered)

        return Response({"global_correct": global_correct,
                         "global_answered": global_answered},
                        status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def update_settings(request):
    """Receives command from frontend to update a user's setting."""

    if request.user.is_authenticated:
        profile: IntervalsProfile = request.user.profile

        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)