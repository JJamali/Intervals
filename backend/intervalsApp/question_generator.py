# from .serializers import QuestionSerializer
from rest_framework import serializers
import random
from .models import User

notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G']


# Assumes that when note = 0, A is the note in question. Similarly, G refers to index 11
# This calculates Hz values starting at A2 = 110Hz
def note_to_frequency(note):
    # Frequency of A4 is 440Hz
    a = 440
    return (a / 4) * (2 ** ((note) / 12))


def generate_interval(semitones):

    base_note_index = notes.index(random.choice(notes))
    second_note_index = base_note_index + semitones

    # Randomly chooses octave multiplier value to vary Hz
    octave = random.choice([1, 2, 3])

    base_note = note_to_frequency(octave * base_note_index)
    second_note = note_to_frequency(octave * second_note_index)

    return base_note, second_note


# Manually define the difficulty of each level as difficulties cannot be generated, at least not reasonably
# This function defines the difficulty of each level and generate_interval actually generates the answer
def generate_answers(level):
    # Cases by level
    # Lists are in the form [interval number, quality, semitones]
    if level == 0:
        interval_options = [[3, "major", 4], [5, "perfect", 7], [8, "perfect", 12]]

    if level == 1:
        interval_options = [[3, "major", 4], [4, "perfect", 5], [5, "perfect", 7], [8, "perfect", 12]]

    return interval_options, random.choice(interval_options)


def create_random_question(user: User):

    question = "This is a question"

    # Generates all answers and random correct answer based on user's level
    current_user = user.profile
    answers_data, correct_answer_data = generate_answers(current_user.level)

    # Takes strings from interval_options list and puts them in one list, named answers
    answers = []
    for x in answers_data:
        answers.append(x[1])

    # Collect string of correct_answer
    correct_answer = correct_answer_data[1]

    # Generates Hz values of first and second notes to be played in frontend
    first_note, second_note = generate_interval(correct_answer_data[2])

    # Packages and serializes entire question to be sent
    random_question = Question(question, answers, correct_answer, first_note, second_note)
    serializer = QuestionSerializer(random_question)

    return serializer.data


class Question:
    def __init__(self, question, answers, correct_answer, first_note, second_note):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer
        self.first_note = first_note
        self.second_note = second_note


class QuestionSerializer(serializers.Serializer):
    question = serializers.CharField(max_length=20)
    answers = serializers.ListField(child=serializers.CharField(max_length=20))
    correct_answer = serializers.CharField(max_length=20)
    first_note = serializers.IntegerField(max_value=10, min_value=None)
    second_note = serializers.IntegerField(max_value=10, min_value=None)

    def create(self, validated_data):
        return Question(**validated_data)
