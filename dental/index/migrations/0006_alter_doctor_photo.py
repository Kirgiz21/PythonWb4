# Generated by Django 5.0.6 on 2024-05-10 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_alter_doctor_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctor',
            name='photo',
            field=models.ImageField(upload_to='', verbose_name='Фото лікаря'),
        ),
    ]
