from django.apps import AppConfig


class IntervalsAppConfig(AppConfig):
    name = 'intervalsApp'
    SCORE_RANGE = 20  # The number of most recent results factor into calculation of score
    TOTAL_LEVELS = 5  # Maximum level. The first level is level 0.
