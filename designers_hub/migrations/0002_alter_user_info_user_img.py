# Generated by Django 4.2 on 2023-07-19 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designers_hub', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='user_img',
            field=models.ImageField(blank=True, null=True, upload_to='user-images'),
        ),
    ]
