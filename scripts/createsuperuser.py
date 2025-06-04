import os
from django.contrib.auth import get_user_model

def run():
    User = get_user_model()

    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpassword")
    first_name = os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin")
    last_name = os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "User")

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password, first_name=first_name, last_name=last_name)
        print("Superuser created.")
        
    else:
        print("Superuser already exists.")
        
run()