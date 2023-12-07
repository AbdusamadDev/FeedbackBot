import os
import threading

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
def run_bot():
    os.system("python3 ./bot/main.py")

application = get_wsgi_application()
threading.Thread(target=run_bot).start()
