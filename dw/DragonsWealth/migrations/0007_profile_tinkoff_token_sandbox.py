# Generated by Django 3.1.7 on 2021-05-08 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DragonsWealth', '0006_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='tinkoff_token_sandbox',
            field=models.CharField(default='', max_length=255),
        ),
    ]