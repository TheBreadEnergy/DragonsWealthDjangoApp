# Generated by Django 3.1.7 on 2021-05-08 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DragonsWealth', '0002_auto_20210508_0313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='tinkoff_token',
            field=models.TextField(blank=True, max_length=255),
        ),
    ]