# Generated by Django 3.1.3 on 2021-03-12 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0008_auto_20210312_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalgoalsoutcome',
            name='is_highest_value',
        ),
        migrations.AlterField(
            model_name='finalgoalsoutcome',
            name='max_value',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='finalgoalsoutcome',
            name='min_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
