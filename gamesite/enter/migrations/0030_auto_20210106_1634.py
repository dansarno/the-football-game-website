# Generated by Django 3.1.3 on 2021-01-06 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0029_fiftyfiftybetgroup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fiftyfiftybetgroup',
            name='entry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='enter.entry'),
        ),
        migrations.AlterField(
            model_name='groupwinnerbetgroup',
            name='entry',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='enter.entry'),
        ),
    ]
