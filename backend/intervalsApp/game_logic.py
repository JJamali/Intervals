from .models import User
from django.apps import apps


def handle_answer(user: User, correct):
    current_user = user.profile

    # Update user model based on correctness
    if correct:

        current_user.total_correct += 1
        current_user.total_completed += 1
        # Cycle list data structure to contain most recent results
        if len(current_user.recent_results) >= apps.get_app_config('intervalsApp').SCORE_RANGE:
            current_user.recent_results.pop(0)
        current_user.recent_results.append(True)

    else:
        current_user.total_completed += 1
        # Cycle list data structure to contain most recent results
        if len(current_user.recent_results) >= apps.get_app_config('intervalsApp').SCORE_RANGE:
            current_user.recent_results.pop(0)
        current_user.recent_results.append(False)

    # Level up user
    required_correct_rate = 80

    # If minimum amount of questions have been answered and correct
    if len(current_user.recent_results) == apps.get_app_config('intervalsApp').SCORE_RANGE:
        if 100 * sum(current_user.recent_results) >= required_correct_rate * apps.get_app_config('intervalsApp').SCORE_RANGE:

            current_user.level += 1

    current_user.save()
