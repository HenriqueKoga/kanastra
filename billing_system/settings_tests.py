from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'billing_system',
]

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.sqlite3',
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
