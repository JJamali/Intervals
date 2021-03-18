# from .serializers import QuestionSerializer
from rest_framework import serializers


def create_random_question():

    question = "This is a question"
    answers = ["one", "two"]
    correct_answer = "one"

    random_question = Question(question, answers, correct_answer)
    serializer = QuestionSerializer(random_question)

    return serializer.data


class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=20)
    answers = serializers.ListField(child=serializers.CharField(max_length=20))
    correct_answer = serializers.CharField(max_length=20)

    def create(self, validated_data):
        return Question(**validated_data)