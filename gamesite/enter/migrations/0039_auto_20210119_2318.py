# Generated by Django 3.1.3 on 2021-01-19 23:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0038_auto_20210119_2252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topgoalscoringgroupbet',
            old_name='outcome',
            new_name='choice',
        ),
        migrations.RenameField(
            model_name='topgoalscoringplayerbet',
            old_name='outcome',
            new_name='choice',
        ),
    ]
