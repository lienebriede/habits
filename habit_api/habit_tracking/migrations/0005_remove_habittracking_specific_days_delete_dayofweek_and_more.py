# Generated by Django 5.1 on 2024-08-23 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('habit_tracking', '0004_dayofweek_habittracking_goal_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='habittracking',
            name='specific_days',
        ),
        migrations.DeleteModel(
            name='DayOfWeek',
        ),
        migrations.AddField(
            model_name='habittracking',
            name='specific_days',
            field=models.CharField(blank=True, choices=[('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday')], max_length=20),
        ),
    ]
