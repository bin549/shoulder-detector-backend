# Generated by Django 4.0.5 on 2023-09-18 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_examination_examination_type'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ExaminationResult',
        ),
    ]
