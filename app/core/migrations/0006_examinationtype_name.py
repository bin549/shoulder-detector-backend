# Generated by Django 4.0.5 on 2023-09-18 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_user_id_examination_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='examinationtype',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='RTL，CSA，AI'),
            preserve_default=False,
        ),
    ]