from django.contrib.auth.management.commands.createsuperuser import (
    Command as BaseCommand,
)
from django.core.management.base import CommandError


class Command(BaseCommand):
    help = "Create a superuser with a telegram ID"

    def handle(self, *args, **options):
        options["interactive"] = True
        database = options.get("database")
        telegram_id = None

        # Handle interactive mode
        if options["interactive"]:
            try:
                # You can include additional validation here if needed
                telegram_id = input("Telegram ID: ")
            except KeyboardInterrupt:
                raise CommandError("Operation cancelled.")
            except Exception as e:
                raise CommandError(f"An error occurred: {e}")

        superuser = self.UserModel._default_manager.db_manager(
            database
        ).create_superuser(**options, telegram_id=telegram_id)
        if options.get("verbosity", 0) >= 1:
            self.stdout.write("Superuser created successfully.")
