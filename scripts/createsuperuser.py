import os
from django.contrib.auth import get_user_model

def run():
    User = get_user_model()

    email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "adminpassword")

    if not User.objects.filter(email=email).exists():
        User.objects.create_superuser(email=email, password=password)
        print("Superuser created.")
        
    else:
        print("Superuser already exists.")
        
run()