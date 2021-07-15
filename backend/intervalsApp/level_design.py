import random


# In the form: [scale degree, quality, semitones]

major_dict = {
    2: [2, "Major", 2],
    3: [3, "Major", 4],
    6: [6, "Major", 9],
    7: [7, "Major", 11],
}

minor_dict = {
    2: [2, "Minor", 1],
    3: [3, "Minor", 3],
    6: [6, "Minor", 9],
    7: [7, "Minor", 10],
}

perfect_dict = {
    1: [1, "Perfect", 0],  # Unison
    4: [4, "Perfect", 5],  # Perfect 4th
    5: [5, "Perfect", 7],  # Perfect 5th
    8: [8, "Perfect", 12]  # 8ve
}

augmented_dict = {
    1: [1, "Augmented", 1],
    2: [2, "Augmented", 3],
    3: [3, "Augmented", 5],
    4: [4, "Augmented", 6],
    5: [5, "Augmented", 8],
    6: [6, "Augmented", 10],
    7: [7, "Augmented", 12],
}

diminished_dict = {
    2: [2, "Diminished", 0],
    3: [3, "Diminished", 2],
    4: [4, "Diminished", 4],
    5: [5, "Diminished", 6],
    6: [6, "Diminished", 7],
    7: [7, "Diminished", 9],
    8: [8, "Diminished", 11]
}

intervals_dict = {
    "major": major_dict,
    "minor": minor_dict,
    "perfect": perfect_dict,
    "augmented": augmented_dict,
    "diminished": diminished_dict,
}


# This function defines the difficulty of each level and generate_interval actually generates the answer
def generate_answers(level):
    """
    Returns all options from a level and one random correct answer as a tuple. Each level is defined manually.
    Lists are in the form [scale degree, quality, semitones].
    This function defines the difficulty of each level and generate_interval actually generates the answer.
    """

    if level == 0:
        interval_options = [intervals_dict["major"][3],
                            intervals_dict["perfect"][5],
                            intervals_dict["perfect"][8]]

    if level == 1:
        interval_options = [intervals_dict["major"][3],
                            intervals_dict["perfect"][4],
                            intervals_dict["perfect"][5],
                            intervals_dict["perfect"][8]]

    if level == 2:
        interval_options = [intervals_dict["major"][2],
                            intervals_dict["major"][6],
                            intervals_dict["major"][7]]

    if level == 3:
        interval_options = [intervals_dict["major"][2],
                            intervals_dict["major"][3],
                            intervals_dict["perfect"][4],
                            intervals_dict["perfect"][5],
                            intervals_dict["major"][6],
                            intervals_dict["major"][7],
                            intervals_dict["perfect"][8]]

    if level == 4:
        interval_options = [intervals_dict["minor"][2],
                            intervals_dict["minor"][3],
                            intervals_dict["minor"][6],
                            intervals_dict["minor"][7]]

    if level == 5:
        interval_options = [intervals_dict["minor"][2],
                            intervals_dict["minor"][3],
                            intervals_dict["perfect"][4],
                            intervals_dict["perfect"][5],
                            intervals_dict["minor"][6],
                            intervals_dict["minor"][7],
                            intervals_dict["perfect"][8]]

    return interval_options, random.choice(interval_options)
