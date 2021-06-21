from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
from .serializers import BriefUserSerializer, UserSerializer, StatsSerializer, SettingsSerializer
from .question_generator import QuestionSerializer
from .question_generator import create_random_question
from .game_logic import handle_answer
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Question, RecentResults, IntervalsProfile
import json
from .permissions import IsItselfOrReadOnly, IsItself
from rest_framework.permissions import IsAuthenticatedOrReadOnly

User = get_user_model()


@api_view(['GET'])
def get_current_user_id(request):
    """Returns the current user's id if logged in"""
    if request.method == 'GET':
        if request.user.is_authenticated:
            user_id = request.user.pk
            return Response({'id': user_id}, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class UserList(generics.ListCreateAPIView):
    """Allows anyone to view user list or create new users"""
    queryset = User.objects.all()
    serializer_class = BriefUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.get_queryset().get(pk=self.kwargs.get('id'))


class StatsView(generics.RetrieveAPIView):
    queryset = IntervalsProfile.objects.all()
    serializer_class = StatsSerializer

    def get_object(self):
        user = User.objects.get(pk=self.kwargs.get('id'))
        return self.get_queryset().get(user=user)


class SettingsView(generics.RetrieveUpdateAPIView):
    queryset = IntervalsProfile.objects.all()
    serializer_class = SettingsSerializer
    permission_classes = [IsItselfOrReadOnly]

    def get_object(self):
        user = User.objects.get(pk=self.kwargs.get('id'))
        self.check_object_permissions(self.request, user)
        return self.get_queryset().get(user=user)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = json.loads(request.body)
        serializer = self.get_serializer_class()(profile, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, *args, **kwargs):
        profile = self.get_object()
        data = json.loads(request.body)
        serializer = self.get_serializer_class()(profile, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200)
        return Response(status=status.HTTP_400_BAD_REQUEST)


# Quiz section


class QuestionView(generics.GenericAPIView, mixins.RetrieveModelMixin, mixins.CreateModelMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [IsItselfOrReadOnly, IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_object(self):
        user = User.objects.get(pk=self.kwargs.get('id'))
        self.check_object_permissions(self.request, user)
        return generics.get_object_or_404(self.get_queryset(), profile=user.profile)

    def create(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get('id'))
        self.check_object_permissions(request, user)

        # Don't create a question if the previous question hasn't been answered
        try:
            question = user.profile.question
            if not question.answered:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            pass

        given_level = request.GET.get('level', default=user.profile.level)

        RecentResults.objects.get_or_create(profile=user.profile, level=given_level)
        # Update current_level
        user.current_level = given_level
        user.save()

        if given_level < 0 or given_level > user.profile.level:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        question_data = create_random_question(user, given_level)
        return Response(question_data, status=status.HTTP_201_CREATED)


class AnswerView(APIView):
    permission_classes = [IsItself]

    def post(self, request, id):
        # Receives user's guess from frontend
        user = User.objects.get(pk=id)
        self.check_object_permissions(request, user)

        try:
            guess = request.data["guess"]
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Fetches question from database
        try:
            current_question = user.profile.question
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        # Reject the guess if the question has already been answered before
        if current_question.answered:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            current_question.answered = True
            current_question.save()

        correct = current_question.correct_answer == guess

        handle_answer(user, correct)
        return Response({"correct": correct, "correct_answer": current_question.correct_answer},
                        status=status.HTTP_200_OK)


@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request, username=username, password=password)
        print(user)
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
