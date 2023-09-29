# Generated by Django 4.0.5 on 2023-09-29 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_examination_input_image_alter_user_telephone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_delete', models.BooleanField(default=False, verbose_name='逻辑删除标志')),
                ('name', models.CharField(max_length=255, verbose_name='名称')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('delete_time', models.DateTimeField(null=True, verbose_name='删除时间')),
            ],
            options={
                'db_table': 'zone',
            },
        ),
    ]
