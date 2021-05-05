from rest_framework import serializers
import random
from .models import User, Question
from .level_design import generate_answers
from .serializers import QuestionSerializer


# Assumes that when note = 0, A is the note in question. Similarly, G refers to index 11
# This calculates Hz values starting at A2 = 110Hz
def note_to_frequency(note):
    # Frequency of A4 is 440Hz
    a = 440
    return (a / 4) * (2 ** (note / 12))


def generate_interval(semitones):
    base_note_index = random.randrange(0, 36)

    base_note = note_to_frequency(base_note_index)
    second_note = note_to_frequency(base_note_index + semitones)

    return base_note, second_note


def convert_answer_to_string(answer):

    number_component = answer[0]

    if number_component == 1:
        return "perfect Unison"
    elif number_component == 2:
        number_component = "2nd"
    elif number_component == 3:
        number_component = "3rd"
    elif number_component == 8:
        return "Perfect 8ve"
    else:
        number_component = str(number_component) + "th"
    output = answer[1] + " " + number_component
    return output


# Generates all data for a question
# Saves correct_answer to Question model, to be referenced in answer_check later on
# Serializes everything except correct_answer and sends to frontend
def create_random_question(user: User, given_level=None):

    question = "Identify the interval"

    # Generates all answers and random correct answer based on user's level
    current_user = user.profile

    # If specific level parameter was passed
    if given_level is not None:
        answers_data, correct_answer_data = generate_answers(given_level)
    # Else take user level
    else:
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

    # If a user already has a question, update it with new values
    random_question, created = Question.objects.update_or_create(
        profile=current_user,
        defaults={
            'question_text': question,
            'answers': answers,
            'correct_answer': correct_answer,
            'first_note': first_note,
            'second_note': second_note,
            'answered': False,
        }
    )

    # Excludes correct_answer in serialization
    serializer = QuestionSerializer(random_question)

    # Save to database
    random_question.save()
    return serializer.data
