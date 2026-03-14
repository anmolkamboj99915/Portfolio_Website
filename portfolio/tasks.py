from celery import shared_task
from django.core.cache import cache
from .github_sync import sync_github_projects

@shared_task
def sync_github():
    try:
        sync_github_projects()
        try:
            cache.set("github_synced", True, 3600)
        except Exception:
            pass
    finally:
        try:
            cache.delete("github_sync_running")
        except Exception:
            pass