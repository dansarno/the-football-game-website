# Generated by Django 3.1.3 on 2021-02-06 23:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0002_auto_20210206_1845'),
        ('feed', '0004_calledbetpost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calledbetpost',
            name='bet',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='enter.calledbet'),
        ),
    ]
