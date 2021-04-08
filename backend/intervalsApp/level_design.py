import random


# In the form [scale degree, quality, semitones]

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

intervals_dict = {
    "major": major_dict,
    "minor": minor_dict,
    "perfect": perfect_dict,
}


# Manually define the difficulty of each level as difficulties cannot be generated, at least not reasonably
# This function defines the difficulty of each level and generate_interval actually generates the answer
def generate_answers(level):
    # Cases by level
    # Lists are in the form [interval number, quality, semitones]
    if level == 0:
        interval_options = [intervals_dict["major"][3],
                            intervals_dict["perfect"][5],
                            intervals_dict["perfect"][8]]

    if level == 1:
        interval_options = [intervals_dict["major"][3],
                            intervals_dict["major"][4],
                            intervals_dict["perfect"][5],
                            intervals_dict["perfect"][8]]

    return interval_options, random.choice(interval_options)