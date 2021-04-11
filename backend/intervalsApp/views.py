from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from .question_generator import create_random_question
from .game_logic import handle_answer
from .models import Question, RecentResults


# User

# current_user handles requests pertaining to the current user
@api_view(['POST', 'GET'])
def current_user(request):

    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        print(request.user)
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserList(APIView):

    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):

        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
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

        current_user = request.user
        handle_answer(request.user, correct)
        return Response({"correct": correct, "correct_answer": current_question.correct_answer}, status=status.HTTP_200_OK)
