# Generated by Django 4.2.1 on 2023-05-13 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='Work_day',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
