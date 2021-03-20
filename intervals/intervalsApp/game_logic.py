from .models import User


def handle_answer(user: User, correct):
    current_user = user.intervals_profile

    # Update user model
    if correct:

        current_user.total_correct += 1
        current_user.total_completed += 1
        # Cycle list data structure to contain most recent results
        current_user.recent_results.pop(0)
        current_user.recent_results.append(True)

    else:

        current_user.total_completed += 1
        # Cycle list data structure to contain most recent results
        current_user.recent_results.pop(0)
        current_user.recent_results.append(False)
