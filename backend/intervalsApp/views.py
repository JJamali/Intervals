from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSerializerWithToken
from .question_generator import create_random_question, QuestionSerializer
from .game_logic import handle_answer


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

        question_data = create_random_question(current_user)
        return Response(question_data, status=status.HTTP_201_CREATED)


# Return result
@api_view(['POST'])
def answer_check(request):

    if request.method == 'POST':
        # Backend sends frontend correct guess
        print(request.user)
        data = request.data["question"]
        guess = request.data["guess"]

        # Deserialization and game logic handling
        serializer = QuestionSerializer(data=data)
        if serializer.is_valid():
            question = serializer.save()

            correct = question.correct_answer == guess
            handle_answer(request.user, correct)
            return Response({"correct": correct, "correct_answer": question.correct_answer}, status=status.HTTP_200_OK)
