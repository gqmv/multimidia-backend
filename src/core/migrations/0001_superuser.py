from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = []

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User

        DJANGO_SU_NAME = "admin"
        DJANGO_SU_EMAIL = "admin@admin.com"
        DJANGO_SU_PASSWORD = "admin"

        user = User.objects.create_superuser(
            username=DJANGO_SU_NAME, email=DJANGO_SU_EMAIL, password=DJANGO_SU_PASSWORD
        )

    operations = [
        migrations.RunPython(generate_superuser),
    ]
