# Generated by Django 4.2 on 2023-07-21 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('designers_hub', '0003_like'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
