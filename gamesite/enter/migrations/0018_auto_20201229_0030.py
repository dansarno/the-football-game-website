# Generated by Django 3.1.3 on 2020-12-29 00:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0017_auto_20201228_1637'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='is_top_team',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='fastestgoaloutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='fastestyellowcardsoutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='highestscoringteamoutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='mostyellowcardsoutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='toreachfinaloutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='toreachsemifinaloutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
        migrations.AlterField(
            model_name='towinoutcome',
            name='team',
            field=models.ForeignKey(limit_choices_to={'is_top_team': True}, on_delete=django.db.models.deletion.CASCADE, to='enter.team'),
        ),
    ]