from django.core.management.base import BaseCommand
from django.apps import apps
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta


def clear_guests(allowed_time_period: timedelta) -> int:
    """Deletes all guests who haven't logged in within the given time period.

    :param allowed_time_period: A guest who hasn't logged in within this time period will be deleted.
    :return: The number of deleted guests.
    """
    oldest_login_limit = datetime.now() - allowed_time_period
    guests = get_user_model().objects.filter(is_guest=True, last_login__lt=oldest_login_limit)
    num_deleted = len(guests)
    guests.delete()
    return num_deleted


class Command(BaseCommand):
    help = 'Deletes guest accounts that have been inactive for too long'

    def handle(self, *args, **options):
        allowed_time_period = - apps.get_app_config('intervalsApp').GUEST_INACTIVE_LIMIT
        num_deleted = clear_guests(allowed_time_period)

        self.stdout.write(self.style.SUCCESS(f'Deleted {num_deleted} guests'))
