# Generated by Django 3.1.3 on 2021-02-17 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20210207_2115'),
        ('enter', '0007_auto_20210217_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='users.profile'),
        ),
    ]
