from .models import User, RecentResults
from django.apps import apps

SCORE_RANGE = apps.get_app_config('intervalsApp').SCORE_RANGE


def handle_answer(user: User, correct):
    """
    This function has two parts to it. First, it cycles the recent_results array,
    removing the oldest response and adding the newest. Then, it decides whether or not to level up the user based on
    the level they are currently viewing, and their score for the level.
    """
    current_user = user.profile
    recent_results = current_user.recent_results_at_level(current_user.current_level)

    # Total completed is always updated
    recent_results.total_completed += 1

    # Cycle list data structure to contain most recent results
    if len(recent_results.recent_results) >= SCORE_RANGE:
        recent_results.recent_results.pop(0)

    # Update user model based on correctness
    if correct:
        recent_results.total_correct += 1
        recent_results.recent_results.append(True)

    else:
        recent_results.recent_results.append(False)

    # Level up user logic

    # If level being done is user's level
    # This means that if the user is currently using a previous level, they would not level up
    if current_user.level == current_user.current_level:
        required_correct_rate = 80
        # If minimum amount of questions have been answered and correct
        if len(recent_results.recent_results) == SCORE_RANGE:
            if 100 * sum(recent_results.recent_results) >= required_correct_rate * SCORE_RANGE:

                # If user is max level, do not increase level
                if current_user.level == apps.get_app_config('intervalsApp').TOTAL_LEVELS:
                    pass
                # Else, increase level
                else:
                    current_user.level += 1
                    current_user.current_level = current_user.level
                    RecentResults.objects.get_or_create(profile=current_user, level=current_user.level)

    recent_results.save()
    current_user.save()
