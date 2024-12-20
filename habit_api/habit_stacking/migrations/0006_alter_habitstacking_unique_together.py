# Generated by Django 5.1 on 2024-08-27 08:39

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('habit_stacking', '0005_alter_habitstacking_unique_together'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='habitstacking',
            unique_together={('user', 'habit1', 'habit2')},
        ),
    ]
