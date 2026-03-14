import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    help = "Create superuser automatically if not exists"

    def handle(self, *args, **kwargs):

        User = get_user_model()

        username = (os.getenv("DJANGO_SUPERUSER_USERNAME") or "").strip()
        email = (os.getenv("DJANGO_SUPERUSER_EMAIL") or "").strip()
        password = (os.getenv("DJANGO_SUPERUSER_PASSWORD") or "").strip()
        
        if not username or not email or not password:
            self.stdout.write(self.style.WARNING("Superuser environment variables not set"))
            return
        
        try:
            try:
                User.objects.exists()
            except Exception as db_error:
                self.stdout.write(self.style.ERROR(f"Database not ready: {db_error}"))
                return

            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={"email": email}
            )
            
            if created:
                user.set_password(password)
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS("Superuser created"))
            else:
                updated_fields = []
                
                if user.email != email:
                    user.email = email
                    updated_fields.append("email")
                    
                if not user.is_staff:
                    user.is_staff = True
                    updated_fields.append("is_staff")
                
                if not user.is_superuser:
                    user.is_superuser = True
                    updated_fields.append("is_superuser")
                    
                if updated_fields:  
                    user.save(update_fields=updated_fields)
                self.stdout.write("Superuser already exists")
       
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed creating superuser: {e}"))
