from datetime import date

from app.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with predefined vulnerable users"

    def handle(self, *args, **kwargs):
        # Delete all existing users first
        User.objects.all().delete()

        users = [
            {
                "username": "admin",
                "password": "admin123",
                "role": "admin",
                "full_name": "Admin Person",
                "birth_date": "1980-01-01",
                "email": "admin@example.com",
            },
            {
                "username": "test",
                "password": "1234",
                "role": "user",
                "full_name": "Test User",
                "birth_date": "1990-05-10",
                "email": "test@example.com",
            },
            {
                # Your XSS payload user
                "username": "<img src=x onerror=alert(1)>",
                "password": "pw",
                "role": "user",
                "full_name": "Malicious User",
                "birth_date": "1995-09-09",
                "email": "xssuser@example.com",
            },
        ]

        for u in users:
            User.objects.create(
                username=u["username"],
                password=u["password"],  # *** intentionally plaintext ***
                role=u["role"],
                full_name=u["full_name"],
                birth_date=u["birth_date"],
                email=u["email"],
            )

        self.stdout.write(self.style.SUCCESS("Vulnerable users inserted."))
