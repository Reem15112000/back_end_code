# Generated by Django 3.2 on 2023-05-23 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_consultation_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='gender',
            field=models.CharField(max_length=10),
        ),
    ]
