from django.core.management.base import BaseCommand

from users.models import Settings


class Command(BaseCommand):
    help = "Create default settings for all users"

    def handle(self, *args, **options):
        settings = Settings.objects.create()

        Settings.objects.bulk_create(settings)
        self.stdout.write(
            self.style.SUCCESS("Default settings objects has been created")
        )
