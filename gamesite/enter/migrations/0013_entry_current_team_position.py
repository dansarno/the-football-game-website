# Generated by Django 3.1.3 on 2021-05-07 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0012_entry_correct_bets'),
    ]

    operations = [
        migrations.AddField(
            model_name='entry',
            name='current_team_position',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
