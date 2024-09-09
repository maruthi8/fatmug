from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from fatmug.celery_app import app as celery_app

print("fatmug/__init__.py has been imported.")

__all__ = ('celery_app',)
