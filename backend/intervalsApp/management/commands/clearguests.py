from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.contrib.auth import get_user_model
from datetime import datetime

class Command(BaseCommand):
    help = 'Deletes guest accounts that have been inactive for too long'

    def handle(self, *args, **options):
        oldest_login_limit = datetime.now() - apps.get_app_config('intervalsApp').GUEST_INACTIVE_LIMIT
        guests = get_user_model().objects.filter(is_guest=True, last_login__lt=oldest_login_limit)
        num_deleted = len(guests)
        guests.delete()

        self.stdout.write(self.style.SUCCESS(f'Deleted {num_deleted} guests'))