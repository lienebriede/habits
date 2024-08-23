# Generated by Django 5.1 on 2024-08-22 13:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('couplings', '0001_initial'),
        ('habits', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HabitTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('completed', models.BooleanField(default=True)),
                ('coupling', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='coupling_trackings', to='couplings.coupling')),
                ('habit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='habit_trackings', to='habits.habit')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='habit_trackings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'habit', 'coupling', 'date')},
            },
        ),
    ]
