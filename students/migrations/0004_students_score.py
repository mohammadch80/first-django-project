# Generated by Django 4.0.6 on 2023-04-25 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0003_alter_students_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
