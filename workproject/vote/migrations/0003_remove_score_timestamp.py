# Generated by Django 5.1.2 on 2024-11-16 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0002_score_timestamp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='score',
            name='timestamp',
        ),
    ]
