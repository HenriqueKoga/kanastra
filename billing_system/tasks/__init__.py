# billing_system/__init__.py

from ..infrastructure.celery import app

__all__ = ('app',)
