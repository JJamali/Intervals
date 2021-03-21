from django.apps import apps
from .models import User


def handle_answer(user: User, correct):
    print(user, correct)
    current_user = user.profile

    # Update user profile
    current_user.total_completed += 1
    current_user.total_correct += 1 if correct else 0

    # pop if the recent results list is full because
    # we don't want it to exceed a target number of elements
    if len(current_user.recent_results) >= apps.get_app_config('intervalsApp').SCORE_RANGE:
        current_user.recent_results.pop(0)

    current_user.recent_results.append(correct)

    # save the user so that the changes are applied
    current_user.save()
