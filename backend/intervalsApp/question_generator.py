from rest_framework import serializers
import random
from .models import User, Question

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
        interval_options = [[3, "Major", 4], [5, "Perfect", 7], [8, "Perfect", 12]]

    if level == 1:
        interval_options = [[3, "Major", 4], [4, "Perfect", 5], [5, "Perfect", 7], [8, "Perfect", 12]]

    return interval_options, random.choice(interval_options)


def convert_answer_to_string(answer):

    number_component = answer[0]

    if number_component == 1:
        number_component = "1st"
    elif number_component == 2:
        number_component = "2nd"
    elif number_component == 3:
        number_component = "3rd"
    else:
        number_component = str(number_component) + "th"

    output = answer[1] + " " + number_component
    return output


# Generates all data for a question
# Saves correct_answer to Question model, to be referenced in answer_check later on
# Serializes everything except correct_answer and sends to frontend
def create_random_question(user: User):

    question = "This is a question"

    # Generates all answers and random correct answer based on user's level
    current_user = user.profile
    answers_data, correct_answer_data = generate_answers(current_user.level)

    # Converts list of answers into a list of strings, to be sent to frontend
    answers = []
    for x in answers_data:
        answers.append(convert_answer_to_string(x))

    # Generates Hz values of first and second notes to be played in frontend
    # Must be done before converting correct_answer to string
    first_note, second_note = generate_interval(correct_answer_data[2])

    # Collect string of correct_answer
    # Must be done after generating interval
    correct_answer = convert_answer_to_string(correct_answer_data)

    # Packages and serializes entire question to be sent
    random_question = Question(question_text=question, answers=answers, correct_answer=correct_answer, first_note=first_note, second_note=second_note, profile=current_user)

    # Excludes correct_answer in serialization
    serializer = QuestionSerializer(random_question)

    # Save to database
    random_question.save()
    return serializer.data


class QuestionSerializer(serializers.Serializer):
    question_text = serializers.CharField(max_length=20)
    answers = serializers.ListField(child=serializers.CharField(max_length=20))
    # correct_answer = serializers.CharField(max_length=20)
    first_note = serializers.IntegerField(min_value=0)
    second_note = serializers.IntegerField(min_value=0)

    def create(self, validated_data):
        return Question(**validated_data)
