from django.apps import AppConfig
from datetime import timedelta


class IntervalsAppConfig(AppConfig):
    name = 'intervalsApp'
    SCORE_RANGE = 20  # The number of most recent results factor into calculation of score
    TOTAL_LEVELS = 5  # Maximum level. The first level is level 0.
    GUEST_INACTIVE_LIMIT = timedelta(weeks=1)  # Minimum time a guest can be inactive for before they are deleted