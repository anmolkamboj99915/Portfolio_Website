from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Sync GitHub repositories into Project database"
    
    def handle(self, *args, **kwargs):
        
        self.stdout.write(self.style.NOTICE("Starting Github sync..."))
        
        try:
            from portfolio.github_sync import sync_github_projects
            sync_github_projects()
            self.stdout.write(
                self.style.SUCCESS("GitHub projects synced successfully")
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"GitHub sync failed: {str(e) or type(e).__name__}"))
            
            