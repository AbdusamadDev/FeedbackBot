from django.contrib.auth.hashers import make_password

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

hashed_password = make_password("2005")
print(hashed_password)
