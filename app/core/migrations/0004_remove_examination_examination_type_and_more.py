# Generated by Django 4.0.5 on 2023-09-18 15:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_examinationresult_examinationtype_patient_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examination',
            name='examination_type',
        ),
        migrations.AddField(
            model_name='examination',
            name='patient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='core.patient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='examination',
            name='user_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='name',
            field=models.CharField(default=1, max_length=255, verbose_name='姓名'),
            preserve_default=False,
        ),
    ]