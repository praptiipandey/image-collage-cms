# Generated by Django 2.1.4 on 2019-01-02 08:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('security', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='api_key',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 2, 8, 41, 12)),
        ),
    ]
