# Generated by Django 3.1.3 on 2021-05-12 10:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('enter', '0021_auto_20210512_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='outcome',
            name='choice_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='enter.choicegroup'),
        ),
    ]