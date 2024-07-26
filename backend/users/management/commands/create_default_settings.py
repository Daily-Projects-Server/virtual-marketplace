from django.core.management.base import BaseCommand
from users.models import User, Settings


class Command(BaseCommand):
    help = "Create default settings for all users"

    def handle(self, *args, **options):
        settings = [Settings(user=user) for user in User.objects.all()]

        Settings.objects.bulk_create(settings)
        self.stdout.write(self.style.SUCCESS("Default settings created for all users"))
